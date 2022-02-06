import boto3
import pymysql


def get_file_from_s3(bucket_name, file_name, with_delete=False):
    """
    Returns content of file from s3 on passing event record dictionary.
    On error notifies client and returns error code

    Args:
        bucket_name(str): Name of the bucket from which file has to be extracted
        file_name(str): Name of the file that has to be extracted from the bucket
        with_delete(bool): Parameter that signifies whether the original file has to be deleted or not
    Returns:
        tuple(str, str): File content and file name obtained from the event
    """
    try:
        s3 = boto3.client("s3")
        file_from_s3 = s3.get_object(Bucket=bucket_name, Key=file_name)
        file_content = file_from_s3["Body"].read().decode('utf-8-sig')

        if with_delete:
            delete_s3_file(bucket_name, file_name)

        return file_content, file_name

    except Exception as e:
        raise Exception(e)


def delete_s3_file(bucket, key):
    """
    Delete mentioned file from s3 bucket specified
    Args:
        bucket(str): Bucket name fom which file is to be deleted
        key(str): File which is to be deleted
    """
    try:
        s3_resource = boto3.resource('s3')
        s3_resource.Object(bucket, key).delete()

    except Exception as e:
        raise Exception(e)


def upload_to_s3(file_content, bucket_name, file_name):
    """This method stores the source poslog into the destination bucket

    Args:
        file_content(str): Content that has to be uploaded to s3
        bucket_name(str): S3 bucket where file has to be uploaded
        file_name(str): Name of file to which content has to be uploaded
    """
    try:
        s3_resource = boto3.resource('s3')
        object_handler = s3_resource.Object(bucket_name, file_name)
        object_handler.put(Body=bytes(file_content, encoding="utf-8"))
    except Exception as e:
        raise Exception(e)


def send_sns_message(sns_topic_arn, sns_subject, sns_message):
    """
    Sends provided message to sns topic with subject as provided.
    Args:
        sns_topic_arn(str): SNS topic to which message has to be sent
        sns_subject(str): SNS subject that has to be sent in topic
        sns_message(str): SNS message that has to be sent to topic
    """
    try:
        sns_client = boto3.client('sns')
        sns_client.publish(TopicArn=sns_topic_arn, Message=sns_message, Subject=sns_subject)
    except Exception as e:
        raise Exception(e)


def upload_to_rds(conn, sql_query):

    with conn.cursor() as cur:
        cur.execute(sql_query)
        conn.commit()


def upload_to_dynamo(table_name, data_to_push):
    """
    Uploads data provided to mentioned table name
    Args:
        table_name(str): DynamoDB table name where data has to be inserted
        data_to_push(dict): Data that has to be pushed to dynamodb.
    """
    try:
        dynamodb_resource = boto3.resource('dynamodb')
        dynamodb_table = dynamodb_resource.Table(table_name)
        dynamodb_table.put_item(Item=data_to_push)
    except Exception as e:
        raise Exception(e)
