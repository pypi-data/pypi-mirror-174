import cv2
import numpy as np
from ..utils import softmax
from ..utils import BaseEngine


def preprocess(image, input_size, mean, std, swap=(2, 0, 1)):
    imh, imw = image.shape[:2]
    m = min(imh, imw)  # min dimension
    top, left = (imh - m) // 2, (imw - m) // 2
    padded_img = cv2.resize(image[top:top + m, left:left + m], input_size, interpolation=cv2.INTER_LINEAR)
    padded_img = padded_img[:, :, ::-1].astype(np.float32)
    padded_img /= 255.0
    if mean is not None:
        padded_img -= np.array(mean)
    if std is not None:
        padded_img /= np.array(std)
    padded_img = padded_img.transpose(swap)
    padded_img = np.ascontiguousarray(padded_img, dtype=np.float32)
    return padded_img


class ClassificationTrtPredictor(BaseEngine):
    def __init__(self, trt_file, image_size=(224, 224)):
        super(ClassificationTrtPredictor, self).__init__(trt_file)
        self.image_size = image_size  # (h, w)
        self.mean = [0.485, 0.456, 0.406]
        self.std = [0.229, 0.224, 0.225]

    def predict(self, origin_img, class_names: list):
        n_classes = len(class_names)
        img = preprocess(origin_img, self.image_size, self.mean, self.std)
        data = self.infer(img)
        predictions = np.reshape(data, (1, -1, n_classes))[0][0]
        out = softmax(predictions) * 100
        output_class = np.argmax(out)

        return {'category_id': int(output_class),
                'category': class_names[int(output_class)],
                'score': float(out[int(output_class)])}
