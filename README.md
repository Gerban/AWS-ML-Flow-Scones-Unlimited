### AWS ML Flow project to build a classification model for image classification for Scones Unlimited

### Software Requirements
- Python Kernel: Python 3, Instance: ml.t3.medium, Image: Data Science 
- Python 3.9 runtime for AWS Lambda functions
- JupyterLab on AWS

### Project Steps
- Import images for 133 different categories and filter out only type bicycle and motorcycle
- Train a classification model, save model, build endpoint configuration and deploy endpoint
- Build three lambda functions: first function imports and reformats image, second function 
deploys endpoint using the trained classification model and generates an inference, third lambda 
function checks whether the inference meets a tolerance threshold. A high threshold of 0.93 was used.
- Combined the three lambda functions into one step function that can be used to run test cases
of randomly selected images to make inferences. 
- The inferences outputs for test cases are captured and plots are used to highlight how many test cases
meet the accuracy threshold. Another plot shows the predicted values for each of the test images. 

### Documents
- READMD.MD: file that contains project information and files included
- MLflow_SconesUnlimted_AG.ipynb: project notebook based on supplied 'starter.ipynb' code 
that contains the project steps
- lambda.py: contains code of the three lambda functions
- stepFunction.json: contains json code of the implemented step-function
- stepFunction_TestImage_Pass.png: a saved image of step functions with all lamdba functions passing for a prediction that meets 0.93 threshold
- stepFunction_TestImage_Fail.png: a saved image of step function with last lambda function failing due 
to prediction not meeting the required threshold of 0.93
