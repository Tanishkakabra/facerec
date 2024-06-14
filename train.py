import face_recognition
import os
import pickle

def load_and_save_known_faces(known_faces_dir, output_file):
    known_face_encodings = []
    known_face_names = []
    for filename in os.listdir(known_faces_dir):
        if filename.endswith(('.jpg', '.png', 'jpeg', 'JPG')):
            image_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(image_path)
            encodings = face_recognition.face_encodings(image)
            if encodings:  # Ensure that at least one face was found
                known_face_encodings.append(encodings[0])
                known_face_names.append(os.path.splitext(filename)[0])

    # Save the encodings and names to a file
    with open(output_file, 'wb') as f:
        pickle.dump((known_face_encodings, known_face_names), f)

if __name__ == "__main__":
    known_faces_dir = '/home/tanishka/facerec/green_flags'
    output_file = '/home/tanishka/facerec/known_faces.pkl'
    load_and_save_known_faces(known_faces_dir, output_file)
    print("Known faces have been serialized to", output_file)
