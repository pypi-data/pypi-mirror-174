import numpy as np
import json
import boto3
import json
from PIL import Image
from numpy import asarray

ENDPOINT_NAME = 'mbari315k'
model_height, model_width = 640, 640

test_image = '/Volumes/Tempbox/Lonny/benthic_test_images/20191104T235504Z--9faf7c89-2fef-4a13-bf8b-dc79ceb3f981.png'

rgba_image = Image.open(test_image)
rgb_image = rgba_image.convert('RGB').resize((model_width,model_height))
data = np.array(np.array(rgb_image).astype(np.float32))

payload = json.dumps([data.tolist()])

client = boto3.client('sagemaker-runtime')
response = client.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                   ContentType='application/json',
                                   Body=payload)

result = json.loads(response['Body'].read().decode())
print('Results: ', result)