try:
	import datetime
	import mysql.connector
	from mysql.connector import errorcode

except Exception as e:
	print('E {0}'.format(e))

def table_description(db_connector, table_name):
	# example output
	'''[['total_limit', 'int', 'YES', '', None, ''], ['local_limit', 'int', 'YES', '', None, ''], ['local_limit_time', 'timestamp', 'YES', '', None, ''], ['id', 'int', 'NO', '', None, '']]'''
	try:
		cursor = db_connector.cursor()
		query = 'DESCRIBE {0}'.format(table_name)

		cursor.execute(query)
		isBeginning = True

		content = []
		for element in cursor:
			content.append(list(element))
			if type(content[(len(content) - 1)][1]) == bytes:
				content[(len(content) - 1)][1] = (("{0}".format(content[(len(content) - 1)][1])).split(sep="'"))[1]
			else:
				pass
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_TABLEACCESS_DENIED_ERROR:
			print('You have not been given permission to add a table')
		elif err.errnbo == errorcode.ER_SYNTAX_ERROR:
			print('Check your syntax')
		else:
			print('Error: {0}'.format(err)) 

	return content

def remove_record(db_connector, table_name, condition):
	''' 
	table_name: 'table_name'
	attribute_list: ['attrib_one', ..., 'attrib_x']
	condition:  DELETE FROM timelog WHERE local_limit_time IS NULL;
	'''
	try:
		cursor = db_connector.cursor()
		success = True
		query_to_del = 'DELETE FROM {0} WHERE {1}'.format(table_name, condition)
		cursor.execute(query_to_del)
		
		db_connector.commit()
		cursor.close()
		pass
	except mysql.connector.Error as err:
		print('remove_record error: {0}'.format(err))
		success = False
		pass
	return success

def query(db_connector, select_column, condition, limit_records, table_name):
	try:
		''' 
		table_name ex: 'name_of_table' type: string
		limit_records ex: 10 a feasible type: int 
		condition ex: 'column = 3 and ...' type: string
		select_column ex: 'column_name_0, ...' type: string 
		'''
		cursor = db_connector.cursor()
		query = None
		content = ''
		isBeginning = True
		success = False

		if condition == None:
			query = "SELECT {0} FROM {1} LIMIT {2}".format(select_column, table_name, limit_records)
		else:
			query = "SELECT {0} FROM {1} WHERE {2} LIMIT {3}".format(select_column, table_name, condition, limit_records)

		cursor.execute(query)
		content = []
		for element in cursor:
			content.append(element)
		

	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_TABLEACCESS_DENIED_ERROR:
			print('You have not been given permission to add a table')
		elif err.errno == errorcode.ER_SYNTAX_ERROR:
			print('Check your syntax')
		else:
			print('Error: {}'.format(err))
	finally:
		cursor.close()
		if content != '':
			success = True
			

	return content
def insert(db_connector, table_name, attributes, record):
	# table_name: 'table_name'
	# attribute ex: ['total_limit', 'local_limit', 'local_limit_time']
	# record ex: 
	#   record =  {
	# 		'total_limit': 3,
	# 		'local_limit': 3,
	# 		'local_limit_time': datetime.datetime(2022, 1, 22, 14, 1, 21)
	# 	}

	try:
		cursor = db_connector.cursor()
		record_types = ''
		isBeginning = True
		success = False
		for element in attributes:
			if not(isBeginning):
				record_types = '{0}, %({1})s'.format(record_types, element)
			else: 
				isBeginning = False
				record_types = '%({0})s'.format(element)


		insert_record = "INSERT INTO {0} ({1}) VALUES ({2})".format(table_name, ', '.join(attributes), record_types)
		
		
		cursor.execute(insert_record, record)
		db_connector.commit()
		cursor.close()
		success = True
	except mysql.connector.Error as err:
		if err.errno == errorcode.ER_TABLEACCESS_DENIED_ERROR:
			print('You have not been given permission to add a table')
		elif err.errno == errorcode.ER_SYNTAX_ERROR:
			print('Check your syntax')
		else:
			print('insert Error: {0}'.format(err)) 
	return success
