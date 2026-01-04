# Miscoshorts - AI-Powered YouTube Shorts Generator

Automatically creates viral YouTube Shorts from long-form videos using AI analysis and automatic subtitle generation.
🎥 **[WATCH YOUTUBE TUTORIAL](https://youtu.be/zukJLVUwMxA?si=_DQ2RG10uzXtt7yT)**

## Features

- 🎥 Downloads YouTube videos automatically
- 🔍 Transcribes audio using Whisper (local or OpenAI‑compatible API)
- 🤖 Analyzes content with Google Gemini to find viral segments
- ✂️ Crops videos to vertical 9:16 format for Shorts
- 📝 Generates automatic subtitles with styling
- 🎬 Creates ready-to-upload MP4 files

## Requirements

- Python 3.12+
- FFmpeg (required by moviepy)
- Google Gemini API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd miscoshorts
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

> **Note:** The `cerebro_openai.py` backend works with any OpenAI‑compatible API (e.g., Ollama, LM Studio, llama.cpp). Set the `OPENAI_BASE_URL` environment variable to the appropriate endpoint (default `http://localhost:9090/v1`). Usually only the port changes (Ollama 11343, LM Studio 1234, llama‑cpp 8080).

3. Install FFmpeg:
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

4. Set up your Google Gemini API key:
   - Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Update the `GEMINI_API_KEY` variable in `cerebro_gemini.py`

5. (Optional) Configure OpenAI‑compatible API backend:
   - Set the `OPENAI_BASE_URL` environment variable to your API endpoint (default `http://localhost:9090/v1`).
   - Example endpoints:
     - Ollama: `http://localhost:11343/v1`
     - LM Studio: `http://localhost:1234/v1`
     - llama.cpp: `http://localhost:8080/v1`
   - If using the remote Whisper server, ensure `USE_WHISPER_API=true` and adjust `api_url` in `subtitulos_whisper.py`.

## Usage

1. Edit the `URL_VIDEO` variable in `maker.py` to point to your target YouTube video
2. Run the script:
```bash
python maker.py
```

3. The script will:
   - Download the video
   - Transcribe the audio
   - Ask Gemini to suggest the best viral segment
   - Show you the suggestion with title, timestamps, and reasoning
   - Ask for confirmation (press 's' to accept or provide custom timestamps)
   - Generate the vertical Short with subtitles
   - Save as `short_con_subs.mp4`

## Configuration

### Video Settings
Edit these variables in `maker.py`:
- `URL_VIDEO`: YouTube video URL to process
- `NOMBRE_SALIDA`: Output filename (default: "short_con_subs.mp4")

### Subtitle Styling
Edit subtitle appearance in `subtitulos.py`:
- Font: `DejaVuSans-Bold` (change to any available system font)
- Font size: `70`
- Color: `yellow` with black stroke
- Position: Centered

### AI Analysis
Edit the prompt in `cerebro_gemini.py` to customize how Gemini analyzes videos for viral potential.

## Output Files

- `short_con_subs.mp4`: Final vertical Short with subtitles
- `transcripcion_completa.txt`: Full transcription with timestamps
- `video_temp.mp4`: Temporary downloaded video (auto-deleted)

## Troubleshooting

### Font Issues
If you encounter font errors, try these alternatives:
- `'LiberationSans-Bold'`
- `'Arial-Bold'` 
- `'Ubuntu-Bold'`

Or install fonts:
```bash
sudo apt install fonts-dejavu-core fonts-liberation
```

### MoviePy Issues
Ensure FFmpeg is installed and in your PATH:
```bash
ffmpeg -version
```

### Whisper Issues
The script uses `openai-whisper`. If you have the wrong whisper package:
```bash
pip uninstall whisper
pip install openai-whisper
```

> **Tip:** To use a remote Whisper server, set `USE_WHISPER_API=true` (default) and point `api_url` in `subtitulos_whisper.py` to the server’s endpoint (e.g., `http://localhost:9191/inference`). The server should return SRT compatible with the script.

### Gemini API Issues
- Make sure your API key is valid
- Check that you're using the correct model name (`gemini-2.5-flash`)
- Monitor your API usage to avoid rate limits

## File Structure

```
miscoshorts/
├── maker.py              # Main script
├── cerebro_gemini.py     # Gemini AI analysis
├── subtitulos.py         # Subtitle generation
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## Dependencies

- `yt-dlp`: YouTube video downloading
- `openai-whisper`: Audio transcription
- `moviepy`: Video editing and processing
- `google-generativeai`: Gemini AI API
- `torch`: Deep learning (Whisper dependency)
- `PIL`: Image processing (MoviePy dependency)

## Author / Resources

Si este código te ha servido, profundizar en la lógica detrás de la IA es lo que te diferenciará como ingeniero. Echa un vistazo a mis libros:

- 📖 Explora la Inteligencia Artificial: https://amzn.eu/d/dSwYhue
- 💻 Programar con Inteligencia Artificial: https://amzn.eu/d/eK4f73N
- Canal de YouTube: https://www.youtube.com/@jokioki?sub_confirmation=1


## License

MIT License - feel free to use and modify for your projects.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Tips for Best Results

1. **Choose videos with clear audio** - Whisper works best with clean speech
2. **Look for moments with strong reactions** - Gemini identifies these as viral potential
3. **Keep segments 30-60 seconds** - Ideal for Shorts attention spans
4. **Ensure good lighting and clear visuals** - Important for vertical format
5. **Test different subtitle styles** - Adjust colors and fonts for your brand
