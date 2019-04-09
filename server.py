__author__='deej'

from flask import Flask,request,render_template

# from flask_cors import CORS
import json
# from Compression import *
from Compression import *
#Initiate flaskapp 

app = Flask(__name__)
# CORS(app)



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['GET','POST'])
def test():
  if request.method == 'POST':
    thresh = float(request.form['thresh'])     # [-50, 0]
    ratio = int(request.form['ratio'])        # [1, 50]
    print(ratio)
    knee= int(request.form['knee'])      # [0, 20]
    att = float(request.form['att']) # between 0 & 0.5
    rel = float(request.form['rel'])   # between 0.001 & 2.5
      # def __init__(self,comp_threshold,comp_ratio,attack,release,knee_width):
    dr_compress=DRC(thresh,ratio,att,rel,knee)
    dr_compress.Init_Compression()
  return 'params'

# print(params[a])

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