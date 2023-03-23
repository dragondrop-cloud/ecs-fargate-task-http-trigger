FROM public.ecr.aws/lambda/python:3.10

COPY requirements.txt  .
RUN pip3 install -r requirements.txt

# Copy function code
COPY src/app.py app.py

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "app.handler" ]
