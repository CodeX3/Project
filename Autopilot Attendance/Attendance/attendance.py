import datetime
import sqlite3
from sqlite3 import Error

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

def MarkAttendance(name):
    today = datetime.date.today().strftime("%Y-%m-%d")
    if os.path.isfile(f'record/{today}.csv'):
        print("record already created")

    else :
        f=open(f'record/{today}.csv','x')
        f.writelines('Name,Date,Time')
        f.close()
        print("record created")
    with open(f'record/{today}.csv','r+') as f:
        myDataList = f.readlines()
        nameList=[]
        for line in myDataList:
            entry =line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.datetime.now()
            today = datetime.date.today().strftime("%Y-%m-%d")
            dtString =now.strftime("%H:%M:%S")
            f.writelines(f'\n{name},{today},{dtString}')
    try:
        # print(name)
        db_path = '../../HostelManagement/db.sqlite3'
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute(f"select sd_id from User_student Where sd_name='{name}'  ")
        result = cursor.fetchone()
        cursor.execute(f"select * from User_attendance Where sd_name='{name}'  AND  date=CURRENT_DATE ")
        at = cursor.fetchone()
        student_id = result[0]
        print(student_id)
        month = int(datetime.date.today().strftime("%m"))
        year = int(datetime.date.today().strftime("%Y"))
        if at is None:
            print("entered")
            cursor.execute(f"insert into User_attendance('sd_id','date','status','sd_name','stduent_info_id','month','year') values({student_id},CURRENT_DATE ,1,'{name}',{student_id},{month},{year}) ")
            connection.commit()
            print("value inserted")
        else:
            print("already value exists!!")
        cursor.close()
        connection.close()
        # print(result)
        # print(at)
    except Error as e:
        print(e)
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
            name =classNames[matchIndex]
            print(name)
            y1,x2,y2,x1 = faceloc
            # print(y1, x2, y2, x1)
            # y1, x2, y2, x1 =y1*4,x2*4,y2*4,x1*4
            # print(y1, x2, y2, x1)
            cv2.rectangle(img,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,0),2)
            # cv2.rectangle(img, (x1, y1-100), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            MarkAttendance(name)

    cv2.imshow('Webcam',img)
    cv2.waitKey(1)