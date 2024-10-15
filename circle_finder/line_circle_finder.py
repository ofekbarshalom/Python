import mss
import cv2
import numpy as np
import keyboard

sct = mss.mss()

# Create a named window to display the image
cv2.namedWindow("Circles / Lines Detected", cv2.WINDOW_NORMAL)

while not keyboard.is_pressed('q'):
    # Grab the screen
    scr = sct.grab({
        'left': 5,
        'top': 50,
        'width': 405,
        'height': 680,
    })

    # Convert the captured image to a NumPy array
    img = np.array(scr)

    # Convert from BGRA to BGR (OpenCV uses BGR format)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    gray = cv2.GaussianBlur(gray, (5, 5), 2)

    # Apply Canny edge detection with lower thresholds for weaker edges
    edges = cv2.Canny(gray, 30, 100)

    # Define a mask to limit the region of interest
    mask = np.zeros_like(edges)
    # Create a polygon mask (you can adjust the points based on your game's region)
    polygon = np.array([[
        (0, 680), (0, 100), (415, 100), (415, 680)
    ]], np.int32)
    cv2.fillPoly(mask, polygon, 255)

    # Apply the mask to the edges
    masked_edges = cv2.bitwise_and(edges, mask)

    # Apply Hough Circle Transform with adjusted parameters
    circles = cv2.HoughCircles(
        gray,
        cv2.HOUGH_GRADIENT,
        dp=1,  # Resolution of the accumulator
        minDist=20,  # Minimum distance between detected centers
        param1=50,  # Upper threshold for the Canny edge detector
        param2=15,  # Accumulator threshold for the circle centers (lower for more sensitivity)
        minRadius=5,  # Reduced minimum circle radius to detect the ball
        maxRadius=15  # Increased maximum circle radius to cover different ball sizes
    )

    # Apply Hough Line Transform with modified parameters for track detection
    HoughLines = cv2.HoughLinesP(
        masked_edges,
        1,
        np.pi / 180,
        threshold=100,  # Threshold to detect stronger lines
        minLineLength=80,  # Detect only longer lines (the track)
        maxLineGap=10  # Allow small gaps between line segments
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

    # Check if lines were found
    if HoughLines is not None:
        print("Line found")
        for line in HoughLines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)

    else:
        print("No lines found.")

    # Show the image with detected circles and lines
    cv2.imshow("Circles / Lines Detected", img)
    cv2.resizeWindow("Circles / Lines Detected", 415, 680)

    # Check for key press to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up and close windows
cv2.destroyAllWindows()
