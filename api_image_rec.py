from flask import Flask, request, Response
import numpy as np
import json
import cv2

#Initialize Flask application
app = Flask(__name__)

#route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
	r = request
	#convert string of image data to uint8
	nparr = np.fromstring(r.data, np.uint8)
	#decode image
	img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
	#do your processing here with image
	#cv2.imwrite("img.jpg", img)

	#response
	response = {'message': 'image received. size = {}x{}'.format(img.shape[1], img.shape[0])}
	responseJson = json.dumps(response)
	return Response(response=responseJson, status=200, mimetype="application/json")

#start flask app
app.run(host="0.0.0.0", port=5000)