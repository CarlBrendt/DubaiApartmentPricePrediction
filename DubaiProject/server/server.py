from flask import Flask,request,jsonify
import util

app = Flask(__name__)

@app.route('/get_district_names')
def get_district_names():
    response = jsonify({
        'locations' : util.get_district_names()
    })
    response.headers.add('Access-Control-Allow-Origin','*' )
    return response

@app.route('/predict_apartment_price', methods = ['POST'])
def predict_apartment_price():
    total_sqft = float(request.form['total_sqft'])
    location = request.form['location']
    bhk = int(request.form['bhk'])
    bath = int(request.form['bath'])
    
    response = jsonify({
        'estimated_price' : str(util.get_estimated_price(location,bhk,bath,total_sqft))
    })
    
    response.headers.add('Access-Control-Allow-Origin','*')
    return response
    
if __name__ == "__main__":
    print("Starting Pytohn Server for Apartment Price Prediction")
    util.load_saved_artifacts()
    app.run()