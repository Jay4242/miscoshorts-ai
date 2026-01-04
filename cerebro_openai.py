import os
import openai
from openai import OpenAI
import re

# Base URL for OpenAI API (adjust as needed). Note: Ollama typically runs on port 11343, LMStudio on 1234, and llama.cpp's llama-server defaults to 8080.
BASE_URL = os.getenv("OPENAI_BASE_URL", "http://localhost:9090/v1")

# Configure OpenAI API key from environment variable
api_key = os.getenv("OPENAI_API_KEY", "none")
openai.api_key = api_key
client = OpenAI(base_url=BASE_URL, api_key=api_key)

MODEL_NAME = "qwen3:30b"

def encontrar_clip_viral(segmentos_whisper):
    """Consult OpenAI model to find the best viral short segment."""
    print(f"✨ Consulting {MODEL_NAME} (with timestamps)...")

    # Accept either a list of segment dicts or an SRT string
    if isinstance(segmentos_whisper, str):
        # Remote Whisper API returned SRT text
        segmentos = _parse_srt(segmentos_whisper)
    else:
        # Local Whisper library returned list of segment dicts
        segmentos = segmentos_whisper

    # Build timestamped transcription text
    texto_con_tiempos = ""
    for seg in segmentos:
        texto_con_tiempos += f"[{seg['start']:.1f}s] {seg['text']}\n"

    # Prompt for the model (same as Gemini version)
    prompt = f"""
    Actúa como editor de video profesional. Analiza esta transcripción timestamped.
    Identifica EL MEJOR segmento para un Short viral (30-60 seg).

    Transcripción:
    {texto_con_tiempos}

    Responde SOLO con este formato exacto (sin explicaciones extra):
    TITULO: [Escribe un título gancho aquí]
    INICIO: [Solo el número del segundo, ej: 120.5]
    FIN: [Solo el número del segundo, ej: 155.0]
    RAZON: [Breve motivo]
    """

    # Call OpenAI ChatCompletion API
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    # Return the model's text response
    return response.choices[0].message.content
def _parse_srt(srt_text: str):
    """
    Parse a simple SRT string into a list of segments.
    Each segment is a dict with ``start`` (seconds as float) and ``text``.
    """
    segments = []
    # Split on double newlines to get each block
    blocks = [b.strip() for b in srt_text.strip().split("\n\n") if b.strip()]
    timestamp_pattern = re.compile(r"(\d{2}):(\d{2}):(\d{2}),(\d{3})")
    for block in blocks:
        lines = block.splitlines()
        if len(lines) < 2:
            continue
        # lines[1] should be the timestamp line: "00:00:00,000 --> 00:00:03,600"
        match = timestamp_pattern.search(lines[1])
        if not match:
            continue
        hours, minutes, seconds, millis = map(int, match.groups())
        start_seconds = hours * 3600 + minutes * 60 + seconds + millis / 1000.0
        # The rest of the lines after the timestamp are the subtitle text
        text = " ".join(lines[2:]).strip()
        segments.append({"start": start_seconds, "text": text})
    return segments
