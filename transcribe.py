from pydub import AudioSegment
import librosa
import os
import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import numpy as np
from pyannote.audio import Pipeline


pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                    use_auth_token="_____________R")

pipeline.to(torch.device("cuda"))


# Configuring device and data types for PyTorch
device = "cuda" if torch.cuda.is_available() else "cpu"
torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

# Load and setup the Whisper model
model_id = "openai/whisper-large-v3"
model = AutoModelForSpeechSeq2Seq.from_pretrained(
    model_id, torch_dtype=torch_dtype, use_safetensors=True, cache_dir='./model'
)
model.to(device)
processor = AutoProcessor.from_pretrained(model_id)
pipe = pipeline(
    "automatic-speech-recognition",
    model=model,
    tokenizer=processor.tokenizer,
    feature_extractor=processor.feature_extractor,
    max_new_tokens=128,
    chunk_length_s=30,
    batch_size=16,
    return_timestamps=True,
    torch_dtype=torch_dtype,
    device=device,
)


# Function to transcribe audio
def transcribe(sr, data):
    processed_data = np.array(data).astype(np.float32)
    results = pipe(processed_data, generate_kwargs={"language": "russian"})["text"]
    return results


# Convert MP3 to WAV
output_file = "converted_audio.wav"
diarization = pipeline(output_file, min_speakers=2, max_speakers=5)
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
# Load the WAV file
data, sr = librosa.load(output_file, sr=16000)

# Setup diarization
# diarization_pipeline = PyannotePipeline.from_pretrained("pyannote/speaker-diarization")
# diarization = diarization_pipeline(output_file)

# Process each identified speaker segment
for turn, _, speaker in diarization.itertracks(yield_label=True):
    segment = data[int(turn.start * sr): int(turn.end * sr)]
    transcription = transcribe(sr, segment)
    print(f"Speaker {speaker} time: {turn.start:.1f}s to {turn.end:.1f}s: {transcription}")
