"""

Download and put in the project folder: yolo.h5
https://github.com/OlafenwaMoses/ImageAI/tree/master/imageai/Detection

Скачать и положить в папку с проектом, файл: yolo.h5

"""

from imageai.Detection import VideoObjectDetection
import os

execution_path = os.getcwd()

detector = VideoObjectDetection()
detector.setModelTypeAsYOLOv3()
detector.setModelPath(os.path.join(execution_path , "yolo.h5"))
detector.loadModel()

video_path = detector.detectObjectsFromVideo(
    input_file_path=os.path.join(execution_path, "video1.mp4"),
    output_file_path=os.path.join(execution_path, "video1_new.mp4"),
    frames_per_second=20, log_progress=True
)
