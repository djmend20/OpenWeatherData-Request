import requests;

def get_weatherdata(api_key, zip_code): 
	request_json = dict()
	try:
		url = "https://api.openweathermap.org/data/2.5/weather?zip=%s,us&appid=%s" % (zip_code, api_key)
		r = requests.get(url)
		request_json = r.json()
	except Exception as e:
		print("E: {0}".format(e))
	if 'message' in request_json and len(request_json) != 0:
		print('Could not request information')

	return r.json()

def open_weather_map_record(json):
	record = {}
	try:
		for key in json:
			if (type(json[key]) == dict):
				for embedded_key in json[key]:
					record['{0}_{1}'.format(key, embedded_key)] = json[key][embedded_key]
			elif (type(json[key]) == list):
				for embedded_key in json[key][0]:
					record['{0}_{1}'.format(key, embedded_key)] = json[key][0][embedded_key]
			else:
				record[key] = json[key]
		
	except Exception as e:
		print("Exception: {0}".format(e))
	
	return record