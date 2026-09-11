#import json #no json used in this file, but used in vitals/ai_service.py and medications/ai_service.py
from openai import OpenAI
from django.conf import settings
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from bert_score import score as bertscore_score
import nltk
import numpy as np
   

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def transcribe_audio(audio_file_path: str) -> str:
    """Send audio file to Whisper and return transcript."""
    with open(audio_file_path, 'rb') as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            language="en"
        )
    return response.text


def extract_care_note_from_transcript(transcript: str) -> str:
    """
    Use GPT to turn a rambling spoken care note into a structured,
    professional, third-person clinical note. One flowing paragraph,
    no headings. Refuses to fabricate content if the transcript is
    empty, nonsensical, or unrelated to care.

    Note: this pipeline does not perform speaker diarization — if the
    transcript contains more than one voice, GPT infers likely speaker
    roles from context only, and is instructed to hedge where unclear
    rather than guess with false confidence.
    """

    prompt = f"""
You are a clinical documentation assistant helping care home staff turn a spoken
account into a professional care note for a resident's file.

Transcript: "{transcript}"

Rewrite this as a clear, professional care note following these rules:
- Write in third person, past tense, formal clinical tone (e.g. "Resident was
  observed to..." not "I saw..." or "She was...").
- Do NOT reproduce the transcript verbatim — rephrase into concise, factual
  clinical language.
- If multiple topics are mentioned (e.g. nutrition, mood, mobility, an incident),
  organise them into one flowing, well-structured paragraph — do not use
  headings, bullet points, or bold text. Use clear topic transitions instead
  (e.g. "Following lunch, resident..." / "Later in the shift...").
- Remove filler words, false starts, and conversational speech patterns
  ("um", "like", "so yeah") entirely.
- Do NOT invent, assume, or add any clinical detail, measurement, name, or
  event that was not stated in the transcript.
- If the transcript mentions a fall, injury, safeguarding concern, or any
  urgent issue, state it clearly and factually without dramatizing it.
- If the transcript appears to contain more than one speaker (e.g. a
  back-and-forth exchange), do not confidently assign specific statements
  to "the carer" or "the resident" unless the content makes the speaker
  unambiguous (e.g. a direct question clearly being answered). Where it is
  unclear who said what, describe the interaction generally (e.g. "An
  exchange took place regarding...") rather than attributing specific
  words to a specific person.
- Keep the note reasonably concise — a professional summary, not a padded-out
  essay. Aim for roughly the same amount of information as the transcript,
  just reworded and organised.
- If the transcript does not contain any genuine care-related information
  (e.g. it is empty, just background noise, nonsensical, or unrelated small
  talk with no actual care content), do NOT invent a plausible-sounding note
  under any circumstances. Instead, return exactly this and nothing else:
  NO_CONTENT
- Return ONLY the finished note text. No preamble, no explanation, no quotation
  marks around it.
"""

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()

def summarize_care_notes_period(notes) -> str:
    """
    Takes an iterable of CareNote objects (already filtered to one patient
    and one date range) and produces a single professional summary covering
    that period. Only ever summarizes what's actually in the notes — never
    invents patterns, trends, or events not recorded.
    """

    if not notes:
        return "NO_CONTENT"

    # Build a plain-text log GPT can read, oldest first so the summary
    # reads in chronological order like a real shift handover would.
    entries = []
    for note in sorted(notes, key=lambda n: n.created_at):
        entries.append(
            f"[{note.created_at.strftime('%d %b %Y %H:%M')}] "
            f"{note.get_category_display()} ({note.get_priority_display()}): {note.note_text}"
        )
    log_text = "\n".join(entries)

    prompt = f"""
You are a clinical documentation assistant. Below is a chronological log of
care notes recorded for one resident over a selected period.

Care note log:
{log_text}

Write a single professional summary of this period for care home staff
handover purposes. Follow these rules:
- Write in third person, past tense, formal clinical tone.
- Summarize themes and patterns actually present in the log (e.g. mood,
  nutrition, mobility, sleep, incidents) — only mention what's genuinely
  reflected in multiple entries or is individually significant.
- If there are any urgent, safeguarding, or incident-related entries, mention
  them clearly and specifically, including their date.
- Do NOT invent, assume, or add any detail, trend, or event not present in
  the log above.
- If the log is too short or repetitive to draw out real patterns, say so
  plainly rather than padding it out.
- Do not use headings or bullet points — one flowing, well-organized summary,
  similar in style to a shift handover note.
- Return ONLY the summary text. No preamble, no explanation.
"""

    client = OpenAI(api_key=settings.OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()

def compute_summary_metrics(summary_text: str, source_notes_text: str) -> dict:
    """
    Computes ROUGE, BLEU, and BERTScore comparing the AI summary against
    the concatenated original care notes (the "source"). This measures
    faithfulness/overlap to source, not correctness against a human-written
    gold-standard summary — there is no human reference in this pipeline.
    """

    # --- ROUGE ---
    rouge = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_scores = rouge.score(source_notes_text, summary_text)

    # --- BLEU ---
    # NLTK expects the reference as a list of tokenised words, and the
    # candidate (summary) also tokenised. Smoothing avoids a score of 0
    # when there's no exact 4-gram overlap, which is common with short text.
    reference_tokens = [nltk.word_tokenize(source_notes_text.lower())]
    candidate_tokens = nltk.word_tokenize(summary_text.lower())
    smoothing = SmoothingFunction().method1
    bleu = sentence_bleu(reference_tokens, candidate_tokens, smoothing_function=smoothing)

    # --- BERTScore ---
    # Compares semantic similarity (not just word overlap) using a local
    # BERT model. Slower than ROUGE/BLEU, runs on CPU by default.
    P, R, F1 = bertscore_score([summary_text], [source_notes_text], lang='en', verbose=False)

    return {
        'rouge1': round(rouge_scores['rouge1'].fmeasure, 4),
        'rouge2': round(rouge_scores['rouge2'].fmeasure, 4),
        'rougeL': round(rouge_scores['rougeL'].fmeasure, 4),
        'bleu': round(bleu, 4),
        'bertscore_precision': round(P.mean().item(), 4),
        'bertscore_recall': round(R.mean().item(), 4),
        'bertscore_f1': round(F1.mean().item(), 4),
    }

def build_evidence_links(summary_text: str, notes) -> list:
    """
    For each sentence in the AI summary, finds which original care note(s)
    it is most semantically grounded in, using OpenAI embeddings + cosine
    similarity. Returns a list of dicts staff can use to verify the summary
    against the actual source notes it was generated from.
    """
    import numpy as np
    from openai import OpenAI
    from django.conf import settings

    client = OpenAI(api_key=settings.OPENAI_API_KEY)

    # Split summary into sentences to link individually
    summary_sentences = [s.strip() for s in nltk.sent_tokenize(summary_text) if s.strip()]

    # Guard: OpenAI's embeddings endpoint rejects empty strings outright,
    # and older notes (created before note_text became required) may have
    # blank text — exclude those from evidence-linking entirely.
    note_list = [n for n in notes if n.note_text and n.note_text.strip()]

    if not summary_sentences or not note_list:
        return []

    # Get embeddings for every summary sentence and every source note in one batch
    texts_to_embed = summary_sentences + [n.note_text for n in note_list]
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=texts_to_embed,
    )
    all_embeddings = [item.embedding for item in response.data]

    summary_embeddings = all_embeddings[:len(summary_sentences)]
    note_embeddings = all_embeddings[len(summary_sentences):]

    def cosine_similarity(a, b):
        a, b = np.array(a), np.array(b)
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

    evidence_links = []
    for sentence, sent_emb in zip(summary_sentences, summary_embeddings):
        similarities = [cosine_similarity(sent_emb, note_emb) for note_emb in note_embeddings]
        best_idx = int(np.argmax(similarities))
        best_note = note_list[best_idx]

        evidence_links.append({
            'summary_sentence': sentence,
            'matched_note_id': best_note.id,
            'matched_note_date': best_note.created_at.strftime('%d %b %Y %H:%M'),
            'matched_note_category': best_note.get_category_display(),
            'matched_note_text': best_note.note_text,
            'similarity': round(similarities[best_idx], 4),
        })

    return evidence_links