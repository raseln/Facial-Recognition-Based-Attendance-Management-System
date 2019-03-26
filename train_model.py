import cv2
import numpy as np
from os import listdir
from os.path import isfile, join

# Get the training data we previously made
data_path = 'D:/Image Processing Tutorial/Practices/amsrf/face_database/'
#data_path = 'D:/Image Processing Tutorial/Practices/amsrf/training_data1/'
onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

# Create arrays for training data and labels
Training_Data, Labels = [], []

# Open training images in our datapath
# Create a numpy array for training data
for i, files in enumerate(onlyfiles):
    image_path = data_path + onlyfiles[i]
    images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    Training_Data.append(np.asarray(images, dtype=np.uint8))
    ids = onlyfiles[i].split("_")[0]
    Labels.append(ids)

# Create a numpy array for labels
Labels = np.asarray(Labels, dtype=np.int32)
#Labels = np.array(Labels)

# Initialize facial recognizer
model = cv2.face.LBPHFaceRecognizer_create()
#model = cv2.face.EigenFaceRecognizer_create()
#model = cv2.face.FisherFaceRecognizer_create()

# Training our model
model.train(Training_Data, Labels)
model.save("trained_model.yml")
print("Model trained sucessefully")