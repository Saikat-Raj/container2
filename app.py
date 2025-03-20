import os
import csv
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/calculate", methods=["POST"])
def calculate():
    try:
        data = request.get_json()
        file_path = os.path.join("/data", data["file"])

        if not os.path.exists(file_path):
            return jsonify({"file": data["file"], "error": "File not found."}), 404

        try:
            total_sum = 0
            with open(file_path, "r") as csvfile:
                reader = csv.DictReader(csvfile)

                if not all(field in reader.fieldnames for field in ["product", "amount"]):
                    return (
                        jsonify({"file": data["file"], "error": "Input file not in CSV format."}),
                        400,
                    )

                total_sum = sum(int(row["amount"]) for row in reader if row["product"] == data["product"])

            return jsonify({"file": data["file"], "sum": total_sum})

        except Exception:
            return (
                jsonify({"file": data["file"], "error": "Input file not in CSV format."}),
                400,
            )

    except Exception as e:
        return jsonify({"file": data["file"], "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6001)
