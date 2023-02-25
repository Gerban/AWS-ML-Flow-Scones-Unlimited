# Note for Step function:
#Once you have tested the lambda functions, save the code for each lambda function in a python script called ‘lambda.py’.
#With your lambdas in place, you can use the Step Functions visual editor to construct a workflow that chains them together.
# In the Step Functions console you’ll have the option to author a Standard step function Visually.
#When the visual editor opens, you’ll have many options to add transitions in your workflow. We’re going to keep it simple
# and have just one: to invoke Lambda functions. Add three of them chained together. For each one, you’ll be able to select
# the Lambda functions you just created in the proper order, filter inputs and outputs, and give them descriptive names.
#Make sure that you:
#Are properly filtering the inputs and outputs of your invokations (e.g. $.body)
#Take care to remove the error handling from the last function - it’s supposed to “fail loudly” for your operations colleagues!
#Take a screenshot of your working step function in action and export the step function as JSON for your submission package.

# First Lambda function: serializeImageData
import json
import boto3
import botocore
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""

    # Get the s3 address from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']

    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket, key, '/tmp/image.png')

    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())

    # Pass the data back to the Step Function
    print("Event:", event.keys())
    return {
        'statusCode': 200,
        'body': {
            "s3_bucket": bucket,
            "s3_key": key,
            "image_data": image_data,
            "inferences": []
        }
    }


# Second Lambda function: imageClassifier
import json
import boto3
runtime = boto3.client("runtime.sagemaker")
import base64

#import sagemaker
#from sagemaker.serializers import IdentitySerializer

# Fill this in with the name of your deployed model:
ENDPOINT = 'image-classification-2023-02-22-19-36-33-279'

def lambda_handler(event, context):
    # Decode the image data
    image = base64.b64decode(event['body']['image_data'])

    #Instantiate a Predictor
    predictor = runtime.invoke_endpoint(EndpointName=ENDPOINT, ContentType='application/x-image', Body=image)

    # Make a prediction:
    inferences = predictor['Body'].read().decode('utf-8')

    # Sagemaker version: would need Sagemaker package added as zip file
    #predictor = sagemaker.predictor.Predictor(ENDPOINT)
     
    ## For this model the IdentitySerializer needs to be "image/png"
    #predictor.serializer = IdentitySerializer("image/png")
    
    # Make a prediction: using sagemaker package 
    #inferences = predictor.predict(image)

    # We return the data back to the Step Function               
    inferences_json = json.loads(inferences)
    
    return {
        'statusCode': 200,
        'body': json.dumps(inferences_json)
    }


# Third Lambda function: lowConfInferenceFilter
import json

THRESHOLD = .93


def lambda_handler(event, context):
    # Grab the inferences from the event
    inferences = event['body']

    inferences = list(map(float, inferences[1:-1].split(',')))
    print(inferences)
    
    # Check if any values in our inferences are above THRESHOLD
    meets_threshold = any([x > THRESHOLD for x in inferences])

    # If our threshold is met, pass our data back out of the
    # Step Function, else, end the Step Function with an error
    if meets_threshold:
        pass
    else:
        raise ("THRESHOLD_CONFIDENCE_NOT_MET")

    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }


