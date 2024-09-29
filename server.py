import csv
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.DEBUG)

@app.route('/submit', methods=['POST'])
def submit():
    data = request.json
    app.logger.debug(f"Received data: {data}")
    try:
        with open('data.csv', 'a', newline='') as csvfile:
            fieldnames = ['name', 'email', 'major', 'research-interest-1', 'research-interest-2', 'research-interest-3']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerow(data)
        return jsonify({'message': 'Data saved successfully'}), 200
    except Exception as e:
        app.logger.error(f"Error writing to CSV: {e}")
        return jsonify({'message': 'Failed to save data'}), 500

if __name__ == '__main__':
    app.run(debug=True)