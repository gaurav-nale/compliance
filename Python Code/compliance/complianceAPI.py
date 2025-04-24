from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

# API Endpoint: API Gateway endpoint
def call_api_gateway(API_URL, payload, header = None):
    try:
        if header is None:
            header = {
                'Content-Type' : 'application/json',
                'x-api-key' : 'lYHsJE2Lnl1BDpLqQXXhtvXsDynbS12aELP0CUih'
            }
        
        response = requests.post(API_URL, data = json.dumps(payload), headers=header)
        response.raise_for_status()

        return {
            'status_code': response.status_code,
            'headers': dict(response.headers),
            'body': response.json()
        }

    except Exception as e:
        return {
            "Error" : str(e)
        }, 500
    
@app.route("/call_api", methods = ['POST'])
def call_api():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"Error" : "Invalid JSON payload"}), 400
        
        API_URL = "https://g9z9wv5is3.execute-api.us-east-2.amazonaws.com/dev/scanner"

        payload = {
            "query": [
                {
                    "type": "Sender",
                    "name": "John Doe",
                    "address1": "123 Main St",
                    "city": "Anytown",
                    "country": "USA",
                    "skipScanning": "no"
                },
                {
                    "type": "Beneficiary",
                    "name": "Example Corp",
                    "country": "Canada",
                    "skipScanning": "no"
                }
            ]
        }

        api_response = call_api_gateway(API_URL, data if data else payload)

        if "Error" in api_response:
            return jsonify(api_response), api_response[1]
        
        return jsonify(api_response), 200

    except Exception as e:
        return jsonify({'Error' : str(e)}), 500
    
if __name__ == '__main__':
    app.run(host = "0.0.0.0", port = 5000, debug = True)