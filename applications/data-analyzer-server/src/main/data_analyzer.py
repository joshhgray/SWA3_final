from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze_data():
    try:
        input_data = request.get_json()
    except Exception as e:
        return jsonify({"error": str(e)}), 500