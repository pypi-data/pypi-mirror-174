from ..model_zoo import ClassificationTrtPredictor


class ObjectClassificationTrt:
    def __init__(self,
                 trt_file="models/person-cls.trt",
                 input_shape=(224, 224),
                 conf=0.01,
                 iou=0.45,
                 end2end=False):
        self.conf = conf
        self.iou = iou
        self.end2end = end2end
        self.model = ClassificationTrtPredictor(trt_file=trt_file, image_size=input_shape)

    def predict(self, image, class_names):
        return self.model.predict(image, class_names=class_names)

    @staticmethod
    def show(image, result):
        pass
