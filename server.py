from flask import Flask,request
from flask import render_template
from flask_cors import CORS
import json
from Compression import *

#Initiate flaskapp 

app = Flask(__name__)
CORS(app)

@app.route('/test/<var>')
def index(var):
    return 'This is the value in A:'

# @app.route('/compress', methods=['POST'])
# def compress():
#     req_data = request.get_json()
#     compression_value = req_data['compression']
#     file_name = req_data['filePath']
#     compression_value = float(compression_value) / 10
#     print(compression_value)
#     jCoder = jpeg_coder(compression_value)
#     file_name = './src/assets/images/' + str(file_name)
#     sizeBefore, sizeAfter = jCoder.encode(file_name)

#     print(compression_value)
#     print(file_name)
 
#     data ={}
#     data['fileSizeBefore'] = int(sizeBefore)
#     data['fileSizeAfter'] = int(sizeAfter)
#     json_data = json.dumps(data)
#     return json_data
    
# @app.route('/result')
# def result():
#     return 'result to be implemented soon!'


if __name__=="__main__":
    app.run(debug=True)