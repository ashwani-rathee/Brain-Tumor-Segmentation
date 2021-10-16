import os
import io
import json
from utils import *
from PIL import Image
from flask import Flask,request

app = Flask(__name__)

unet_model = DynamicUNet([16,32,64,128,256])
unet_classifier = BrainTumorClassifier(unet_model,'cpu')
unet_classifier.restore_model(os.path.join('./',f"brain_tumor_segmentor.pt"))

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)


@app.route('/')
def index():
    return 'Web App with Python Flask! Hey'

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        file = np.array(Image.open(io.BytesIO(file.read())))
        data =  {"image": file }
        output= unet_classifier.predict(data,  0.65)
        return json.dumps({'mask':output}, cls=NumpyEncoder)

if __name__ == '__main__':
    app.run()