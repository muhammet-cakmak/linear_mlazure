import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods = ['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    
    int_features = [int(x) for x in request.form.values()]
    #final_features = np.array(int_features)
    final_features = [int_features]
    ## You can use an indendent python file for infernece
    import requests
    import json 
    
    json_data = json.dumps({"data":final_features})  # final_features   formatı liste içinde liste olmalı.

    request_headers = {'Content-Type':'application/json'} # tahmine girecek arayüzden gelen data json formatında olacağı için  buraya json yazdık

    response = requests.post(

        url = "http://b62bce06-d9d8-4748-8aeb-1a2a067af1fd.eastus2.azurecontainer.io/score",   # REST Endpoint
        data=json_data,
        headers=request_headers
    )
   
    # Bu response.cotent sonucu byte dönüyor bunu floata cevirdim. Çoklu girdi olursa liste yapmak lazım ona bak.
    output = float(response.content.decode('utf8').replace("[", '').replace("]", ''))
    
    return render_template('index.html', prediction_text = 'Employee Salary should be $ {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)


