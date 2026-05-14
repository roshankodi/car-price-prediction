from flask import Flask, render_template, request, flash
from app.utils import Prediction

app = Flask(__name__)
import os
app.secret_key = os.getenv("SECRET_KEY", "dev_secret")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_price():
    try:
        year = int(request.form['year'])
        km_driven = int(request.form['km_driven'])
        fuel = int(request.form['fuel'])
        seller_type = int(request.form['seller_type'])
        transmission = int(request.form['transmission'])
        owner = int(request.form['owner'])

        data = [year, km_driven, fuel, seller_type, transmission, owner]

        pred_obj = Prediction()
        price = max(0, pred_obj.predict(data))  # ✅ prevent negative price

        return render_template('index.html', prediction_text=f"Predicted Price: ₹{round(price, 2)}")

    except Exception as e:
        flash(f"Error: {e}")
        return render_template("index.html")

if __name__ == '__main__':
    print("🚀 Flask app starting...")
    if __name__ == "__main__":
    app.run()
