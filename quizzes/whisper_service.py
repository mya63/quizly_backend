import whisper


def transcribe_audio(audio_path):
    """
    Transcribes an audio file using the Whisper model.

    Args:
        audio_path (str): Path to the audio file.

    Returns:
        str: Transcribed text from the audio file.
    """
    # NEU: Modell wird erst hier geladen
    model = whisper.load_model("base")

    result = model.transcribe(audio_path)
    return result["text"]