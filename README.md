FOCA v0.1.1
![logo](logo.png)

FOCA is an AI architecture that connects several AI API into one personal AI companion.
Currently FOCA can have long term memory, voice and vision.

What FOCA will have in future (hopefully):
1) webui
2) asyncio
3) 2D body
4) modular memory
5) ability to write message first
6) to-do list/calendar maintaining
7) 24/7 subconscious


Installation:
1. Install git
2. Install FFmpeg (and add it to PATH or insert FFmpeg path into .env)
3. Install uv
4. Clone the repository

```
git clone https://github.com/focami181310/foca.git
```

5. Setup virtual environment for Python

```
cd foca
```
```
uv venv .venv
```
```
uv pip install -r requirements.txt
```

6. Rename .env.example to .env and fill it
7. Fill data/memory/system_prompt.json file with your character prompt
8. Run foca.py

```
uv run foca.py
```

You can use commands: 
/v - to send voice message
/i - to send message with image 
/mute @foca - to turn off Foca's voice
/unmute @foca - to turn on Foca's voice 
/exit - to exit the program

Enjoy.

