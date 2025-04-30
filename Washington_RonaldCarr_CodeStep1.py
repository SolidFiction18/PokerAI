import cv2
# Change the index (0, 1, 2...) based on your USB camera
camera_index = 0 # Adjust if needed
# Open a connection to the camera
cap = cv2.VideoCapture(camera_index)
# Check if the camera is opened correctly
if not cap.isOpened():
    print("Error: Could not open camera.")
    #exit()
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    # If the frame is captured correctly, display it
    if ret:
         cv2.imshow("Live Camera Feed", frame)
    else:
         print("Error: Unable to capture video.")
         break
        # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()