FROM amazon/amazon-ecs-sample

# Python3.8
RUN yum install -y amazon-linux-extras \
&&  amazon-linux-extras enable python3.8 \
&&  yum install -y python3.8

# Copy all files of the application into the Docker image.
RUN mkdir /app
COPY ./src/ /app/

WORKDIR /app

# ENTRYPOINT [ "sh", "-c" ]
ENTRYPOINT [ "/usr/bin/python3.8", "main.py" ]
# CMD ["/usr/bin/python3.8 main.py \"Hello from an ECS Task for Step Functions.\""]
CMD [ "--succeed", "Hello from an ECS Task for Step Functions." ]

