from flask import Flask, request
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import base64
import cv2
import io
from PIL import Image

model = tf.keras.models.load_model('../model/final_model.h5')
app = Flask(__name__)
CORS(app)

@app.route('/process_image',methods=['POST'])
def predict_digit():
    jsonData = request.get_json()
    data = jsonData['image']
    if data != "":
        image_array = url_to_image(data)
        result = model.predict(image_array)
        prediction = np.argmax(result,axis=1)[0]
        return {'image_prediction': int(prediction)}
    else:
        return {'image_prediction': "Nope"}

def url_to_image(url):
    image_64 = url.split('base64,')[1]
    binary = base64.b64decode(image_64)
    image = Image.open(io.BytesIO(binary)).convert('L')

    pred_img_resize = image.resize((28,28), Image.ANTIALIAS)
    
    #handle the threshhold iof not array would be all 0 if i use black pen
    threshold = 0
    img = pred_img_resize.point(lambda p: p > threshold and 255)

    pred_img_resize = np.array(img).reshape(-1,28,28,1)
    pred_img_normalized = pred_img_resize.astype('float32')/255.0

    return pred_img_normalized

if __name__ == '__main__':
    app.run(debug=True)