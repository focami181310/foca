import message_worker as mw
from speech_to_text.voice_text import get_voice_text
import os
from vision import img_in_message as im
from speech_to_text.voice_text import get_voice_text

user_name = os.getenv("USER_NAME")

def skip_user():
    response = mw.send_message()
    return response

def user_voice_msg():
    message = "[Голосовое сообщение]" + get_voice_text()
    print(f"{user_name}: {message}")
    mw.add_message("user", user_name, message)
    response = mw.send_message()
    return response

def user_image_msg():
    img_text = input(f"{user_name}: ")
    if img_text == "/v":
        img_text = "[Голосовое сообщение]" + get_voice_text()
        print(f"{user_name}: {img_text}")
    img_path = input("Image path: ")
    im.add_img("user",user_name,img_text,img_path)
    response = mw.send_message()
    return response

COMMANDS={
    "": skip_user,
    "/v": user_voice_msg,
    "/i": user_image_msg,
}


