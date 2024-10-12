import mss
import cv2
import numpy as np
import keyboard

sct = mss.mss()

# Create a named window to display the image
cv2.namedWindow("Circles / Lines Detected", cv2.WINDOW_NORMAL)  # Keep the window open

while not keyboard.is_pressed('q'):
    # Grab the screen
    scr = sct.grab({
        'left': 0,
        'top': 50,
        'width': 415,
        'height': 680,
    })

    # Convert the captured image to a NumPy array
    img = np.array(scr)

    # Convert from BGRA to BGR (OpenCV uses BGR format)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1,  # Resolution of the accumulator
        minDist=20,  # Minimum distance between detected centers
        param1=50,  # Upper threshold for the Canny edge detector
        param2=18,  # Accumulator threshold for the circle centers
        minRadius=10,  # Minimum circle radius
        maxRadius=14  # Maximum circle radius
    )

    # Check if any circles were found
    if circles is not None:
        circles = np.uint16(np.around(circles))
        print("Circle found")
        for i in circles[0, :]:
            # Draw the outer circle
            cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)

    else:
        print("No circles found.")


    # Show the image with detected circles
    cv2.imshow("Circles / Lines Detected", img)  # Keep this open throughout the loop

    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up and close windows
cv2.destroyAllWindows()
