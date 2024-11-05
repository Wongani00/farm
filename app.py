from flask import Flask, render_template, jsonify, request
from datetime import datetime
import joblib
import pandas as pd

app = Flask(__name__) #initializing the app

# loading the model
model = joblib.load('ml_model/rfrmodel.joblib')

 # defining a dictionary and list that will be sent to the form's market and region inputs
markets = {'Area 23': 0,
        'Balaka Boma': 1,
        'Bangula': 2,
        'Bembeke turn off': 3,
        'Bolero': 4,
        'Bowe': 5,
        'Bvumbwe': 6,
        'Chamama': 7,
        'Chatoloma': 8,
        'Chikhwawa': 9,
        'Chikuli': 10,
        'Chikweo': 11,
        'Chilinga': 12,
        'Chilumba': 13,
        'Chimbiya': 14,
        'Chinakanaka': 15,
        'Chinamwali': 16,
        'Chintheche': 17,
        'Chiponde': 18,
        'Chiradzulu Boma': 19,
        'Chitakale': 20,
        'Chitipa Boma': 21,
        'Dowa Boma': 22,
        'Dwangwa': 23,
        'Dyelatu': 24,
        'Dzaleka': 25,
        'Dzaleka (inside Camp)': 26,
        'Embangweni': 27,
        'Euthini': 28,
        'Golomoti': 29,
        'Hewe': 30,
        'Jali': 31,
        'Jenda': 32,
        'Kambilonje': 33,
        'Kameme': 34,
        'Kamsonga': 35,
        'Kamuzu Road': 36,
        'Kamwendo': 37,
        'Karonga Boma': 38,
        'Kasiya': 39,
        'Kasungu Boma': 40,
        'Khuwi': 41,
        'Lilongwe': 42,
        'Limbe': 43,
        'Limbuli': 44,
        'Lirangwe': 45,
        'Liwonde': 46,
        'Lizulu': 47,
        'Luchenza': 48,
        'Luncheza': 49,
        'Lunzu': 50,
        'Madisi': 51,
        'Makanjila': 52,
        'Makanjira': 53,
        'Makhanga': 54,
        'Malomo': 55,
        'Mangamba': 56,
        'Mangochi Boma': 57,
        'Mangochi Turn Off': 58,
        'Manyamula': 59,
        'Marka': 60,
        'Mayaka': 61,
        'Mbela': 62,
        'Mbonechela': 63,
        'Mchinji Boma': 64,
        'Migowi': 65,
        'Misuku': 66,
        'Mitundu': 67,
        'Mkanda': 68,
        'Monkey Bay': 69,
        'Mpamba': 70,
        'Mpita': 71,
        'Mponela': 72,
        'Mtakataka': 73,
        'Mtowe': 74,
        'Mulanje Boma': 75,
        'Mulomba': 76,
        'Muloza': 77,
        'Mwansambo': 78,
        'Mwanza Boma': 79,
        'Mzimba': 80,
        'Mzuzu': 81,
        'Nambuma': 82,
        'Namwera': 83,
        'Nanjiri': 84,
        'Nayuchi': 85,
        'Nchalo': 86,
        'Neno Boma': 87,
        'Ngabu': 88,
        'Nkhamenya': 89,
        'Nkhatabay Boma': 90,
        'Nkhate': 91,
        'Nkhoma': 92,
        'Nkhotakota Boma': 93,
        'Nsanama': 94,
        'Nsanje Boma': 95,
        'Nserema': 96,
        'Nsikawanjala': 97,
        'Nsundwe': 98,
        'Nsungwi': 99,
        'Ntaja': 100,
        'Ntakataka': 101,
        'Ntcheu Boma': 102,
        'Ntchisi Boma': 103,
        'Nthalire': 104,
        'Ntonda': 105,
        'Ntowe': 106,
        'Phalombe Boma': 107,
        'Phaloni': 108,
        'Phalula': 109,
        'Rumphi Boma': 110,
        'Salima': 111,
        'Santhe': 112,
        'Sharpevaley': 113,
        'Songani': 114,
        'Songwe': 115,
        'Sorgin': 116,
        'Thavite': 117,
        'Thekerani': 118,
        'Thete': 119,
        'Thondwe': 120,
        'Thyolo Boma': 121,
        'Tomali': 122,
        'Tsangano turnoff': 123,
        'Uliwa': 124,
        'Ulongwe': 125,
        'Vigwagwa': 126,
        'Waliranji': 127,
        'Zomba Boma': 128} 
regions = ['Central Region', 'Northern Region', 'Southern Region']

# predicted price
predicted_price = 0
# defining the  home route
@app.route("/")
def index():
    return render_template("home.html")

# predict function
@app.route("/predict")
def predict():
    return render_template("predict.html", markets=markets, regions=regions)

#prediction function
@app.route("/prediction", methods=["POST"])
def prediction():
    # Receiving the JSON data sent from JS
    data = request.get_json()
    
    # Checking if necessary fields are present
    if not all(k in data for k in ("date", "region", "market", "commodity")):
        return jsonify({"error": "Missing data"}), 400
    
    date = data["date"]
    region = data["region"]
    market = data["market"]
    commodity = data["commodity"]
    
    # Converting date from HTML input to datetime object
    dateobject = datetime.strptime(date, '%Y-%m-%d')
    year = dateobject.year
    month = dateobject.month
    
    # usdprice dictionary
    usdprice = {'Beans': 1.2862449583897813,
            'Maize': 0.23245165743760904,
            'Rice': 0.966745234787441}
    # Initialize variables
    usdprice = 0  # This could also be passed as part of the request
    northern_region, central_region, southern_region = 0, 0, 0
    commodity_maize, commodity_rice, commodity_beans = 0, 0, 0
    category_cereals_tubers, category_pulses_nuts = 0, 0

    # Check the region
    if region == "Central Region":
        central_region = 1
    elif region == "Northern Region":
        northern_region = 1
    elif region == "Southern Region":
        southern_region = 1
    
    # Check commodity type and set features accordingly
    if commodity == "Maize":
        commodity_maize = 1
        category_cereals_tubers = 1
        usdprice = 0.23245
    elif commodity == "Beans":
        commodity_beans = 1
        category_pulses_nuts = 1
        usdprice = 7.4194
    elif commodity == "Rice":
        commodity_rice = 1
        category_cereals_tubers = 1
        usdprice = 0.9667

    # Create features list
    features = [[
        markets[market], usdprice, month, year,
        central_region, northern_region,
        southern_region, category_cereals_tubers,
        category_pulses_nuts, commodity_beans,
        commodity_maize, commodity_rice
    ]]

    # Print the features for debugging
    print("Features for prediction:", features)

    # Make prediction
    price_predicted = f"{model.predict(features)[0]:.2f}"
    
    # Print the predicted price for debugging
    print("Predicted price:", price_predicted)
    
    return jsonify({"price": price_predicted})


    # Dummy prediction logic for demonstration
    # predicted_price = (int(year) + int(month)) * 10  # Replace with your model's prediction logic

    # # Update the database
    # date = f"{year}-{month:02d}"
    # new_prediction = Prediction(date=date, price=predicted_price, commodity=commodity)
    # db.session.add(new_prediction)
    # db.session.commit()   
    return jsonify({"price":predicted_price})

# about route function
@app.route("/about")
def about():
    return render_template("about.html")

# page not found and internal server error handling
@app.errorhandler(404)
def page_not_found(e):
 return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
 return render_template('500.html'), 500


# calling the app
# if __name__ == "__main__":
#     app.run(debug=True) #running the app