import cv2
import numpy as np
from django.core.files.base import ContentFile
from .models import *
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import *
from googletrans import Translator


translator = Translator()

VOC_LABELS = [
    "background", "aeroplane", "bicycle", "bird", "boat", "bottle",
    "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant",
    "sheep", "sofa", "train", "tvmonitor"
]


def process_image(image_feed_id):
    try:
        image_feed = UserImage.objects.get(enter_user_name=image_feed_id, was_processed=False)
        image_path = image_feed.image.path

        model_path = 'DetectorApp/mobilenet_iter_73000.caffemodel'
        config_path = 'DetectorApp/mobilenet_ssd_deploy.prototxt'
        net = cv2.dnn.readNetFromCaffe(config_path, model_path)

        img = cv2.imread(image_path)
        if img is None:
            print("Failed to load image")
            return False

        h, w = img.shape[:2]
        blob = cv2.dnn.blobFromImage(img, 0.007843, (300, 300), 127.5)

        net.setInput(blob)
        detections = net.forward()

        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.6:
                class_id = int(detections[0, 0, i, 1])
                class_label = VOC_LABELS[class_id]
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                cv2.rectangle(img, (startX, startY), (endX, endY), (0, 255, 0), 2)
                label = f"{class_label}: {confidence:.2f}"
                cv2.putText(img, label, (startX + 5, startY + 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                new_pic = ProcessedUserImage.objects.create(
                    processed_image='image_feed',
                    image_user_name=image_feed_id,
                    object_type=translator.translate(class_label, src='en', dest='ru').text,
                    location=f"{startX},{startY},{endX},{endY}",
                    confidence=float(confidence)
                )
                image_feed.was_processed = True

        result, encoded_img = cv2.imencode('.jpg', img)
        if result:
            content = ContentFile(encoded_img.tobytes(), f'processed_{image_feed.image.name}')
            new_pic.processed_image.save(content.name, content, save=True)

        return True

    except UserImage.DoesNotExist:
        print("ImageFeed not found.")
        return False
