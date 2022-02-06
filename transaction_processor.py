import constants
import pymysql


def summarize_transaction(transaction_data, file_name):
    """
    Summarizes the transaction and return summarized content
    Args:
        transaction_data(str): Transaction data to summarize
        file_name(str): Name of file in s3 containing data
    Returns:
        list: Summarized transaction message and total record count
    """
    summary_data = {}
    record_count = 0
    transaction_items = transaction_data.strip().split('\n')
    for transaction in transaction_items:
        record_count = record_count + 1
        product_name, quantity, amount, revenue = transaction.split(',')
        if product_name in summary_data.keys():
            current_quantity, current_amount, current_revenue = summary_data[product_name]
            summary_data[product_name] = current_quantity + int(quantity), current_amount + int(amount), \
                                         current_revenue + int(revenue)
        else:
            summary_data[product_name] = int(quantity), int(amount), int(revenue)

    # Store data as [('egg', 5, 100, 10, 'my_file'), ('apple', 1, 200, 20, 'my_file')]
    summary_list = [(key, *value, file_name) for key, value in summary_data.items()]

    return summary_list, record_count


def generate_sql_query(transaction_list):
    """
    Generates SQL query based on the transaction list and column names
    Args:
        transaction_list(list): List of summarized transaction data
    Returns:
        str: SQL query to insert data in database
    """
    column_names = constants.RDS_COLUMN_HEADERS
    data = str(transaction_list).strip('[]')
    sql_query = f'INSERT INTO {constants.TABLE_NAME}({column_names}) VALUES {data};'
    return sql_query


def insert_to_rds(summarized_transaction):
    """
    Inserts summarized transaction into rds database
    Args:
        summarized_transaction(list): List of transaction to insert into database
    """
    sql_query = generate_sql_query(summarized_transaction)
    connection = pymysql.connect(host=constants.DATABASE_HOST, user=constants.DATABASE_USER, passwd=constants.DATABASE_PASSWORD,
                                 db=constants.DATABASE_NAME)

    with connection:
        with connection.cursor() as cursor:
            # cursor.execute(f"CREATE TABLE {constants.TABLE_NAME}")
            cursor.execute(sql_query)
        connection.commit()
