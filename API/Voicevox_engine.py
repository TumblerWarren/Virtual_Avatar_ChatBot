import os
from tqdm import tqdm
import sys
import requests
import zipfile

def download_voicevox():
    is_cuda_available = os.environ.get("CUDA_STATUS")

    if is_cuda_available == 'True':
        download_url = r"https://github.com/VOICEVOX/voicevox/releases/download/0.14.7/voicevox-windows-directml-0.14.7.zip"
    else:
        download_url = r"https://github.com/VOICEVOX/voicevox/releases/download/0.14.7/voicevox-windows-cpu-0.14.7.zip"

    response = requests.get(download_url)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024  # 1 KB


    if response.status_code == 200:
        with open(f"voicevox.zip", "wb") as file, tqdm(desc="Downloading Voicevox",total=total_size,unit="B", unit_scale=True, unit_divisor=1024,) as progress_bar:
            for data in response.iter_content(block_size):
                file.write(data)
                progress_bar.update(len(data))
                sys.stdout.flush()
        print(f"Voicevox downloaded successfully.")
    else:
        print("Failed to download Voicevox.")


def extract_zip(file_path, extract_to):
    with zipfile.ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"Extracted contents to {extract_to}")

def main():
    zip_file_path = "voicevox.zip"
    download_successful = download_voicevox()
    extract_to_folder = "."  # Change this to the desired extraction folder
    extract_zip(zip_file_path, extract_to_folder)
    os.remove(zip_file_path)  # Remove the downloaded ZIP file after extraction

if __name__ == "__main__":
    main()

