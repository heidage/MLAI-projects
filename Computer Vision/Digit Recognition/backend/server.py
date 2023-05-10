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
    image = request.json.get('image')
    if image != "":
        image_array = url_to_image(image)
        result = model.predict(image_array)
        prediction = np.argmax(result,axis=1)[0]
        return {'image_prediction': int(prediction)}
    else:
        return {'image_prediction': "Nope"}

def url_to_image(url):
    image_64 = url.split(',')[1]
    binary = base64.b64decode(image_64)
    image = Image.open(io.BytesIO(binary))
    image = cv2.cvtColor(np.array(image),cv2.IMREAD_GRAYSCALE)

    pred_img_resize = cv2.resize(image,(28,28))
    pred_img_resize = cv2.bitwise_not(pred_img_resize)

    pred_img_normalized = pred_img_resize.astype('float32')/255.0
    pred_img_normalized = pred_img_normalized.reshape(-1,28,28,1)

    return pred_img_normalized

if __name__ == '__main__':
    app.run(debug=True)