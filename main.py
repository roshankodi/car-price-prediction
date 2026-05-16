from flask import (
    Flask,
    render_template,
    request,
    flash,
    jsonify
)
import logging

from CONFIG import DEBUG, HOST, PORT, SECRET_KEY
from app.utils import Prediction


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

app = Flask(__name__)
app.secret_key = SECRET_KEY

_predictor = None


def get_predictor():
    global _predictor

    if _predictor is None:
        _predictor = Prediction()

    return _predictor


@app.route('/')
def home():
    return render_template(
        'index.html'
    )


@app.route(
    '/predict',
    methods=['POST']
)
def predict_price():

    try:

        year = int(
            request.form.get(
                'year',
                ''
            ).strip()
        )

        km_driven = int(
            request.form.get(
                'km_driven',
                ''
            ).strip()
        )

        fuel = int(
            request.form.get(
                'fuel',
                ''
            ).strip()
        )

        seller_type = int(
            request.form.get(
                'seller_type',
                ''
            ).strip()
        )

        transmission = int(
            request.form.get(
                'transmission',
                ''
            ).strip()
        )

        owner = int(
            request.form.get(
                'owner',
                ''
            ).strip()
        )

        if year < 1900 or year > 2100:
            raise ValueError(
                "Year must be between 1900 and 2100"
            )

        if km_driven < 0:
            raise ValueError(
                "Kilometers driven cannot be negative"
            )

        current_year = 2026

        car_age = max(
            current_year - year,
            1
        )

        km_per_year = (
            km_driven / car_age
        )

        data = [
            year,
            km_driven,
            fuel,
            seller_type,
            transmission,
            owner,
            car_age,
            km_per_year
        ]

        price = max(
            0.0,
            get_predictor().predict(
                data
            )
        )

        return render_template(
    "index.html",
    prediction_text=f"₹{price:,.2f}",
    model_name="Random Forest Regressor",
    accuracy="~85–95%",
    car_age=car_age,
    km_per_year=round(
        km_per_year,
        2
    )
)

    except ValueError as e:

        flash(
            f"Invalid input: {e}"
        )

    except Exception:

        logging.exception(
            "Prediction failed"
        )

        flash(
            "Something went wrong while generating prediction."
        )

    return render_template(
        "index.html"
    )


if __name__ == "__main__":

    app.run(
        host=HOST,
        port=PORT,
        debug=DEBUG
    )

@app.route(
    '/api/predict',
    methods=['POST']
)
def api_predict():

    try:

        data = request.get_json()

        if not data:

            return jsonify({

                "error":
                "No JSON data provided"

            }),400


        year = int(
            data.get(
                "year"
            )
        )

        km_driven = int(
            data.get(
                "km_driven"
            )
        )

        fuel = int(
            data.get(
                "fuel"
            )
        )

        seller_type = int(
            data.get(
                "seller_type"
            )
        )

        transmission = int(
            data.get(
                "transmission"
            )
        )

        owner = int(
            data.get(
                "owner"
            )
        )

        current_year = 2026

        car_age = max(
            current_year-year,
            1
        )

        km_per_year = (
            km_driven/car_age
        )

        features=[

            year,
            km_driven,
            fuel,
            seller_type,
            transmission,
            owner,
            car_age,
            km_per_year

        ]

        price=max(
            0,
            get_predictor().predict(
                features
            )
        )

        return jsonify({

            "predicted_price":
            round(
                float(price),
                2
            ),

            "car_age":
            car_age,

            "km_per_year":
            round(
                km_per_year,
                2
            )

        })

    except Exception as e:

        return jsonify({

            "error":
            str(e)

        }),400

    except Exception as e:

        return jsonify({

            "error":
            str(e)

        }),400