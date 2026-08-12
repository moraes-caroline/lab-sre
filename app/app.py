from flask import Flask, jsonify
from opentelemetry.instrumentation.flask import FlaskInstrumentor
import time
import logging

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)

# Basic structured logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger(__name__)


@app.route("/")
def home():
    return jsonify(status="ok")


@app.route("/health")
def health():
    return jsonify(status="healthy")


@app.route("/slow")
def slow():
    # Simulate slow handler — avoid in production or move to background jobs
    time.sleep(5)
    logger.info("/slow responded after sleep")
    return jsonify(status="slow")


@app.route("/error")
def error():
    # Intentional error endpoint for testing; return structured error and log
    try:
        raise Exception("Erro proposital")
    except Exception as e:
        logger.exception("Erro proposital no endpoint /error")
        return jsonify(error=str(e)), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
