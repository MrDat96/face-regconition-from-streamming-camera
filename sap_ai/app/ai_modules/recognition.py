from fas_recognition import detection, feature_extraction, classification, \
    image_utils
from PIL import Image
import time

PATH_ENDCODE = "./data/encode_data"
def recognition(pathImage):
    image = Image.open(pathImage)

    image = image_utils.rotate_on_exif(image)
    image = image_utils.resize_max_size(image, 2000, 2000)

    detector = detection.MTCNNDetector(thresholds=[0.8, 0.9, 0.9])
    start_time = time.time()
    boxes = detector.detect(image) #Cut face
    if not len(boxes):
        print("No one is deteced!")
        DETECTING = False
        return
    print(f'Detection time: {time.time() - start_time}')

    encoder = feature_extraction.FaceEncoder()
    start_time = time.time()
    tensors = encoder.encode(image, boxes) # Encode face
    print(f'Encoding time: {time.time() - start_time}')

    # Declare classifier
    classifier = classification.WeightedKNNClassifier(distance_threshold=0.5,
                                                    n_neighbors=7)
    start_time = time.time()
    #
    classifier.fit(PATH_ENDCODE)
    print(f'Classification training time: {time.time() - start_time}')

    start_time = time.time()
    labels = classifier.predict(tensors) #Who
    print(f'Classification time: {time.time() - start_time}')

    print(boxes, len(boxes))
    print(labels, len(labels))