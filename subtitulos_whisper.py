import requests

def transcribe_and_save(
    video_path: str,
    url_video: str,
    use_api: bool = True,
    api_url: str = "http://localhost:9191/inference",
):
    """
    Transcribe the audio of the given video using either the local Whisper model
    or a remote Whisper API.

    Parameters
    ----------
    video_path: str
        Path to the local video file.
    url_video: str
        Original video URL (used only for logging in the output file).
    use_api: bool, optional
        If True, send the video to a remote Whisper inference server.
        If False (default), use the local ``whisper`` library.
    api_url: str, optional
        URL of the remote Whisper inference endpoint.

    Returns
    -------
    dict
        Whisper‑style transcription result dictionary containing at least
        ``text`` and optionally ``segments``.
    """
    if use_api:
        # Remote transcription via HTTP POST
        with open(video_path, "rb") as f:
            files = {"file": (video_path, f, "application/octet-stream")}
            response = requests.post(api_url, files=files, timeout=3600)
            response.raise_for_status()
            # Assume the remote service returns JSON compatible with Whisper output
            try:
                result = response.json()
            except ValueError:
                # Fallback: treat raw text as the transcription
                result = {"text": response.text, "segments": []}
    else:
        # Local transcription using the Whisper library
        import whisper
        model = whisper.load_model("base")
        result = model.transcribe(video_path)

    # Save the full transcription to a text file (same format as before)
    with open("transcripcion_completa.txt", "w", encoding="utf-8") as f:
        f.write(f"URL: {url_video}\n")
        f.write(result.get("text", ""))

    return result
