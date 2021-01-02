SHELL           = /bin/bash
APP_NAME        = ecs-input-output1
IMAGE_TAG       = latest
STACK_NAME      = ecs-sample-input-output
STACK_INFO_FILE = stack-info-cache_$(STACK_NAME).txt
PROFILE    ?= default

docker-image:
	docker image build -t $(APP_NAME):$(IMAGE_TAG) ./input-output1

docker-run:
	docker container run $(APP_NAME):$(IMAGE_TAG)

docker-run-with-fail:
	docker container run $(APP_NAME):$(IMAGE_TAG) "This run will fail."

docker-image-check:
	docker container run -ti $(APP_NAME):$(IMAGE_TAG) /bin/bash

docker-login:
	_TMP_FILE=`mktemp` ; sed 's/^/export /' $(STACK_INFO_FILE) > $${_TMP_FILE} ; source $${_TMP_FILE} ; \
	aws --profile $(PROFILE) ecr get-login-password | docker login --username AWS --password-stdin $${CFN_ECR_LOGIN_URI}

docker-ecr-pushimage:
	# Only when the file $(STACK_INFO_FILE) exists, you can push your docker image.
	if test \! -f $(STACK_INFO_FILE) ; then exit 1 ; fi ;

	_TMP_FILE=`mktemp` ; sed 's/^/export /' $(STACK_INFO_FILE) > $${_TMP_FILE} ; source $${_TMP_FILE} ; \
	aws --profile $(PROFILE) ecr get-login-password | docker login --username AWS --password-stdin $${CFN_ECR_LOGIN_URI}

	_TMP_FILE=`mktemp` ; sed 's/^/export /' $(STACK_INFO_FILE) > $${_TMP_FILE} ; source $${_TMP_FILE} ; \
	docker image tag $(APP_NAME):$(IMAGE_TAG) $${CFN_ECR_URI} ; \
	docker image push $${CFN_ECR_URI} ; \
	rm $${_TMP_FILE}

cloudwatch-logs-get-resource-policies:
	aws --profile $(PROFILE) logs describe-resource-policies

cloudwatch-logs-put-resource-policy:
	export _TMP_FILE=`mktemp` ; \
	echo $${_TMP_FILE} ; \
	export AWS_ACCOUNT_ID=`aws --profile $(PROFILE) sts get-caller-identity | jq -r .Account` ; \
	export AWS_REGION=`aws configure list | grep region | awk '{print $$2};'` ; \
	envsubst < ./resource-based-policies/cloudwatch-logs-resource-based-policy-ecs-sample.json > $${_TMP_FILE} ; \
	aws --profile $(PROFILE) logs put-resource-policy --policy-name AWSLogDeliveryWriteEcsSampleStateMachine --policy-document file://$${_TMP_FILE} ; \
	rm $${_TMP_FILE}

cfn-validate:
	aws --profile ${PROFILE} cloudformation validate-template --template-body file://statemachine-ecs-sample-template.yaml

cfn-deploy: cfn-validate
	aws --profile ${PROFILE} cloudformation deploy \
	--stack-name ${STACK_NAME} \
	--template-file statemachine-ecs-sample-template.yaml \
	--capabilities CAPABILITY_IAM

cfn-delete:
	aws --profile $(PROFILE) cloudformation delete-stack \
	--stack-name ${STACK_NAME} \

cfn-cache-stackinfo:
	# Initialize $(STACK_INFO_FILE)
	@cp /dev/null $(STACK_INFO_FILE)

	# Fetch the CFn Stack ID
	@echo -n "CFN_STACK_ID=" >> $(STACK_INFO_FILE)
	@aws --profile $(PROFILE) cloudformation list-stacks --query 'StackSummaries[?StackName == `$(STACK_NAME)` && contains(StackStatus, `DELETE`) != `true`] | [0] | StackId' >> $(STACK_INFO_FILE)

	# Fetch the ECR URI
	@echo -n "CFN_ECR_URI=" >> $(STACK_INFO_FILE)
	@aws --profile $(PROFILE) cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey == `EcrUri`] | [0] | OutputValue' >> $(STACK_INFO_FILE)

	# Fetch the ECR Login URI
	@echo -n "CFN_ECR_LOGIN_URI=" >> $(STACK_INFO_FILE)
	@aws --profile $(PROFILE) cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey == `EcrLoginUri`] | [0] | OutputValue' >> $(STACK_INFO_FILE)

	# Fetch the ECS Cluster ID
	@echo -n "CFN_CLUSTER_ID=" >> $(STACK_INFO_FILE)
	@aws --profile $(PROFILE) cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey == `EcsClusterId`] | [0] | OutputValue' >> $(STACK_INFO_FILE)

	# Fetch the ECS Cluster ARN
	@echo -n "CFN_CLUSTER_ARN=" >> $(STACK_INFO_FILE)
	@aws --profile $(PROFILE) cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey == `EcsClusterArn`] | [0] | OutputValue' >> $(STACK_INFO_FILE)

	# Fetch the ECS Task Definition ARN
	@echo -n "CFN_TASK_DEFINITION_ARN=" >> $(STACK_INFO_FILE)
	@aws --profile $(PROFILE) cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey == `EcsTaskDefinitionArn`] | [0] | OutputValue' >> $(STACK_INFO_FILE)

	# Fetch the VpcSubnet1 ID.
	@echo -n "CFN_VPC_SUBNET1=" >> $(STACK_INFO_FILE)
	@aws --profile $(PROFILE) cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey == `VpcSubnet1`] | [0] | OutputValue' >> $(STACK_INFO_FILE)

	# Fetch the VpcSubnet2 ID.
	@echo -n "CFN_VPC_SUBNET2=" >> $(STACK_INFO_FILE)
	@aws --profile $(PROFILE) cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey == `VpcSubnet2`] | [0] | OutputValue' >> $(STACK_INFO_FILE)

	# Fetch the Security Group ID for internal use.
	@echo -n "CFN_SECURITY_GROUP_INTERNAL=" >> $(STACK_INFO_FILE)
	@aws --profile $(PROFILE) cloudformation describe-stacks --stack-name $(STACK_NAME) --query 'Stacks[0].Outputs[?OutputKey == `SecurityGroupInternal`] | [0] | OutputValue' >> $(STACK_INFO_FILE)

	# Print all IDs
	@cat $(STACK_INFO_FILE)

run-ecs-task:
	_TMP_FILE=`mktemp` ; sed 's/^/export /' $(STACK_INFO_FILE) > $${_TMP_FILE} ; source $${_TMP_FILE} ; \
	aws --profile $(PROFILE) ecs run-task \
	--launch-type "FARGATE" \
	--cluster $${CFN_CLUSTER_ID} \
	--task-definition $${CFN_TASK_DEFINITION_ARN} \
	--network-configuration "{\"awsvpcConfiguration\": {\"subnets\": [\"$${CFN_VPC_SUBNET1}\", \"$${CFN_VPC_SUBNET2}\"], \"securityGroups\": [\"$${CFN_SECURITY_GROUP_INTERNAL}\"], \"assignPublicIp\": \"ENABLED\"}}" ; \
	rm $${_TMP_FILE}

run-ecs-task-clean: cfn-cache-stackinfo run-ecs-task
