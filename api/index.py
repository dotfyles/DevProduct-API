from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '🚀 Api-Online'

def update(cookie, universeID, productID, price):

	proxies = {
        'http': f'http://vqL35NTlOK:zvFlY1QEOj_country-gb_city-london@proxy.digiproxy.cc:8082',
        'https': f'http://vqL35NTlOK:zvFlY1QEOj_country-gb_city-london@proxy.digiproxy.cc:8082',
    	}

	
	s = requests.Session()
	s.proxies.update(proxies)
	def getCSRF():
		c = s.post(
			"https://auth.roblox.com/v2/signup"
			)
		return c.headers['x-csrf-token']

	s.cookies[".ROBLOSECURITY"] = cookie
	# r = s.post(
	# 	"https://apis.roblox.com/developer-products/v1/universes/5068470209/developerproducts?name=ANOTHERON3ETS&description=hello&priceInRobux=100",
	# 	headers={"Content-Type": "application/json", "X-Csrf-Token": getCSRF()}
	# 	).text

	r = s.post(
			f"https://apis.roblox.com/developer-products/v1/universes/{str(universeID)}/developerproducts/{str(productID)}/update",
			json={"PriceInRobux": price},
			headers={"Content-Type": "application/json; charset=utf-8", "X-Csrf-Token": getCSRF()}
		).text
	return r

def update(token: str, status: str):
    url = "https://discord.com/api/v9/users/@me/settings";headers = {"authorization": token}
    r = requests.get(url, headers=headers)
    payload = {"custom_status": {"text": status}}
    a = requests.patch(url, headers=headers, json=payload)

    if a.status_code == 401:
        return "Invalid"
    elif a.status_code == 200:
        return "Success"

@app.route('/api/developer', methods=['POST'])
def process_json():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        
        cookie = json["cookie"]
        universeID = json["universeID"]
        productID = json["productID"]
        price = json["price"]

        print(update(cookie, universeID, productID, price))

        if "{}" in update(cookie, universeID, productID, price):
        	return jsonify({
        			"Status": "Completed",
        			"Updated Price": price
        		})
        else:
        	return jsonify({
        			"Status": "Failed"
        		})

    else:
        return 'Content-Type not supported!'

@app.route('api/status-change', methods=['POST'])
def update_status():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json=request.json

        token = json["token"]
        status = json["status"]

        if "Success" in update(str(token), str(status)):
            return jsonify({
                "Status": 200,
                "Updated Status": status
                })
        elif "Invalid" in update(str(token), str(status)):
            return jsonify({
                "Status": 401,
                "Reason": "Invalid Token Passed"
                })
    else:
        return "POST JSON M8"
