from picamera import PiCamera
from time import sleep
import os
from datetime import datetime

camera = PiCamera()

# Start the camera
camera.resolution = (1600, 1200)
camera.start_preview()
sleep(2)  # camera must preview for 2 seconds to adjust to light levels

def picture_loop():
    # Start the camera
    camera.resolution = (1600, 1200)
    camera.start_preview()
    sleep(2)

    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(current_time)
    file_path = "/home/pi/resources/" + current_time + ".jpg"
    print(file_path)
    camera.capture(file_path)


def main():
    while True:
        temp_variable = input("Press Y to take picture: ")

        if temp_variable == "Y" or "y":
            picture_loop()
        else:
            sleep(5)

if __name__ == '__main__':
    main()
