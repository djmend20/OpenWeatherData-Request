try:

	import datetime
	
except Exception as e:
	print('E: {0}'.format(e))

def config_db():
	key = ['user', 'password', 'host', 'database', 'raise_on_warnings']
	value = []
	for posit in range(len(key)):
		msg = 'Type {0}: '.format(key[posit])
		val = input(msg)
		value.append(val)
	return dict(zip(key, value))

def attribute_list(table_description):
	try:
		attributes = []
		for posit in range(len(table_description)):
			attributes.append(table_description[posit][0])

	except Exception as e:
		print('attribute_list e: {0}'.format(e))
	return attributes

def update_timelog_data(old_data):
	try:
		new_data = []
		for posit in range(len(old_data)):
			if posit < 2:
				new_data.append(old_data[posit] + 1)
			else:
				new_data.append(old_data[posit])
	except Exception as e:
		print('update_timelog_data Error: {0}'.format(e))

	return new_data

def timelog_record(new_data, old_data, attribute_list):
	# old data: (0, 0, None, 0)
	# attribute list: []
	try:
		_record = {}
		for posit in range(len(attribute_list)):
			if old_data[posit] == None:
				_record[attribute_list[posit]] = datetime.datetime.now()
			elif new_data != None:
				_record[attribute_list[posit]] = new_data[posit]
			else:
				_record[attribute_list[posit]] = old_data[posit]
	except Exception as e:
		print("timelog_record Error: {0}".format(e))

	return _record


def weather_record(data_dict):
	record = {}
	try:
		for key in data_dict:
			if (type(data_dict[key]) == dict):
				for embedded_key in data_dict[key]:
					record['{0}_{1}'.format(key, embedded_key)] = data_dict[key][embedded_key]
			elif (type(data_dict[key]) == list):
				for embedded_key in data_dict[key][0]:
					record['{0}_{1}'.format(key, embedded_key)] = data_dict[key][0][embedded_key]
			else:
				record[key] = data_dict[key]
		
	except Exception as e:
		print("weather_record Exception: {0}".format(e))
	
	
	return record