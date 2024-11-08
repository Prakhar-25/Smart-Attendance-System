import face_recognition
import numpy as np
import cv2 as cv
from .models import KnownFace
import pickle


def train_image(img,name):

    known_faces = KnownFace.objects.all()
    known_names = [face.known_name for face in known_faces]
    known_encodings = [pickle.loads(face.known_encoding) for face in known_faces]

    # training image
    student_img = face_recognition.load_image_file(img)

    # face encoding
    student_fe = face_recognition.face_encodings(student_img)[0]

    # lists of known encodings and their names
    if name not in known_names:
        new_name = KnownFace(known_name = name)
        new_name.save()
        new_name.save_encoding(student_fe)
    

def recognize():
    known_faces = KnownFace.objects.all()
    known_names = [face.known_name for face in known_faces]
    known_encodings = [pickle.loads(face.known_encoding) for face in known_faces]
    student_name = "Unknown"
    camera_error = False
    print("known_names:",known_names)
    print("known_encodings: ",known_encodings)
    camera = cv.VideoCapture(0)
    if camera.isOpened():
        while True:
            success,frame = camera.read()
            if not success:
                break
            else:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv.resize(frame, (0, 0), fx=0.25, fy=0.25)
                #convert to RGB(face recognition) from BGR(opencv)
                rgb_frame = cv.cvtColor(small_frame,cv.COLOR_BGR2RGB)
                face_locations = face_recognition.face_locations(rgb_frame)
                face_encodings = face_recognition.face_encodings(rgb_frame,face_locations)
                face_names = []
                for face_encoding in face_encodings:
                    # check for match
                    matches = face_recognition.compare_faces(known_encodings,face_encoding)
                    name = "Unknown"  # default case
                    face_distances = face_recognition.face_distance(known_encodings,face_encoding)
                    print("face_distances: ",face_distances)
                    best_match_index = np.argmin(face_distances)

                    if matches[best_match_index]:
                        name = known_names[best_match_index]
                    face_names.append(name)
                    student_name = name

                for(top,right,bottom,left),name in zip(face_locations,face_names):
                    # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv.rectangle(frame, (left,top), (right,bottom), (0,255,0), 2) #outer box
                    cv.rectangle(frame, (left, bottom-20), (right,bottom),(0,255,0), cv.FILLED) # inner box
                    font = cv.FONT_HERSHEY_COMPLEX
                    cv.putText(frame, name, (left+6,bottom-6), font, 0.60, (0,0,0))
                    

            cv.imshow("Press 'q' to exit",frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
    else:
        camera_error = True
    camera.release()
    cv.destroyAllWindows()
    return student_name, camera_error