try:
	import_success = True
	import sys
	import datetime
	import mysql.connector
	sys.path.append("..")
	
	from classes_methods.api_method import *
	from classes_methods.db_methods import *
	from classes_methods.methods import *
	from mysql.connector import errorcode
	

except Exception as e:
	print('Import Error: {e}'.format(e))
	import_success = False

def main():
	if (import_success):
		try:		
			config = config_db()
			db_connector = mysql.connector.connect(**config)
			query_tables = ['timelog', 'rd_weather'] # existing tables within mysql database

			id_last_record = (query(db_connector, 'MAX(id)', None, 1, query_tables[0]))[0][0] # returns a list of tuples
			last_record = (query(db_connector, '*', 'id = {0}'.format(id_last_record), 1, query_tables[0]))[0]
			timelog_description = table_description(db_connector, 'timelog')
			timelog_attribute = attribute_list(timelog_description)
			
			request_limit = 3 # limit set beforehand
			zip_code = input("Enter Zipcode: ")
			api_key = input("Provide your api_key: ") 
			url = "https://api.openweathermap.org/data/2.5/weather?zip=%s,us&appid=%s" % (zip_code, api_key)
			
			
			
			if (last_record[1] == request_limit):
				# find the greatest id 
				time_diff = datetime.datetime.now() - last_record[2] 
				if (time_diff.days > 0):
					print('New day: permsion to request data granted')
					new_timelog_values = [last_record[0], 0, None, last_record[3]+1]
					new_timelog_record = dict(zip(timelog_attribute, new_timelog_values))
					if (insert(db_connector, query_tables[0], timelog_attribute, new_timelog_record)):
						print('New data inserted')
					else:
						print('Could not insert')
				else:
					print('Perhaps out of requests. Check your email.')
			elif(last_record[1] < request_limit):
				# YYYY-MM-DD hh:mm:ss
				new_data = update_timelog_data(last_record)

				new_timelog_record = timelog_record(new_data, last_record , timelog_attribute)
				remove_record(db_connector, query_tables[0], 'local_limit = {0}'.format(last_record[1]))
				if (insert(db_connector, query_tables[0], timelog_attribute, new_timelog_record)):
					print('Data in timelog updated')
				else:
					print('Exceeded number of requests')
				db_connect.close()
			else:
				print('Table value error')


		except mysql.connector.Error as err:
			print('main error: {0}'.format(err))
	else:
		print('Main did not execute because import failed')


if __name__ == '__main__':
	main()