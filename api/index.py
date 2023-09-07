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
