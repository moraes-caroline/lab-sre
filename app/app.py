from flask import Flask, jsonify
import time
import logging
import psycopg2

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.psycopg2 import Psycopg2Instrumentor

app = Flask(__name__)

# OpenTelemetry
FlaskInstrumentor().instrument_app(app)
Psycopg2Instrumentor().instrument()

tracer = trace.get_tracer(__name__)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

logger = logging.getLogger(__name__)


def get_connection():
    return psycopg2.connect(
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


@app.route("/db-health")
def db_health():
    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT 1")

        cur.close()
        conn.close()

        return jsonify(status="healthy")

    except Exception as e:
        logger.exception("Database health check failed")
        return jsonify(status="unhealthy", error=str(e)), 500


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
    try:
        with tracer.start_as_current_span("database-query"):

            conn = get_connection()
            cur = conn.cursor()

            cur.execute("SELECT now();")

            result = cur.fetchone()

            cur.close()
            conn.close()

        return jsonify(time=str(result[0]))

    except Exception as e:
        logger.exception("Erro no endpoint /db")
        return jsonify(error=str(e)), 500


@app.route("/insert")
def insert():
    try:
        with tracer.start_as_current_span("database-insert"):

            conn = get_connection()
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
            conn.close()

        return jsonify(status="saved")

    except Exception as e:
        logger.exception("Erro no endpoint /insert")
        return jsonify(error=str(e)), 500


@app.route("/stats")
def stats():
    try:
        with tracer.start_as_current_span("database-count"):

            conn = get_connection()
            cur = conn.cursor()

            # Simulação de query lenta
            time.sleep(3)

            cur.execute(
                """
                SELECT COUNT(*)
                FROM requests
                """
            )

            count = cur.fetchone()[0]

            logger.info(f"Total registros: {count}")

            cur.close()
            conn.close()

        return jsonify(records=count)

    except Exception as e:
        logger.exception("Erro no endpoint /stats")
        return jsonify(error=str(e)), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
