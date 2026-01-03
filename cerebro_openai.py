import os
import openai
from openai import OpenAI

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

    # Build timestamped transcription text
    texto_con_tiempos = ""
    for seg in segmentos_whisper:
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
