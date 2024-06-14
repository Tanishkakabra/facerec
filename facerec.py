import face_recognition
import cv2
import os
import getpass
import sys
import pickle
import dlib
import numpy as np
PWD = "Meow"


detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("/home/tanishka/facerec/shape_predictor_68_face_landmarks.dat")

def shape_to_np(shape, dtype="int"):
    # Initialize the list of (x, y)-coordinates
    coords = np.zeros((68, 2), dtype=dtype)
    
    # Loop over the 68 facial landmarks and convert them to a 2-tuple of (x, y)-coordinates
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    
    return coords

def eye_aspect_ratio(eye):
    # Compute the euclidean distances between the two sets of vertical eye landmarks (x, y)-coordinates
    A = np.linalg.norm(eye[1] - eye[5])
    B = np.linalg.norm(eye[2] - eye[4])
    
    # Compute the euclidean distance between the horizontal eye landmark (x, y)-coordinates
    C = np.linalg.norm(eye[0] - eye[3])
    
    # Compute the eye aspect ratio
    ear = (A + B) / (2.0 * C)
    return ear

def detect_blink(frame):
    # Convert the image to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the grayscale image
    faces = detector(gray, 1)
    
    for face in faces:
        # Get the landmarks for the face
        shape = predictor(gray, face)
        shape = shape_to_np(shape)
        
        # Extract the coordinates for the left and right eye
        left_eye = shape[36:42]
        right_eye = shape[42:48]
        
        # Compute the eye aspect ratio (EAR) for both eyes
        left_ear = eye_aspect_ratio(left_eye)
        right_ear = eye_aspect_ratio(right_eye)
        
        # Average the EAR for both eyes
        ear = (left_ear + right_ear) / 2.0
        
        # Define a threshold to determine if the eyes are closed
        EAR_THRESHOLD = 0.25
        
        return ear < EAR_THRESHOLD
    
    return False
def load_known_faces(file_path):
    with open(file_path, 'rb') as f:
        known_face_encodings, known_face_names = pickle.load(f)
    return known_face_encodings, known_face_names


def is_face_known(cap):
    known_faces_file = '/home/tanishka/facerec/known_faces.pkl'
    known_face_encodings, known_face_names = load_known_faces(known_faces_file)
    count = 0
    blink_seen = False
    open_seen = False
    while count <= 10:
        count += 1
        ret, frame = cap.read()
        if not ret:
            continue
        test_face_locations = face_recognition.face_locations(frame)
        test_face_encodings = face_recognition.face_encodings(frame, test_face_locations)

        name = "Unknown"
        # Compare the test face with known faces
        for test_face_encoding in test_face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, test_face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            
            if (name != "Unknown"):
                if detect_blink(frame):
                    blink_seen = True
                else:
                    open_seen = True
                if (blink_seen and open_seen):
                    print("Test face matches:", name)
                    return True
            
    return False

            
def you_shall_not_pass():
    cap = cv2.VideoCapture(0)
    face_matches = is_face_known(cap)
    cap.release()
    cv2.destroyAllWindows()
    
    if face_matches:
        return True
    else:
        pcount = 0
        while pcount <= 10:
            pcount += 1
            password = getpass.getpass(prompt='Password: ')
            if password == PWD:
                print("Password Matches!")
                return True
            else:
                print("Try again!")
        if (pcount >= 10):
            return False
            print(PWD)

    
    
def main():
    ans = you_shall_not_pass()
    if ans:
        print("SUCCESS")
        sys.exit(0)
    else:
        print("FAILURE")
        sys.exit(0)

main()
    

