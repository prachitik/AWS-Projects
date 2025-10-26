import boto3
import os
import json
from PIL import Image
import io
from datetime import datetime

# Initialize AWS clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ImageMetadata')

def lambda_handler(event, context):
    print("===== Lambda Execution Started =====")

    try:
        # Log raw event
        print("Event received:", json.dumps(event))

        # Extract bucket and key from the S3 trigger event
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        print(f"Input bucket: {bucket}, Key: {key}")

        # Download image from S3
        print("Downloading image from S3...")
        response = s3.get_object(Bucket=bucket, Key=key)
        image_data = response['Body'].read()
        print(f"Successfully downloaded image: {key}, Size: {len(image_data)} bytes")

        # Open the image with Pillow
        img = Image.open(io.BytesIO(image_data))
        original_size = img.size
        print(f"Original image size: {original_size}")

        # Resize to thumbnail
        print("Resizing image to 128x128 thumbnail...")
        img.thumbnail((128, 128))
        buffer = io.BytesIO()
        img.save(buffer, 'JPEG')
        buffer.seek(0)
        print(f"Thumbnail created successfully. New size: {img.size}")

        # Define output path
        output_bucket = os.environ['OUTPUT_BUCKET']
        output_key = f"processed/thumb_{os.path.basename(key)}"
        print(f"Output bucket: {output_bucket}, Output key: {output_key}")

        # Upload processed image to S3
        print("Uploading processed image to S3...")
        s3.put_object(Bucket=output_bucket, Key=output_key, Body=buffer, ContentType='image/jpeg')
        print("Processed image uploaded successfully.")

        # Prepare metadata
        metadata = {
            'image_name': key,
            'processed_image_name': output_key,
            'original_width': original_size[0],
            'original_height': original_size[1],
            'processed_width': img.size[0],
            'processed_height': img.size[1],
            'input_bucket': bucket,
            'output_bucket': output_bucket,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }

        print("Metadata to insert into DynamoDB:", json.dumps(metadata, indent=2))

        # Insert metadata into DynamoDB
        print("Inserting metadata into DynamoDB...")
        table.put_item(Item=metadata)
        print("Metadata inserted successfully into DynamoDB.")

        print("===== Lambda Execution Completed Successfully =====")
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': '✅ Image processed and metadata saved successfully!',
                'metadata': metadata
            })
        }

    except Exception as e:
        print("❌ ERROR: An exception occurred during processing!")
        print("Exception details:", str(e))
        print("===== Lambda Execution Failed =====")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
