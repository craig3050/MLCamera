from picamera import PiCamera
from time import sleep
import datetime
from gpiozero import LED, Button
import io
import os
from espeak import espeak

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

def toggle_ready_led(toggle):
    if toggle == "ON":
        ready_led.on()
    else:
        ready_led.off()

def toggle_on_led(toggle):
    if toggle == "ON":
        on_led.on()
    else:
        on_led.off()


def toggle_processing_led(toggle):
    if toggle == "ON":
        processing_led.on()
    else:
        processing_led.off()


def take_the_picture(status):
    if status == "start":
        camera.resolution = (1600, 1200)
        # start the camera
        camera.start_preview()
        sleep(2)  # camera must preview for 2 seconds to adjust to light levels
        return "ready"

    elif status == "take":
        # take the picture then stop the camera
        file_name = camera.capture(f'/resources/{current_time()}.jpg')
        camera.stop_preview()
        return file_name

    else:
        return "failed"


def current_time():
    the_time = datetime.datetime.now()
    return the_time


def process_the_picture(file_name):
    toggle_processing_led("ON")
    returned_labels = google_vision(file_name)
    print(returned_labels)
    print("\n\n\n=============\n\n\n")
    for label in returned_labels:
        print(label.description)

    #TODO return a set of labels with percentage confidence


def google_vision(file_name):
    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = os.path.join(os.path.dirname(__file__),
        f'resources/{file_name}.jpg')

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


def read_aloud_text(text_to_read):
    #TODO read aloud text
    espeak.synth(text_to_read)


def send_description_to_email():
    #TODO email a copy of picture and the description google came up with


def main():
    while True:
        toggle_on_led("ON")
        if camera_button.is_pressed:
            ready_status = take_the_picture("start")
            if ready_status == "ready":
                toggle_ready_led("ON")
                wait_for_picture = True

                while wait_for_picture == True:
                    if camera_button.is_pressed:
                        picture_file_name = take_the_picture("take")
                        picture_contents = process_the_picture(picture_file_name)
                        #TODO send first value to read_aloud_text()
                        toggle_ready_led("OFF")
                        wait_for_picture = False
                    else:
                        sleep(0.1)

            else:
                toggle_ready_led("OFF")
                sleep(0.1)

        if more_info_button.is_pressed:
            try:
                print(picture_contents)
                #TODO list labels and confidence in a string for reading aloud



if __name__ == '__main__':
    main()

