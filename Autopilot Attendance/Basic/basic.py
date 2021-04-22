import cv2
import numpy as np
import face_recognition

# load image
imgMe =face_recognition.load_image_file('imageDir/Ajith Anand.jpg')
imgMe =cv2.cvtColor(imgMe,cv2.COLOR_BGR2RGB)

imgTest =face_recognition.load_image_file('imageDir/check.jpg')
imgTest =cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)


# identify face in image
facelocation =face_recognition.face_locations(imgMe)[0]
encodeME = face_recognition.face_encodings(imgMe)[0]
print(facelocation) #top right bottom left values
cv2.rectangle(imgMe,(facelocation[3],facelocation[0]),(facelocation[1],facelocation[2]),(255,0,255),2)

facelocation =face_recognition.face_locations(imgTest)[0]
encodeTest = face_recognition.face_encodings(imgTest)[0]
print(facelocation) #top right bottom left values
cv2.rectangle(imgTest,(facelocation[3],facelocation[0]),(facelocation[1],facelocation[2]),(255,0,255),2)

results =face_recognition.compare_faces([encodeME],encodeTest)
face_distance =face_recognition.face_distance([encodeME],encodeTest)
print(results,face_distance)

cv2.putText(imgTest,f'{results} {round(facelocation[0],2)}',(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,0),2)


# show image
cv2.namedWindow('output',cv2.WINDOW_NORMAL)
cv2.resizeWindow('output',1000,1000)
cv2.imshow('output',imgMe)

cv2.namedWindow('output2',cv2.WINDOW_NORMAL)
cv2.resizeWindow('output2',600,600)
cv2.imshow('output2',imgTest)

cv2.waitKey(0)