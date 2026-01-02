# AI YouTube Shorts Generator

AI-powered tool to automatically generate engaging YouTube Shorts from long-form videos. Uses **Google Gemini 3 Pro Preview** and **Whisper** to extract highlights, add subtitles, and crop videos vertically for social media.

![longshorts](https://github.com/user-attachments/assets/3f5d1abf-bf3b-475f-8abf-5e253003453a)

## Features

- **🎬 Flexible Input**: Supports both YouTube URLs and local video files
- **🤖 Gemini Pro 3 Powered**: Uses `gemini-3-pro-preview` for high-quality highlight selection
- **📝 Custom Subtitles**: Supports `text.md` as subtitle source (10s segments) with automatic formatting
- **🔗 Source Credits**: Automatically adds original video title and link as a permanent footer
- **🎤 Multi-language Transcription**: Auto-detects language (including Korean) using Whisper
- **🎯 Smart Cropping**: 
  - **Face videos**: Static face-centered crop
  - **Screen recordings**: Half-width display with smooth motion tracking
- **📱 Vertical Format**: Perfect 9:16 aspect ratio for TikTok/YouTube Shorts/Instagram Reels
- **⚙️ Automation Ready**: 720p default resolution, 5s/15s auto-timeouts for hands-free processing
- **📦 Organized Output**: Final results are moved to the `out/` folder, and original files are cleaned up automatically

## Installation

### Prerequisites

- Python 3.12+ (Recommended: 3.12.11)
- FFmpeg
- ImageMagick (Required for subtitles)
- Google Gemini API Key (or OpenAI API Key)

### Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SamurAIGPT/AI-Youtube-Shorts-Generator.git
   cd AI-Youtube-Shorts-Generator
   ```

2. **Install system dependencies:**
   
   **macOS:**
   ```bash
   brew install ffmpeg imagemagick
   ```
   
   **Linux:**
   ```bash
   sudo apt install -y ffmpeg imagemagick
   ```

3. **Create and activate virtual environment:**
   ```bash
   python3.12 -m venv venv
   source venv/bin/activate
   ```

4. **Install Python dependencies:**
   
   **macOS:**
   ```bash
   pip install -r requirements_macos.txt
   ```
   
   **Windows/Linux:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   
   Create a `.env` file in the project root:
   ```bash
   # Gemini (Preferred)
   GOOGLE_API_KEY=your_google_api_key_here
   
   # Or OpenAI
   OPENAI_API=your_openai_api_key_here
   ```

## Usage

### Using `text.md` for Subtitles
Prepare a `text.md` file in the project root with numbered segments. Each segment will be displayed for 10 seconds.
```markdown
1. 첫 번째 자막 내용입니다.
2. 두 번째 자막 내용입니다.
```

### Run the Generator
```bash
./run.sh "https://www.youtube.com/watch?v=VIDEO_ID"
```

## How It Works

1. **Download**: Fetches from YouTube or loads local file.
2. **Resolution**: Defaults to **720p** if no input is provided in 5s.
3. **Analyze**: Gemini Pro 3 reads `text.md` (or audio transcription) to find the best highlight.
4. **Interactive Approval**: 15s timeout for auto-approval.
5. **Smart Crop**: Detects faces or tracks motion for 9:16 vertical format.
6. **Subtitles**:
   - **Top**: Displays `text.md` content (10s each).
   - **Bottom**: Displays original video title and URL as source credit.
7. **Cleanup**: Moves final video and `text.md` to `out/` folder and deletes the original heavy video file.

## Configuration

### Subtitle Styling
Edit `Components/Subtitles.py`:
- **Font**: `font='AppleGothic'` (macOS Korean support)
- **Position**: Top (100px margin)
- **Footer**: Bottom (60px margin, 20px size)

### Highlight Selection
Edit `Components/LanguageTasks.py`:
- **Model**: `model="gemini-3-pro-preview"`
- **Temperature**: `1.0`

## Output Files

Final results are stored in the **`out/`** directory:
- Video: `{video-title}_{session-id}_short.mp4`
- Metadata: `{video-title}_{session-id}.md` (Moved from `text.md`)

## Troubleshooting

### No Subtitles
Ensure ImageMagick is installed and configured. On Linux, you may need to fix the policy:
```bash
sudo sed -i 's/rights="none" pattern="@\*"/rights="read|write" pattern="@*"/' /etc/ImageMagick-6/policy.xml
```

### Model Not Found
If `gemini-3-pro-preview` is not available, update the model name in `Components/LanguageTasks.py` to `gemini-1.5-pro` or `gemini-2.0-flash-exp`.

## License

MIT License.
