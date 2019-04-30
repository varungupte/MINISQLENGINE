CSE441: DATABASE SYSTEMS

In this assignment, you are supposed to develop a mini​ sql engine which will run a subset
of SQL queries using ​ command line interface

Programming Languages Allowed : Java, Python and C/C++

Dataset:
1. csv files for tables.
a. If a file is : ​ File1.csv ​ , the table name would be File1
b. There will be no tab ​ separation or space ​ separation, so you are not required
to handle it but you have to make sure to take care of both csv file type
cases: the one where values are in double quotes and the one where values
are without quotes.
2. All the elements in files would be ​ only INTEGERS
3. A file named: ​ metadata.txt​ (note the extension) would be given to you which will
have the following structure for each table:
<begin_table>
<table_name>
<attribute1>
....
<attributeN>
<end_table>

Type of Queries:​​ ​ You’ll be presented with the following set of queries:

1. Select all records :
Select * from table_name;

2. Aggregate functions: Simple aggregate functions on a single column.
Sum, average, max and min. They will be very trivial given that the data is only
numbers:
Select max(col1) from table1;

3. Project Columns(could be any number of columns) from one or more tables :
Select col1, col2 from table_name;

4. Select/project with distinct from one table: (distinct of a pair of values indicates the
pair should be distinct)
Select distinct col1, col2 from table_name;

5. Select with where from one or more tables :
Select col1,col2 from table1,table2 where col1 = 10 AND col2 = 20;
a. In the where queries, there would be a maximum of one AND/OR operator
with no NOT operators.
b. Relational operators that are to be handled in the assignment, the operators
include "< , >, <=, >=, =".

6. Projection of one or more(including all the columns) from two tables with one join
condition :
a. Select * from table1, table2 where table1.col1=table2.col2;
b. Select col1, col2 from table1,table2 where table1.col1=table2.col2;
c. NO REPETITION OF COLUMNS – THE JOINING COLUMN SHOULD BE
PRINTED ONLY ONCE.

IMPORTANT:

● ERROR HANDLING​ : 10% marks will be for error handling.

● For the above queries, please note all the permutations and combinations of
SQL that MySQL permits, specially when it comes to multiple tables. What is
mentioned above are examples of what the queries could be.
Parser: You can use pre​ built parsers for SQL queries
Format of Input​ :
Command lines input such that: {compiled files} “SQL Query”.
Here SQL Query would be a command line argument. Example :

● For C++ it will be – ./a.out “select * from table_name where condition;”

● For Java it will be – java classfile.class “select * from table_name where condition;”

● For Python it will be – python RollNumber.py “select * from table_name where
condition;”
Format of Output:
<Table1.column1,Table1.column2....TableN.columnM>
Row1
Row2.......
RowN