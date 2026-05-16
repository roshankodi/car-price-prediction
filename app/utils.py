import json
import pickle
import logging
import numpy as np
import os

from CONFIG import MODEL_PATH, COLUMNS_PATH, ENCODE_PATH

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


class Prediction:

    model = None
    columns = None
    encodings = None

    def __init__(self):

        if Prediction.model is None:
            self.load_files()

    def load_files(self):

        try:

            if not os.path.exists(MODEL_PATH):
                raise FileNotFoundError(
                    f"Model file not found: {MODEL_PATH}"
                )

            with open(MODEL_PATH, 'rb') as f:
                Prediction.model = pickle.load(f)

            with open(COLUMNS_PATH, 'r') as f:
                Prediction.columns = json.load(f)

            with open(ENCODE_PATH, 'r') as f:
                Prediction.encodings = json.load(f)

            logger.info(
                "Model and configuration loaded successfully"
            )

        except Exception as e:

            logger.error(
                f"Loading error: {str(e)}"
            )

            raise

    def encode_input(self, data):

        encoded = []

        for idx, col in enumerate(
            Prediction.columns
        ):

            value = data[idx]

            if (
                col in Prediction.encodings
                and not isinstance(
                    value,
                    (
                        int,
                        float,
                        np.integer,
                        np.floating
                    )
                )
            ):

                value = Prediction.encodings[
                    col
                ].get(
                    str(value),
                    -1
                )

            encoded.append(
                float(value)
            )

        return np.array(
            encoded,
            dtype=float
        ).reshape(
            1,
            -1
        )

    def predict(self, data):

        input_encoded = self.encode_input(
            data
        )

        prediction = Prediction.model.predict(
            input_encoded
        )[0]

        logger.info(
            f"Prediction successful: {prediction}"
        )

        return float(
            prediction
        )