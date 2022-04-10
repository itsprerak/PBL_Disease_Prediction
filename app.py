from flask import Flask, jsonify, request,render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

app = Flask(__name__, template_folder='Templates')
model = pickle.load(open("model.pkl", "rb"))


# @app.route("/")
# @cross_origin()
# def home():
#     return render_template("review-page.html")


@app.route("/predict", methods = ["GET", "POST"])
def predict():
    return jsonify({"disease": "Dummy"})




@app.route("/process", methods = ["GET", "POST"])
@cross_origin()
def predict2():
    df = pd.read_csv("Symptom-severity.csv")
    symp = dict(zip(df.Symptom, df.weight))
    prediction_text = "dummy dum dum"
    if request.method == "POST":

        # Taking Symptoms
        symptoms = request.form["ddlViewBy"]
        print(symptoms)

        X = pd.DataFrame([
            PM2,
            PM10,
            NO,
            NO2,
            NOx,
            Ammonia,
            CO,
            SO2,
            Ozone,
            Benzene,
            Toluene,
            Year,
            m,
            City_Group_B,
            City_Group_C,
            City_Group_D,
            City_Group_E,
            City_Group_F
        ])
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        scaler.fit(X)
        X = scaler.transform(X)

        prediction=model.predict(X)

        output=round(prediction[0],2)
        if(output<=50):
            air_qual = "GOOD"
        elif(output<=100):
            air_qual="SATISFACTORY"
        elif(output<=200):
            air_qual="MODERATE"
        elif(output<=300):
            air_qual="POOR"
        elif(output<=400):
            air_qual="VERY POOR"
        else:
            air_qual="SEVERE"

        prediction_text = "AQI : {} - {}".format(output, air_qual)
        # We throw this string onto the html in the form of a variable i.e prediction_text
        # there with Jinja Templating you can pay around with it
        
        return render_template("result.html", prediction_text = prediction_text)

    return render_template("trial.html")


if __name__ == "__main__":
    app.run(debug=True)