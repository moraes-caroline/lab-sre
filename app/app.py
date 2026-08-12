from flask import Flask, jsonify
import time
import logging
import psycopg2

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor

app = Flask(__name__)

# OpenTelemetry
FlaskInstrumentor().instrument_app(app)
tracer = trace.get_tracer(__name__)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

# PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="observability",
    user="sre",
    password="sre123"
)


@app.route("/")
def home():
    return jsonify(status="ok")


@app.route("/health")
def health():
    return jsonify(status="healthy")


@app.route("/slow")
def slow():
    with tracer.start_as_current_span("slow-processing"):
        time.sleep(5)

    logger.info("/slow responded after sleep")

    return jsonify(status="slow")


@app.route("/error")
def error():
    try:
        raise Exception("Erro proposital")
    except Exception as e:
        logger.exception("Erro proposital no endpoint /error")
        return jsonify(error=str(e)), 500


@app.route("/db")
def db():
    with tracer.start_as_current_span("database-query"):
        cur = conn.cursor()

        cur.execute("SELECT now();")

        result = cur.fetchone()

        cur.close()

    return jsonify(time=str(result[0]))


@app.route("/insert")
def insert():
    with tracer.start_as_current_span("database-insert"):
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO requests(endpoint)
            VALUES (%s)
            """,
            ("/insert",)
        )

        conn.commit()

        cur.close()

    return jsonify(status="saved")


@app.route("/stats")
def stats():
    with tracer.start_as_current_span("database-count"):
        cur = conn.cursor()

        cur.execute(
            """
            SELECT count(*)
            FROM requests
            """
        )

        count = cur.fetchone()[0]

        cur.close()

    return jsonify(records=count)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
