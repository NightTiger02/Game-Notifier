import time
import cv2
import pygetwindow as gw
import pyautogui
import numpy as np
import webbrowser
from notify_run import Notify
notify = Notify()

def find_image_on_screen(image_path, threshold=0.8):
    try:
        # Capture a screenshot using pyautogui
        screenshot = pyautogui.screenshot()

        # Convert the screenshot to a NumPy array
        screenshot = np.array(screenshot)

        # Convert the color format from RGB to BGR (OpenCV uses BGR)
        screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)

        # Read the image you want to find
        template = cv2.imread(image_path, cv2.IMREAD_COLOR)

        # Perform template matching
        result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)

        # Get the location with highest correlation
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

        if max_val >= threshold:
            return max_loc
        else:
            return None
    except Exception as e:
        print(f"Error finding image: {e}")
        return None


def click_on_image_location(location):
    try:
        # Click on the center of the image location
        pyautogui.click(location[0] + 20, location[1] + 20)
        print("Clicked on the image.")
    except Exception as e:
        print(f"Error clicking on image location: {e}")

def main():
    image_path = 'accept.jpg' # Set the path to the image you want to find

    # Specify the interval (in seconds) between each search
    search_interval = 3
    try:
        while True:
            # Find the image on the screen
            image_location = find_image_on_screen(image_path)

            if image_location is not None:
                print(f"Image found at coordinates: {image_location}")
                click_on_image_location(image_location)
                notify.send('Your game has started!')
            else:
                print("Image not found on the screen.")

            # Wait for the next search
            time.sleep(search_interval)
    except KeyboardInterrupt:
        print("Program terminated by user.")

if __name__ == "__main__":
    main()