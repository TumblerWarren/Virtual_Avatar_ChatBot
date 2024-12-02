import torch
from transformers.models.speecht5.number_normalizer import EnglishNumberNormalizer
from string import punctuation
import re
import soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer, AutoFeatureExtractor, set_seed
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
FILENAME = "local_tts_output.mp3"
OUTPUT_PATH = os.path.join(current_directory, "resource", "voice_out", FILENAME)

# Check if GPU is available and set device
device = "cuda:0" if torch.cuda.is_available() else "cpu"

# Load model, tokenizer, and feature extractor
repo_id = "parler-tts/parler-tts-mini-expresso"
model = ParlerTTSForConditionalGeneration.from_pretrained(repo_id).to(device)
tokenizer = AutoTokenizer.from_pretrained(repo_id)
feature_extractor = AutoFeatureExtractor.from_pretrained(repo_id)

# Constants
SAMPLE_RATE = feature_extractor.sampling_rate
SEED = 42

# Preprocessing function
number_normalizer = EnglishNumberNormalizer()


def preprocess(text):
    text = number_normalizer(text).strip()
    if text[-1] not in punctuation:
        text = f"{text}."

    abbreviations_pattern = r'\b[A-Z][A-Z\.]+\b'

    def separate_abb(chunk):
        chunk = chunk.replace(".", "")
        return " ".join(chunk)

    abbreviations = re.findall(abbreviations_pattern, text)
    for abv in abbreviations:
        if abv in text:
            text = text.replace(abv, separate_abb(abv))
    return text


# TTS generation function
def voice_generation(text):
    description = "Elisabeth speaks happily at a slightly slower than average pace with high quality audio."
    inputs = tokenizer(description, return_tensors="pt").to(device)
    prompt = tokenizer(preprocess(text), return_tensors="pt").to(device)

    set_seed(SEED)
    generation = model.generate(input_ids=inputs.input_ids, prompt_input_ids=prompt.input_ids)
    audio_arr = generation.cpu().numpy().squeeze()

    # Save the generated audio
    sf.write(OUTPUT_PATH, audio_arr, SAMPLE_RATE)
    return OUTPUT_PATH


