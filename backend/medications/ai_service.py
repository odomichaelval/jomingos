import json
from openai import OpenAI
from django.conf import settings
from medications.models import Medication  # adjust import path to match your app name

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


# Derived dynamically from the model — single source of truth
VALID_ROUTES = [key for key, _ in Medication.ROUTE_CHOICES]
VALID_MED_TYPES = [key for key, _ in Medication.MED_TYPE_CHOICES]


def extract_medication_from_transcript(transcript: str) -> dict:
    """Use GPT to parse a medication administration record from a free-form transcript."""

    prompt = f"""
You are a clinical data extraction assistant. Extract medication administration details from this nurse/carer recording.

Transcript: "{transcript}"

Return ONLY valid JSON (no explanation) with these exact keys. Use null if not mentioned or unclear:
{{
  "drug_name": "<name of the drug, or null>",
  "dosage": "<dosage as stated, e.g. '500mg', or null>",
  "route": "<MUST be exactly one of: {VALID_ROUTES} or null>",
  "med_type": "<MUST be exactly one of: {VALID_MED_TYPES} or null>",
  "reason": "<reason/indication if mentioned, or null>",
  "witnessed_by": "<name of witness if mentioned, or null>",
  "notes": "<any other clinical observations not captured above, or empty string>"
}}

Drug name recognition guide (people rarely say "drug name" literally — recognise the intent from natural phrasing):
- "the medicine I gave is Paracetamol" → drug_name: "Paracetamol"
- "I gave her Amoxicillin" / "gave him some Ibuprofen" → drug_name: "Amoxicillin" / "Ibuprofen"
- "administered Morphine" / "medication given was Metformin" → drug_name: "Morphine" / "Metformin"
- "patient was given 500mg of Paracetamol" → drug_name: "Paracetamol", dosage: "500mg"
- "started her on Warfarin" / "put him on Aspirin" → drug_name: "Warfarin" / "Aspirin"
- "witnessed by California" / "witness was California" → witnessed_by: "California"
- "California witnessed it" → witnessed_by: "California"
- If a dosage number is stated right next to a drug-sounding word (e.g. "10mg of X"), treat X as the drug name even without an explicit verb like "gave" or "administered".
- Only extract a drug name if one is clearly named. Do not guess or invent a name if none is mentioned.

Route mapping guide (map what's said to the exact key):
- "orally", "by mouth", "PO" → "oral"
- "IV", "intravenous", "into the vein" → "iv"
- "IM", "intramuscular", "into the muscle" → "im"
- "subcut", "subcutaneous", "under the skin" → "sc"
- "topical", "applied to the skin", "cream" → "topical"
- "inhaled", "inhaler", "nebulizer" → "inhaled"
- "sublingual", "under the tongue" → "sublingual"
- "rectal", "suppository" → "rectal"
- "nasal", "nasal spray" → "nasal"

Type mapping guide:
- "regular", "scheduled", "routine dose" → "regular"
- "PRN", "as required", "as needed" → "prn"
- "STAT", "immediately", "right away" → "stat"
- "TTO", "to take out", "discharge meds" → "tto"

IMPORTANT: If the transcript doesn't clearly indicate a route or type from the lists above, return null for that field. Do NOT guess, default, or invent a value outside the allowed list — and do NOT pick the closest-sounding or most common option as a fallback if the spoken word doesn't clearly match. It is better to return null than to guess incorrectly.

Example of what NOT to do:
- "the route was Chedema" → "Chedema" is not a real route → route: null (NOT "oral")
- "the type was ABC" → "ABC" is not a real type → med_type: null (NOT "regular")

Examples:
- "Gave paracetamol 500mg orally, regular dose" → drug_name: "Paracetamol", dosage: "500mg", route: "oral", med_type: "regular"
- "The medicine I gave is Morphine, 10mg IV, stat for pain" → drug_name: "Morphine", dosage: "10mg", route: "iv", med_type: "stat", reason: "pain"
- "Started her on Amoxicillin 250mg by mouth, regular" → drug_name: "Amoxicillin", dosage: "250mg", route: "oral", med_type: "regular"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()
    raw = raw.replace("```json", "").replace("```", "").strip()
    data = json.loads(raw)

    # Defense in depth: enforce the allowed values ourselves, don't trust GPT blindly
    if data.get('route') not in VALID_ROUTES:
        data['route'] = None
    if data.get('med_type') not in VALID_MED_TYPES:
        data['med_type'] = None

    return data