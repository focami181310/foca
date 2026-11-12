FOCA v0.1
![logo](logo.png)

Installation:

Linux:

1. Install git
2. Install FFmpeg
3. Clone the repository
4. Setup virtual environment for Python

Using uv:
```
cd foca
```
```
uv venv .venv
```
```
uv pip install --python .venv/bin/python openai python-dotenv pygame pydub sounddevice scipy audioop-lts
```
```
uv run foca.py
```
