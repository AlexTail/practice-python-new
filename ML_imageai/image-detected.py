"""

Скачать необходимо и положить в папку с проектом: resnet50_coco_best_v2.0.1.h5
https://github.com/OlafenwaMoses/ImageAI/tree/master/imageai/Detection


"""


from imageai.Detection import ObjectDetection
import os

exec_path = os.getcwd()


detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(
    exec_path, "resnet50_coco_best_v2.0.1.h5")
) 
detector.loadModel()

list = detector.detectObjectsFromImage(
    input_image=os.path.join(exec_path, '1.jpeg'),
    output_image_path=os.path.join(exec_path, '1_new.jpeg'),
    minimum_percentage_probability=90, #минимальный % чтобы учитывал
    display_percentage_probability=True, #% указываться будет
    display_object_name=False #name указываться не будет
)