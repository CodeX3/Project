import cv2
import numpy as np
import face_recognition
import os

path = 'images'
images =[]
classNames =[]
myList =os.listdir(path)
print(myList)

for cl in myList:
    current_image =cv2.imread(f'{path}/{cl}')
    images.append(current_image)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

def findEncodings(images):
    encodeList =[]
    for img in images:
        img =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode =face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnownFaces =findEncodings(images)
print("Successfull encoding")

# camera
cap = cv2.VideoCapture(0)

while True:
    success,img =cap.read()
    # reduce size of image 1/4 of original
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS =cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    # multiple face in one frame
    facesCurrentFrame =face_recognition.face_locations(imgS)
    encodeCurrentFrame =face_recognition.face_encodings(imgS,facesCurrentFrame)

    for encodeFace,faceloc in zip(encodeCurrentFrame,facesCurrentFrame):
        matches = face_recognition.compare_faces(encodeListKnownFaces,encodeFace)
        faceDistance = face_recognition.face_distance(encodeListKnownFaces,encodeFace)
        matchIndex=np.argmin(faceDistance)

        # find the name
        if matches[matchIndex]:
            name =classNames[matchIndex].upper()
            print(name)
            y1,x2,y2,x1 = faceloc
            # print(y1, x2, y2, x1)
            # y1, x2, y2, x1 =y1*4,x2*4,y2*4,x1*4
            # print(y1, x2, y2, x1)
            cv2.rectangle(img,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,0),2)
            # cv2.rectangle(img, (x1, y1-100), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    cv2.imshow('Webcam',img)
    cv2.waitKey(1)