import cv2
import time
import sys

cascPath = "Haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

def face_detector(img, count):
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=8,
        minSize=(30, 30)
    )

    #print(len(faces))
    #print("Done2")

    if faces is ():
        print("No Face Found")
        return img, []
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,255),2)
        roi = gray[y:y+h, x:x+w]
        roi = cv2.resize(roi, (300, 300))
        #print("Face Found "+str(count+1))
    return img, roi


def startCapturing(stdID):
    video_capture = cv2.VideoCapture(0 + cv2.CAP_DSHOW)
    video_capture.set(3, 480)
    video_capture.set(4, 480)
    count = 0

    while True:
        # Capture frame-by-frame
        ret, frame = video_capture.read()

        if not ret:
            break

        cv2.putText(frame, "Press Q to stop capturing", (40, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
        # Display the resulting frame
        cv2.imshow('Video', frame)
        # print("Before")

        original, cropped = face_detector(frame,count)
        if cropped == []:
            #print("Empty")
            continue

        #print("After")
        count += 1
        # Put count on images and display live count
        cv2.putText(original, "Saved {} images".format(count), (40, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
        cv2.imshow('Face Cropper', original)
        #file_name_path = 'face_database/'+stdID+'_' + str(count) + '_'+stdName+'.jpg'
        file_name_path = 'face_database/'+stdID+'_' + str(count) + '.jpg'
        cv2.imwrite(file_name_path, cropped)

        if count == 10:
            break

        time.sleep(1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #print(video_capture.isOpened())
    # When everything is done, release the capture
    video_capture.release()
    #print(video_capture.isOpened())
    cv2.destroyAllWindows()


# if __name__ == '__main__':
#     #stdID = sys.argv[1]
#     stdID = "1"
#     startCapturing(stdID)


# video_capture = cv2.VideoCapture(0)
# video_capture.set(3, 480)
# video_capture.set(4, 480)
# count = 0

# stdID = sys.argv[1]
#stdName = sys.argv[2]

# while True:
#     # Capture frame-by-frame
#     ret, frame = video_capture.read()

#     # Display the resulting frame
#     cv2.imshow('Video', frame)
#     # print("Before")

#     original, cropped = face_detector(frame,count)
#     if cropped == []:
#     	#print("Empty")
#     	continue

#     #print("After")
#     count += 1
#     # Put count on images and display live count
#     cv2.putText(original, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
#     cv2.imshow('Face Cropper', original)
#     #file_name_path = 'face_database/'+stdID+'_' + str(count) + '_'+stdName+'.jpg'
#     file_name_path = 'face_database/'+stdID+'_' + str(count) + '.jpg'
#     cv2.imwrite(file_name_path, cropped)

#     if count == 10:
#     	break

#     time.sleep(1)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # When everything is done, release the capture
# video_capture.release()
# cv2.destroyAllWindows()