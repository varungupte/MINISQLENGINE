#ROLL NUMBER:- 2018201003
#NAME:- VARUN GUPTA

# displaying the output.
def printresult(table,num_tables):
	f=open("output.txt","a+")
	printheader(table)
	f.write('|'.join(table['structure']))
	f.write('\n')
	for row in table['table']:
		output=[]
		for x in row:
			output.append(str(x))
		print '|'.join(output)
		f.write('|'.join(output))
		f.write('\n')
	f.write('\n')
	
#displaying the header
def printheader(table):
	print 'Result:-'
	print '<<<<<<<<<<<$>>>>>>>>>>'
	print '|'.join(table['structure'])
	print '<<<<<<<<<<<>>>>>>>>>>'

#function to find the cross product of the two tables.
def crossproduct(table1, table2):
	crosstable = {}
	crosstable['table'] = []
	crosstable['structure'] = []
	temp1 = crossproductutil(table1)
	temp2 = crossproductutil(table2)
	crosstable['structure'] = crosstable['structure'] + temp1 + temp2
	for row1 in table1['table']:
		for row2 in table2['table']:
			crosstable['table'].append(row1 + row2)
	return crosstable

# helping function to find the cross product.
def crossproductutil(table):
	temporary = []
	for field in table['structure']:
		if len(field.split('.')) == 1:
			temporary.append(table['name'] + '.' + field)
		else:
			temporary.append(field)
	return temporary

# project utility function that evaluates aggregate function on the field specified
def evaluate_aggregate_function(table, fields, distinctflag, aggregatefunctionflag,result_table):
	temp = []
	result_table['structure'].append(aggregatefunctionflag + "(" + fields[0] + ")")
	field_index = table['structure'].index(fields[0])
	for row in table['table']:
		temp.append(row[field_index])
	resultdictionary = {}
	if aggregatefunctionflag == 'sum':
		res=0
		for x in temp:
			res+=x
		resultdictionary[aggregatefunctionflag]=sum(temp)

	elif aggregatefunctionflag == 'max':
		res=temp[0]
		for x in temp:
			if x > res:
				res=x
		resultdictionary[aggregatefunctionflag]=res

	elif aggregatefunctionflag == 'avg':
		resultdictionary[aggregatefunctionflag]=(float(sum(temp)))/len(temp)

	elif aggregatefunctionflag == 'min':
		res=temp[0]
		for x in temp:
			if x < res:
				res=x
		resultdictionary[aggregatefunctionflag]=res
	result_table['table'].append([resultdictionary[aggregatefunctionflag]])