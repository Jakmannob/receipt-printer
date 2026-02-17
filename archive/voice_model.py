import json
import os
import queue
import shutil
import urllib.request
import zipfile

import sounddevice as sd
from vosk import KaldiRecognizer, Model
from zahlwort2num import convert

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

INPUT_DEVICE_ID = 7
MODEL_INSTALL_DIR = "model"
VOSK_MODEL_DL_LINK = "https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip"
# Introduces a short delay after voice command was processed
WAIT_FOR_AUDIO = True

if INPUT_DEVICE_ID < 0:
    print(
        "You need to set your INPUT_DEVICE_ID at the start of the script. "
        "Run print_mic_ids.py to list possible mics."
    )
    exit(1)


def model_name():
    return ".".join(VOSK_MODEL_DL_LINK.split("/")[-1].split(".")[:-1])


def model_path():
    return os.path.join(MODEL_INSTALL_DIR, model_name())


def check_install():
    print("Checking for existing model install...")
    os.makedirs(MODEL_INSTALL_DIR, exist_ok=True)
    if os.path.isdir(model_path()):
        print("Model already downloaded and installed")
        return
    print("No existing install found")
    install_model()


def install_model():
    print("Installing model...")
    zip_path = model_path() + ".zip"
    urllib.request.urlretrieve(VOSK_MODEL_DL_LINK, zip_path)
    with zipfile.ZipFile(zip_path, "r") as extract_file:
        extract_file.extractall(path=model_path())

    # Fix nested extract
    if model_name() in os.listdir(model_path()):
        shutil.move(model_path(), model_path() + ".bak")
        shutil.move(os.path.join(model_path() + ".bak", model_name()), model_path())
        os.rmdir(model_path() + ".bak")


def try_parse_number(text):
    """Parses a number if possible, returns the original text otherwise

    Args:
        text (str): The input text

    Returns:
        str: The parsed number, converted back to str
    """
    if text is None or len(text.strip()) == 0:
        return ""
    try:
        number = convert("".join(text.split(" ")))
    except ValueError:
        return text
    return str(number)


if __name__ == "__main__":
    check_install()
    model = Model(model_path())
    q = queue.Queue()

    def callback(indata, frames, timestamp, status):
        q.put(bytes(indata))

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback,
        device=INPUT_DEVICE_ID,
    ):
        print("Listening...")
        rec = KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                text = json.loads(rec.Result()).get("text", "")

                print(f"You said: {try_parse_number(text)}")
