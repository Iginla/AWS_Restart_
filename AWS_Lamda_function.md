
# AWS Lambda Function for Word Count

## Overview

In this guide, we'll walk through the steps to create an AWS Lambda function in Python. The function counts the number of words in a text file and reports the result via email using Amazon Simple Notification Service (SNS). Optionally, it also sends the result in an SMS.

**Note:** Ensure all resources are created in the same AWS Region.

## Steps

### 1. Create a Lambda Function

- Go to the AWS Management Console.
- Open the Lambda service.
- Click on "Create function."
- Choose "Author from scratch."
- Enter a name for your function.
- Choose Python as the runtime.
- In the "Function code" section, write or upload the Python code below:
    ![Alt text](amda_function.jpg)
  
    ```python'''
    

    import boto3
    import logging

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def lambda_handler(event, context):
    try:
        # Initialize clients
        s3 = boto3.client('s3')
        sns = boto3.client('sns')
        
        # Get the uploaded file details
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Read the content of the file
        response = s3.get_object(Bucket=bucket, Key=key)
        file_content = response['Body'].read().decode('utf-8')
        
        # Count words
        word_count = len(file_content.split())
        
        # Create response message
        response_message = f'The word count in the {key} file is {word_count}.'

        # Publish to SNS topic
        sns.publish(
            TopicArn='<Your-SNS-Topic-ARN>',
            Subject='Word Count Result',
            Message=response_message
        )

        logger.info(f'Successfully processed file: {key}')

        return {
            'statusCode': 200,
            'body': response_message
        }
    except Exception as e:
        logger.error(f'Error processing file: {key}. Error: {str(e)}')
        raise e

- Scroll down, configure the "Execution role" by selecting "Use an existing role" and choose the `LambdaAccessRole` role.
- Click on "Create function."

### 2. Create an S3 Bucket

- Go to the S3 service in the AWS Management Console.
- Click on "Create bucket."
- Enter a unique bucket name and choose the same region as your Lambda function.
- Click on "Create."

### 3. Configure S3 Event Trigger

- After creating the S3 bucket, go to the bucket details page.
- Click on the "Properties" tab.
- Scroll down to the "Event notifications" section and click on "Create event notification."
- Configure the event as follows:
    - Name: Enter a name for the event.
    - Events: Choose "All object create events."
    - Send to: Choose "Lambda function" and select the Lambda function you created.
- Click on "Save."

### 4. Create an SNS Topic

- Go to the SNS service in the AWS Management Console.
- Click on "Create topic."
- Enter a name and display name for your topic.
- Click on "Create topic."

### 5. Subscribe Email and SMS to SNS Topic

- In the SNS topic details page, click on "Create subscription."
- Enter your email address for email subscription and a phone number for SMS subscription.
- Confirm the subscriptions.

### 6. Test the Lambda Function

- Upload a sample text file to the S3 bucket.
- Monitor the CloudWatch Logs for your Lambda function to check for any errors.
- Check your email and SMS for the word count result.
  
### References
-  Kyle Stahl  "5 Minutes to Create an AWS Lambda Function to Stay Updated About COVID-19 in Your Area" Towards Data Science  Mar 17, 2020.
- AWS Lambda Documentation "https://docs.aws.amazon.com/lambda/"
- Amazon S3 "https://docs.aws.amazon.com/s3/"
- Rick Strahl "Getting Images into Markdown Documents and Weblog Posts with Markdown Monster" Mar 15, 2017.

**Note:** Replace `<Your-SNS-Topic-ARN>` with the actual ARN of the SNS topic you created.

