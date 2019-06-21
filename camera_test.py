from picamera import PiCamera
from time import sleep
import os
from datetime import datetime
import io

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

#Import modules for text to speech
from gtts import gTTS

camera = PiCamera()

# Start the camera
camera.resolution = (1600, 1200)
camera.start_preview()
sleep(2)  # camera must preview for 2 seconds to adjust to light levels

def picture_loop():
    # Start the camera
    # camera.resolution = (1600, 1200)
    # camera.start_preview()
    # sleep(2)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(current_time)
    file_path = "/home/pi/resources/" + current_time + ".jpg"
    print(file_path)
    camera.capture(file_path)

    # Send file path to google vision
    labels = google_vision(file_path)
    for label in labels:
        print(label.description)

    # Send labels to text to speech
    for label in labels:
        text_to_speech(label.description)

def google_vision(file_name):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations
    # print('Labels:')
    # for label in labels:
    #     print(label.description)
    return labels


def text_to_speech(text_to_read):
    #todo
    print("==========================================")
    print(text_to_read)
    tts = gTTS(text=text_to_read, lang='en')
    tts.save("read_aloud.mp3")
    os.system("mpg321 read_aloud.mp3") # mpg321 is a command line mp3 player


def main():
    while True:
        temp_variable = input("Press Y to take picture: ")

        if temp_variable == "Y" or "y":
            picture_loop()
        else:
            sleep(5)

if __name__ == '__main__':
    main()
