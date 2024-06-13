import face_recognition
import cv2
import os
import getpass
import sys
PWD = "Meow"


def load_known_faces(known_faces_dir):
    known_face_encodings = []
    known_face_names = []
    for filename in os.listdir(known_faces_dir):
        if filename.endswith(('.jpg', '.png', 'jpeg')):
            image_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:  # Ensure that at least one face was found
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])
    return known_face_encodings, known_face_names



def is_face_known(cap):
    known_faces_dir = '/home/tanishka/facerec/green_flags'
    known_face_encodings, known_face_names = load_known_faces(known_faces_dir)
    count = 0
    while count <= 10:
        count += 1
        ret, frame = cap.read()
        if ret:
            # Save the captured image to a file
            cv2.imwrite('/home/tanishka/facerec/khich.jpg', frame)
        # Load the test image
        test_image_path = '/home/tanishka/facerec/khich.jpg'  # Change this to the path of your test image
        test_image = face_recognition.load_image_file(test_image_path)
        test_face_locations = face_recognition.face_locations(test_image)
        test_face_encodings = face_recognition.face_encodings(test_image, test_face_locations)

        name = "Unknown"
        # Compare the test face with known faces
        for test_face_encoding in test_face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, test_face_encoding)
            name = "Unknown"

            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            
            if (name != "Unknown"):
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
    

