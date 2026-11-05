"""Generates Miss Circle's voice lines: Google Translate TTS (Japanese voice reading English text) -> OGG Vorbis in assets/fpe/sounds/miss_circle/.
Needs network + `pip install soundfile numpy`. Re-run only if you want to change the lines."""
import json, os, subprocess, urllib.parse, io
import soundfile as sf
LINES = {
    "you_failed": "You failed", "wrong": "Wrong answer", "detention": "Detention", "zero": "Zero points", "sit_down": "Sit down",
    "pop_quiz": "Pop quiz", "do_math": "Do the math", "try_again": "Try again", "class_dismissed": "Class dismissed", "late": "You are late",
    "fail3": "Fail, fail, fail", "perfect": "Perfect circle", "come_here": "Come here", "confiscated": "Confiscated", "hurt": "Ugh", "death": "Class is over",
}
OUT = os.path.join(os.path.dirname(__file__), "..", "src/main/resources/assets/fpe/sounds/miss_circle")
os.makedirs(OUT, exist_ok=True)
events = {}
for k, text in LINES.items():
    url = "https://translate.google.com/translate_tts?ie=UTF-8&tl=ja&client=tw-ob&q=" + urllib.parse.quote(text)
    mp3 = subprocess.run(["curl", "-s", "-m", "30", "-A", "Mozilla/5.0", url], capture_output=True, check=True).stdout
    data, sr = sf.read(io.BytesIO(mp3))
    sf.write(os.path.join(OUT, k + ".ogg"), data, sr, format="OGG", subtype="VORBIS")
    events["miss_circle." + k] = {"sounds": [{"name": "fpe:miss_circle/" + k}]}
    print(k, len(data) / sr)
json.dump(events, open(os.path.join(OUT, "..", "..", "sounds.json"), "w"), indent=1)
