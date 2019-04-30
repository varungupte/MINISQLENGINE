#ROLL NUMBER:- 2018201003
#NAME:- VARUN GUPTA

from helper import printresult,crossproduct,crossproductutil,evaluate_aggregate_function
import sys
import re
import os

#ERROR CHECKING:-
#1- if the query is not ending with ; , it will throw an error.
#2- checking it against a pattern  ^select.*from.* . If it is not so, then error is thrown.
#3- if the coulmns specified in the aggregate function contains more than one column throwing the error
#4- if the tables specified are not present,then throw error and return
#5- checking if the field specified exists in any of the table specified or not. If not return.
#6- Tables cannot be more than 2.

#parsing the query
def parse(query,distinctflag,aggregatefunctionflag,starflag):

	#segregating fileds from the query
	fields = query.split('from')[0].replace('select', '').strip()

	# setting the distinct flag if the query contains the distinct flag
	if bool(re.match('^distinct.*', fields)):
		distinctflag = True
		fields = fields.replace('distinct', '').strip()

	# setting the aggregate flag if the query contains any aggregate functions
	if bool(re.match('^(sum|max|min|avg)\(.*\)', fields)):
		aggregatefunctionflag = fields.split('(')[0].strip()
		fields = fields.replace(aggregatefunctionflag, '').strip().strip('()')

	# storing the columns that are required
	fields = fields.split(',')
	for i in range(len(fields)):
		fields[i] = fields[i].strip()

	# if the coulmns specified in the aggregate function contains more than one column throwing the error
	if aggregatefunctionflag is not None and len(fields) > 1:
		print "Only one column need to be passed in aggregate function."
		return 

	# setting the star flag if length of column is one and it is equal to '*'
	if len(fields) == 1: 
		if fields[0] == '*':
			starflag = True

	# if there are more columns on which aggregate function has to be called then return
	if aggregatefunctionflag is not None and starflag == True:
		print "Only one column need to be passed in aggregate function."
		return 

	tables = query.split('from')[1].split('where')[0].strip().split(',')

	# storing the number of tables on which this query has to be called
	for i in range(len(tables)):
		tables[i] = tables[i].strip()

	# if the tables are not specified files then throw error and return
	for table in tables:
		if table not in metadata:
			print table+" not present."
			return 

	# checking if the field specified exists in any of the table specified or not. If not return
	if bool(re.match('^select.*from.*where.*', query)):
		if starflag is False:
			if ispresentfield(fields, tables) == 0:
				return

		whereclause = query.split('where')[1].strip()
		temp = whereclause.replace(' and ', ' ').replace(' or ', ' ')

		columnsincondition = re.findall(r"[a-zA-Z][\w\.]*", temp)
		columnsincondition = set(columnsincondition)
		columnsincondition = list(columnsincondition)

		if ispresentfield(columnsincondition, tables) == 0:
			return

		if starflag is False:
			for i in xrange(len(fields)):
				if len(fields[i].split('.')) == 1:
					for table in tables:
						appended_name = table + '.'
						if fields[i] not in metadata[table]['structure']:
							continue
						else:
							fields[i] = appended_name + fields[i]
							break

		for field in columnsincondition:
			if len(field.split('.')) == 1:
				for table in tables:
					if field not in metadata[table]['structure']:
						continue
					else:
						temp1 = table + '.' + field
						temp2 = ' ' + whereclause
						whereclause = re.sub('(?<=[^a-zA-Z0-9])(' + field + ')(?=[\(\)= ])', temp1, temp2).strip(' ')
		ressel=select(tables, whereclause)
		respro=project(ressel, fields, distinctflag, aggregatefunctionflag)
		printresult(respro,len(tables))

	else:
		if len(tables) > 2:
			print "Tables cannot be more than 2."
			return

		if starflag is not True:
			for field in fields:
				if field in metadata[tables[0]]['structure']:
					continue
				else:
					print field+" field doesn't exists."
					return

		respro=project(metadata[tables[0]], fields, distinctflag, aggregatefunctionflag)
		printresult(respro,len(tables)) 



# storing informatiomation from the .csv files to the global dictionary.
def readdataindict():
	for tablename in metadata:
		metadata[tablename]['table'] = []
		metadata[tablename]['name'] = tablename
		filename='./' + tablename + '.csv'
		if not os.path.exists(filename):
			print "Table doesn't exist"
			sys.exit()
		file = open(filename,'r')
		for line in file:
			row=[]
			for field in line.strip().split(','):
				row.append(int(field.strip('"')))
			metadata[tablename]['table'].append(row)



#flags to check the query contains distinct keyword, aggregate functions and star or not.
distinctflag = False
aggregatefunctionflag = None
starflag = False


#function that prints the required data based on the condition defined in the query
def select(tables, whereclause):
	if len(tables) == 1:
		joined_table = crossproduct(metadata[tables[0]], {'structure':[], 'table':[[]]})
	else:
		joined_table = crossproduct(metadata[tables[0]], metadata[tables[1]])
	if len(tables) > 2:
		for i in range(len(tables) - 2):
			joined_table = crossproduct(joined_table, metadata[tables[i + 2]])
	whereclause = re.sub('(?<=[\w ])(=)(?=[\w ])', '==', whereclause)
	conditions = whereclause.replace(" and ", ",").replace(" or ", ",").replace(')', '').replace('(', '')
	conditions = conditions.split(',')
	result_table = {}
	result_table['structure'] = []
	for x in joined_table['structure']:
		result_table['structure'].append(x)
	for condition in conditions:
		if bool(re.match('.*==.*[a-zA-Z]+.*', condition.strip())):
			temp1 = condition.strip().split('==')[0].strip()
			temp2 = condition.strip().split('==')[1].strip()
			join_cndn = (temp1, temp2)
			allconditions.append(join_cndn)
	for field in joined_table['structure']:
			whereclause = whereclause.replace(field, 'row[' + str(joined_table['structure'].index(field)) + ']')
	result_table['table'] = []
	for row in joined_table['table']:
		if eval(whereclause):
			result_table['table'].append(row)
	return result_table

# project utility function 
def projectutility(table, fields, distinctflag, aggregatefunctionflag, result_table):
	if fields[0] == '*':
			temp = []
			for x in table['structure']:
				temp.append(x)
			fields[:] = temp[:]

			for field_pair in allconditions:
				temp[:] = []
				for x in fields:
					if x != field_pair[1]:
						temp.append(x)

				fields[:] = temp[:]

	result_table['structure'] += fields
	field_indices = []

	for field in fields:
		ind = table['structure'].index(field)
		field_indices.append(ind)

	for row in table['table']:
		result_row = []
		for i in field_indices:
			result_row.append(row[i])
			# print result_row
		result_table['table'].append(result_row)

	if distinctflag==True:
		temp = sorted(result_table['table'])
		result_table['table'][:] = []
		for i in range(len(temp)):
			if i == 0 or temp[i] != temp[i-1]:
				result_table['table'].append(temp[i])

#function that prints the required column
def project(table, fields, distinctflag, aggregatefunctionflag):
	result_table = {}
	result_table['structure'] = []
	result_table['table'] = []
	if aggregatefunctionflag is not None:
		evaluate_aggregate_function(table, fields, distinctflag, aggregatefunctionflag,result_table)
	else:
		projectutility(table, fields, distinctflag, aggregatefunctionflag,result_table)
	return result_table


#function to check whether field is present 
def ispresentfield(fields,tables):
	for field in fields:
		field_flag = 0
		for table in tables:
			if field.split('.')[-1] in metadata[table]['structure']:
				if len(field.split('.')) == 2 and field.split('.')[0] == table:
					field_flag = field_flag + 1
				else:
					field_flag = field_flag + 1

		if field_flag < 1:
			print "Field is not present."
			return 0
	return 1

allconditions = []
metadata = {}
query=sys.argv[1]
query=query.strip('"').strip()

#fetching structurermation from metadata file that contains information regarding the file structure of each table.
filename='./metadata.txt'
if not os.path.exists(filename):
	print "File doesn't exist"
	sys.exit()
file = open(filename,'r')
row = file.readline().strip()
while row:
	if row == "<begin_table>":
		tablename=file.readline().strip()
		metadata[tablename] = {}
		metadata[tablename]['structure'] = []
		attr = file.readline().strip()
		while attr != "<end_table>":
			metadata[tablename]['structure'].append(attr)
			attr=file.readline().strip()
	row = file.readline().strip()

#filling the metadata structure with table information
readdataindict()

#if the query is not having at the semicolon at the end then return
if query[len(query) - 1] != ';':
	print "Query should end with semicolon."
	exit(0)
	
#if the query is not of predefined format then return
if bool(re.match('^select.*from.*', query)) is False:
	print "Please check the query typed.It is Invalid."
	exit(0)

#removing semicolon from the end
query = query.strip(';')

#parsing the query and printing the result
parse(query,distinctflag,aggregatefunctionflag,starflag)

while 1:
	print "Enter quit to exit or type the query to continue:-"
	query=raw_input();
	distinctflag = False
	aggregatefunctionflag = None
	starflag = False
	if query == "quit":
		sys.exit()
	#if the query is not having at the semicolon at the end then return
	if query[len(query) - 1] != ';':
		print "Query should end with semicolon."
		exit(0)
		
	#if the query is not of predefined format then return
	if bool(re.match('^select.*from.*', query)) is False:
		print "Please check the query typed.It is Invalid."
		exit(0)

	#removing semicolon from the end
	query = query.strip(';')

	#parsing the query and printing the result
	parse(query,distinctflag,aggregatefunctionflag,starflag)