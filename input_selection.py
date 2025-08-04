import boto3
import json

# Initialize the S3 client (uses credentials from your AWS CLI config)
s3 = boto3.client('s3')

# Your S3 details
unit = "Sayma ve Olasılık"
subject = "Basit Olayların Olasılıkları"
sub_subject = "Olasılık"
title = "OLASILIK HESAPLAMA"

bucket_name = 'question-generation-doping'
object_key = f'math_lecture_notes/{unit}/{subject}/{sub_subject}/{title}.json'

# Retrieve the object
response = s3.get_object(Bucket=bucket_name, Key=object_key)

# Read the content as bytes and decode to string
content = response['Body'].read().decode('utf-8')

# Parse JSON
lecture = []
question = []
data = json.loads(content)
for obj in data["content"]:
    if obj["type"] == "info":
        lecture.append(obj["text"])
    elif obj["type"] == "text":
        question.append(obj["text"])

lecture = " ".join(lecture)
question = " ".join(question)

{
    "unit" : "Sayma ve Olasılık",
    "subject": "Basit Olayların Olasılıkları",
    "sub_subject": "Olasılık",
    "title": "OLASILIK HESAPLAMA"
}
