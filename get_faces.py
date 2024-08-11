import cv2
from datetime import datetime
import mediapipe as mp



# Function to crop image around face with fractional margin
def crop_face(image, face_landmarks, margin_fraction=0.5):
    h, w, _ = image.shape
    bbox = face_landmarks.location_data.relative_bounding_box

    # Calculate the bounding box dimensions
    bbox_width = int(bbox.width * w)
    bbox_height = int(bbox.height * h)
    
    # Calculate the margins based on the fraction
    margin_x = int(bbox_width * margin_fraction)
    margin_y = int(bbox_height * margin_fraction)
    
    # Calculate the coordinates for cropping
    x_min = max(int(bbox.xmin * w) - margin_x, 0)
    y_min = max(int(bbox.ymin * h) - margin_y, 0)
    x_max = min(int((bbox.xmin + bbox.width) * w) + margin_x, w)
    y_max = min(int((bbox.ymin + bbox.height) * h) + margin_y, h)
    
    return image[y_min:y_max, x_min:x_max]


def scan_for_faces(margin, confidence, data_dir):
    # Set up MediaPipe Face Detection
    with mp_face_detection.FaceDetection(min_detection_confidence=confidence) as face_detection:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Convert the frame to RGB as MediaPipe works with RGB images
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(rgb_frame)

            # Check if faces are detected
            if results.detections:
                print(f"Face detected: {datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}")
                for detection in results.detections:
                    # Adjust margin_fraction as needed
                    cropped_face = crop_face(frame, detection, margin_fraction=margin)
                    
                    # Get the detection time
                    datetime_string = datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")

                    # Save the cropped face image
                    cv2.imwrite(f"{data_dir}/{datetime_string}.jpg", cropped_face)

            # Break the loop on 'q' key press
            if cv2.waitKey(20) & 0xFF == ord('q'):
                break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Initialize MediaPipe Face Detection
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    scan_for_faces(margin=1,
                   confidence=0.5,
                   data_dir="faces")
