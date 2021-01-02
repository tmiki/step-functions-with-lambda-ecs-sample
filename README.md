# Overview
This project consists of 2 applications. There are some purposes below.

- How a Step Functions state machine work.
- How typical resource such as Lambda and ECS work along with Step Functions.
- How you can enable each AWS service put logs.

The most of commands are written in the Makefile of each application. Please check them if you know how it works in detail.

# How to build
## Prerequisites

1. Configure your AWS CLI.

Please ensure that your AWS CLI can invoke AWS APIs to the AWS account you want to use.  

```
$ aws --profile ${your profile} sts get-caller-identity
{
    "UserId": "AROA*****************:botocore-session-1609509422",
    "Account": "123456789012",
    "Arn": "arn:aws:sts::123456789012:assumed-role/YourAssumedRole/botocore-session-1609509422"
}
```

2. Install SAM CLI.

Please install the AWS SAM CLI by referring the document below.  

Installing the AWS SAM CLI - AWS Serverless Application Model  
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html

Check whether you can run the SAM CLI.  

```
$ sam --version
SAM CLI, version 1.15.0
```

3. Instal Docker.

Please install the Docker.

Install Docker Engine | Docker Documentation  
https://docs.docker.com/engine/install/

Check whether you can run the docker command.  

```
$ docker --version
Docker version 19.03.8, build afacb8b7f0
```

4. Set environment variables.

The Makefile always refers the environment variable "PROFILE" to decide which AWS CLI profile should be used.
Please run the export command before the make command in advance.

```
$ export PROFILE=${your AWS CLI profile}
```


## Deploy the sam-sample-input-output app.

1. Update CloudWatch Logs resource based policy.

```
$ cd ./sam-sample-input-output/
$ make cloudwatch-logs-put-resource-policy
```

2. Check your CloudWatch Logs resource based policy is updated.  

```
$ cd ./sam-sample-input-output/
$ make cloudwatch-logs-get-resource-policies
```

3. Build the SAM app.

```
$ cd ./sam-sample-input-output/
$ make cfn-build
```

4. Deploy the SAM app along with the guide.

At your first time, you need to run the "sam deploy" command with its guide.  
Please leave all values except the "AWS Region". You need to specify the AWS Region you want to deploy.

```
$ cd ./sam-sample-input-output/
$ make cfn-deploy-guided
```

Once you deploy the app, some configuration parametes are stored in the "samconfig.toml". Then you don't need to run the "sam deploy" command with its guide.


## Deploy the ecs-sample-input-output app.
### Create a CloudFormation Stack
1. Update CloudWatch Logs resource based policy.

```
$ cd ./ecs-sample-input-output/
$ make cloudwatch-logs-put-resource-policy
```

2. Check your CloudWatch Logs resource based policy is updated.  

```
$ cd ./ecs-sample-input-output/
$ make cloudwatch-logs-get-resource-policies
```

3. Create a CloudFormation stack.

```
$ cd ./ecs-sample-input-output/
$ make cfn-deploy
```

4. Check the outputs of the CloudFormation stack.

This make command fetch the Output variables of the CFn stack and save it into a local file.
Be sure that filename is described in the .gitignore file and therefore it won't be commited to the Git repository.

```
$ cd ./ecs-sample-input-output/
$ make cfn-cache-stackinfo

$ cat stack-info-cache_ecs-sample-input-output.txt
```

### Build a docker image and push it to the ECR repository.
1. Build a Docker image and check it.

```
$ cd ./ecs-sample-input-output/
$ make docker-image
```

```
$ make docker-run
```

```
$ make docker-run-with-fail
```

Make sure the command above will end up with the exit code 9. This behavior is intentional.  
Please also make note the make command decides your command has failed.  

2. Push the Docker image.

Please make sure your IAM entity (IAM User/IAM Role) used by the AWS CLI profile has necessary IAM permissions.
In other words, your IAM entity needs permissions changing/pulling/pushing ECR repositories.

```
$ cd ./ecs-sample-input-output/
$ make docker-ecr-pushimage
```

3. Run an ECS task.

Check whether the ECS task runs properly.

```
$ cd ./ecs-sample-input-output/
$ make run-ecs-task
```

# How to Run a Step Functions state machine
## Run the state machine of the sam-sample-input-output app.

1. Open the Step Functions Console and choose your region.

https://console.aws.amazon.com/states/home?region=us-east-1#/

2. Select a state machine whose name starts with "Sam*".

3. Click the **"Start execution"** button and put an Input JSON object.

You can find a sample Input JSON object in the "./sam-sample-input-output/events/" directory.  
Copy and paste it to the **Start execution Input** text box in the Step Functions console.  
Then, click the **"Start execution"** button.  

You can control the Lambda function by the Input parameter "LambdaInputOutputFunctionParameters.InputOutput2FunctionSucceed".
Other parameters are nothing but dummy.

4. Check the result of the state machine.


## Run the state machine of the ecs-sample-input-output app.

1. Open the Step Functions Console and choose your region.

https://console.aws.amazon.com/states/home?region=us-east-1#/

2. Select a state machine whose name starts with "Ecs*".

3. Click the **"Start execution"** button and put an Input JSON object.

You can find a sample Input JSON object in the "./ecs-sample-input-output/events/" directory.  
Copy and paste it to the **Start execution Input** text box in the Step Functions console.  
Then, click the **"Start execution"** button.  

You can control the Lambda function by the Input parameter "EcsInputOutputTaskParameters.EcsTask2Succeed".
Other parameters are nothing but dummy.

4. Check the result of the state machine.

