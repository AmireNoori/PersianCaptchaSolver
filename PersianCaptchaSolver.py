from mltu.configs import BaseModelConfigs
import cv2
from mltu.inferenceModel import OnnxInferenceModel
from mltu.utils.text_utils import ctc_decoder
import typing
import numpy as np

class CaptchaSolver(OnnxInferenceModel):
    def __init__(self, char_list: typing.Union[str, list], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.char_list = char_list

    def predict(self, image: np.ndarray):
        image = cv2.resize(image, self.input_shapes[0][1:3][::-1])

        image_pred = np.expand_dims(image, axis=0).astype(np.float32)

        preds = self.model.run(self.output_names, {self.input_names[0]: image_pred})[0]

        text = ctc_decoder(preds, self.char_list)[0]

        return text
    
    def Solve(image_path):

        configs = BaseModelConfigs.load("Models/02_captcha_to_text/202406131352/configs.yaml")

        model = CaptchaSolver(model_path=configs.model_path, char_list=configs.vocab)

        image = cv2.imread(image_path.replace("\\", "/"))

        main_prediction_text = model.predict(image)

        if "_" in main_prediction_text:
            parts = main_prediction_text.split("_")
            prediction_text = parts[0]
        else:
            prediction_text = main_prediction_text

        try:
            result = eval(prediction_text)
            final = f"{prediction_text}={result}"
        except SyntaxError:
            result = None
            final = main_prediction_text

        return final,result

