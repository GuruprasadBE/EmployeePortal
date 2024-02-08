import boto3
def lambda_handler(event, context):
    event = eval(event['Records'][0]['Sns']['Message'])
    bucket = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    
    try:
        if 'emp' in filename:
            emp_details = filename.split('_')[0].split('-')
            name = emp_details[1]
            location = emp_details[2]
            
            email_subject = 'NewJoinee: %s from %s location' % (name, location)
            email_message = 'Image of new employee %s uploaded successfully' % (name)
        else:
            email_subject = 'New File Upload Notification'
            email_message = 'A file %s has been uploaded' % filename
    except Exception as e:
        email_subject = 'New File Upload Notification'
        email_message = 'A file %s has been uploaded. But this is from exception block: %s' % (filename, str(e))
    

    client = boto3.client('sns')
    response = client.publish(
        TargetArn="arn:aws:sns:ap-south-1:069449400210:capstone-snstopic",
        Message=email_message,
        MessageStructure='text',
        Subject=email_subject,
    )
