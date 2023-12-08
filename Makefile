REPO_HOST = 977147366110.dkr.ecr.us-east-2.amazonaws.com
APP_NAME = opp-app
TAG = lastest
HOST_PORT = 80
CNTR_PORT = 80
REGION = us-east-2

image: Dockerfile
	docker build --platform linux/amd64 -t myimage .

ecr-login:
	aws ecr get-login-password --region $(REGION) | docker login --username AWS --password-stdin $(REPO_HOST)

pull-image-ec2:
	docker pull $(REPO_HOST)/$(APP_NAME):$(TAG)

run-app-ec2:
	docker run -d -p $(HOST_PORT):$(CNTR_PORT) $(REPO_HOST)/$(APP_NAME):$(TAG)