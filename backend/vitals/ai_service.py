import json
from openai import OpenAI
from django.conf import settings

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


def extract_vitals_from_transcript(transcript: str) -> dict:
    """Use GPT to parse vitals from a free-form transcript."""
    
    prompt = f"""
You are a clinical data extraction assistant. Extract vital signs from this nurse/carer recording.

Transcript: "{transcript}"

Return ONLY valid JSON (no explanation) with these exact keys. Use null if not mentioned:
{{
  "temperature": <float in °C or null>,
  "bp_systolic": <int mmHg or null>,
  "bp_diastolic": <int mmHg or null>,
  "heart_rate": <int bpm or null>,
  "respiratory_rate": <int breaths/min or null>,
  "oxygen_saturation": <float % or null>,
  "blood_glucose": <float mmol/L or null>,
  "weight_kg": <float or null>,
  "pain_score": <int 0-10 or null>,
  "notes": "<any clinical observations not captured above, or empty string>"

}}

Examples of phrases to recognise:
- "temp 37.2" → temperature: 37.2
- "BP 120 over 80" → bp_systolic: 120, bp_diastolic: 80
- "sats 98" → oxygen_saturation: 98.0
- "heart rate 72", "pulse 72" → heart_rate: 72
- "resps 16", "respiratory rate 16" → respiratory_rate: 16
- "BM 5.5", "blood sugar 5.5" → blood_glucose: 5.5
- "pain score 3 out of 10" → pain_score: 3
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",  # cheap and fast; use gpt-4o for better accuracy
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )
    
    raw = response.choices[0].message.content.strip()
    # Strip markdown code fences if present
    raw = raw.replace("```json", "").replace("```", "").strip()
    
    return json.loads(raw)
   

