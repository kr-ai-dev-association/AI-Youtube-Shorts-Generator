from faster_whisper import WhisperModel
import torch

def transcribeAudio(audio_path):
    try:
        print("Transcribing audio...")
        Device = "cuda" if torch.cuda.is_available() else "cpu"
        print(Device)
        model = WhisperModel("base", device="cuda" if torch.cuda.is_available() else "cpu")
        print("Model loaded")
        # language=None으로 설정하면 자동으로 언어를 감지합니다.
        segments, info = model.transcribe(audio=audio_path, beam_size=5, language=None, condition_on_previous_text=False)
        segments = list(segments)
        # print(segments)
        extracted_texts = [[segment.text, segment.start, segment.end] for segment in segments]
        print(f"✓ Transcription complete: {len(extracted_texts)} segments extracted")
        return extracted_texts
    except Exception as e:
        print("Transcription Error:", e)
        return []

if __name__ == "__main__":
    audio_path = "audio.wav"
    transcriptions = transcribeAudio(audio_path)
    # print("Done")
    TransText = ""

    for text, start, end in transcriptions:
        TransText += (f"{start} - {end}: {text}")
    print(TransText)