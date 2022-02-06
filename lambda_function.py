import constants
import urllib
import aws_utility
import time
import transaction_processor


def lambda_handler(event, context):
    for record in event['Records']:

        if record['eventSource'] != 'aws:s3':
            print('Trigger is not from s3. Skipping Processing')
            return

        start_time = time.strftime('%Y%m%d_%H%M%S')
        bucket_name = record['s3']['bucket']['name']

        # Get key replacing %xx of url-encoded value by equivalent character
        file_name = urllib.parse.unquote_plus(record['s3']['object']['key'], encoding="utf-8")

        try:
            sales_file_content, file_name = aws_utility.get_file_from_s3(bucket_name, file_name, with_delete=True)
        except Exception as e:
            end_time = time.strftime('%Y%m%d_%H%M%S')
            print('Error occurred while reading the file from s3.', e)
            error_message = f'Error reading file from s3. The error encountered is {str(e)}'
            aws_utility.send_sns_message(constants.SNS_TOPIC_ARN, constants.FAILED_SNS_SUBJECT, error_message)

            dynamo_data = {'StartTime': start_time, 'EndTime':end_time, 'FileName':file_name, 'Status': 'Failure',
                           'FailureReason': str(e), 'ErrorPhase': 'Reading s3 content from the reprocess bucket'}

            aws_utility.upload_to_dynamo(constants.DYNAMO_TABLE_NAME, dynamo_data)
            continue

        try:
            summarized_transaction, records_processed = transaction_processor.summarize_transaction(sales_file_content,
                                                                                                    file_name)
            transaction_processor.insert_to_rds(summarized_transaction, file_name)

        except Exception as e:
            end_time = time.strftime('%Y%m%d_%H%M%S')
            print(f'Error summarizing file: {file_name}.', e)
            aws_utility.upload_to_s3(sales_file_content, constants.ERROR_BUCKET, file_name)

            error_message = f'Error occurred while processing the file: {file_name}. ' \
                            f'Please check error file in Bucket: {constants.ERROR_BUCKET} with FileName: {file_name}.' \
                            f'\n\nThe error message encountered was {str(e)}'

            aws_utility.send_sns_message(constants.SNS_TOPIC_ARN, constants.FAILED_SNS_SUBJECT, error_message)
            dynamo_data = {'StartTime': start_time, 'EndTime': end_time, 'FileName': file_name, 'Status': 'Failure',
                           'FailureReason': str(e), 'ErrorPhase': 'Summarizing transaction and inserting to RDS'}

            aws_utility.upload_to_dynamo(constants.DYNAMO_TABLE_NAME, dynamo_data)
            continue

        end_time = time.strftime('%Y%m%d_%H%M%S')
        dynamo_data = {'StartTime': start_time, 'EndTime': end_time, 'FileName': file_name, 'Status': 'Success',
                       'RecordProcessed': records_processed}

        aws_utility.upload_to_dynamo(constants.DYNAMO_TABLE_NAME, dynamo_data)
        success_message = f'File: {file_name} is processed successfully. Summarized data is on rds and log in dynamodb'
        aws_utility.send_sns_message(constants.SNS_TOPIC_ARN, constants.SUCCESS_SNS_SUBJECT, success_message)
