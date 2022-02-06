import pymysql
import constants
from transaction_processor import summarize_transaction


# Read file for the sample
with open('transaction.csv') as my_file:
    my_txn = ''.join(my_file.readlines())

summary_txn = summarize_transaction(my_txn, 'my_file')[0]
print(summary_txn)

connection = pymysql.connect(host=constants.RDS_HOST, user=constants.RDS_USER, passwd=constants.RDS_PASSWORD,
                             db=constants.RDS_DB_NAME)

# Create table for first time during insert
'''
print('Creating table')
with connection.cursor() as cursor:
    cursor.execute("CREATE TABLE IF NOT EXISTS test_table(product_name varchar(255), quantity int, amount double, revenue double, file_name varchar(255);")
print('-'* 102)
'''

# Insert data to database
'''
print('Inserting into table')
insert_to_rds(summary_txn)
'''

# Select record from database to validate
'''
with connection.cursor() as cursor:
    cursor.execute("SELECT * FROM test_table;")
    result = cursor.fetchall()

for row in result:
    print(row)
'''
