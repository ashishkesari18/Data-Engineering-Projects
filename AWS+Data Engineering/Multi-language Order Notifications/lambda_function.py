import boto3
import os

# Initialize AWS service clients
translate = boto3.client('translate')
ses = boto3.client('ses')
polly = boto3.client('polly')

def lambda_handler(event, context):
    # Extract data from event
    name = event['customer_name']
    email = event['email']
    lang = event['language_code']
    order_id = event['order_id']
    delivery_date = event['delivery_date']

    # Message in English
    english_msg = f"Hi {name}, your order {order_id} has shipped and will arrive by {delivery_date}. Thanks for shopping with Amazon."

    # Translate the message
    translated_msg = translate.translate_text(
        Text=english_msg,
        SourceLanguageCode='en',
        TargetLanguageCode=lang
    )['TranslatedText']

    # Send translated message via SES
    ses.send_email(
        Source=os.environ['SES_EMAIL'],
        Destination={'ToAddresses': [email]},
        Message={
            'Subject': {'Data': 'Order Shipped!'},
            'Body': {'Text': {'Data': translated_msg}}
        }
    )

    # Optional: Voice alert using Polly
    polly.synthesize_speech(
        Text=translated_msg,
        OutputFormat="mp3",
        VoiceId="Lupe"
    )

    return {
        "status": "success",
        "message": translated_msg
    }
