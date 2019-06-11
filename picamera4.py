from picamera import PiCamera
from time import sleep
import datetime
from gpiozero import LED, Button
import io
import os
from gtts import gTTs

camera = PiCamera()

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

#setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
ready_led = LED(17)
processing_led = LED(18)
on_led = LED(19)
camera_button = Button(2)
more_info_button = Button(3)

# Default message just in case someone presses the other button first
read_aloud_text = ["No pictures have been taken yet", "", "", "", "", ""]

# Display a light to let user know the camera is on
on_led.on()

# Start the camera
camera.resolution = (1600, 1200)
camera.start_preview()
sleep(2)  # camera must preview for 2 seconds to adjust to light levels

# Display ready LED to let user know they can take pictures
ready_led.on()


def google_vision(file_name):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join((os.path.dirname(__file__), 'resources/{file_name}.jpg').format(file_name=file_name))

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


def picture_loop():
    file_name = camera.capture(('/resources/{the_time}.jpg').format(the_time=current_time())) #takes the picture & saves it

    processing_led.blink(on_time=0.2,off_time=0.2,n=None,background=True) # start processing LED flashing

    labels = google_vision(file_name)

    processing_led.off()

    # Process the output from google vision
    read_aloud_text = []
    for label in labels['labelAnnotations']:
        percentage_score = int(label['score'] * 100)
        description = label['description']
        text = (('{description} at {percentage_score} percent').format(description=description, percentage_score=percentage_score))
        read_aloud_text.append(text)
        for item in read_aloud_text[0:5]:
            print(item)

    text_to_speech(read_aloud_text[0])


def read_list_of_text():
    for item in read_aloud_text[0:5]:
        text_to_speech(item)


def text_to_speech(text_to_read):
    #todo
    print("==========================================")
    print(text_to_read)
    tts = gTTS(text=text_to_read, lang='en')
    tts.save("read_aloud.mp3")
    os.system("mpg321 read_aloud.mp3") # mpg321 is a command line mp3 player


# start the main loop
def main():
    while True:
        camera_button.when_pressed = picture_loop()
        more_info_button.when_pressed = read_list_of_text()
        sleep(0.001)


if __name__ == '__main__':
    main()

