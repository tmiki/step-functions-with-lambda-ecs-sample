APP_NAME        =  sam-input-output1
IMAGE_TAG       =  latest
STACK_NAME      = sam-sample-input-output
STACK_INFO_FILE = stack-info-cache_$(STACK_NAME).txt
PROFILE    ?= default

cloudwatch-logs-get-resource-policies:
	aws --profile $(PROFILE) logs describe-resource-policies

cloudwatch-logs-put-resource-policy:
	export _TMP_FILE=`mktemp` ; \
	echo $${_TMP_FILE} ; \
	export AWS_ACCOUNT_ID=`aws --profile $(PROFILE) sts get-caller-identity | jq -r .Account` ; \
	export AWS_REGION=`aws configure list | grep region | awk '{print $$2};'` ; \
	envsubst < ./resource-based-policies/cloudwatch-logs-resource-based-policy-sam-sample.json > $${_TMP_FILE} ; \
	aws --profile $(PROFILE) logs put-resource-policy --policy-name AWSLogDeliveryWriteSamSampleStateMachine --policy-document file://$${_TMP_FILE} ; \
	rm $${_TMP_FILE}

cfn-build:
	sam build --use-container -t statemachine-sam-sample-template.yaml

cfn-deploy-guided:
	sam deploy --guided --profile $(PROFILE)

cfn-deploy:
	sam deploy --profile $(PROFILE)

cfn-build-deploy: cfn-build cfn-deploy
