# ecs-fargate-task-http-trigger
Containerized Lambda function for triggering an ECS Fargate Task hosting the dragondrop engine.

## Purpose
ECS Fargate Tasks are the easiest way to host the dragondrop.cloud core container with serverless compute. Unfortunately, it is
not possible to trigger and configure an ECS Fargate Task dynamically via an HTTPS request, let alone without IAM credentials.

At dragondrop.cloud, we always want to avoid having access to customer credentials of any kind (in fact even our
free tier offering is hosted in our customer's cloud environment), and so storing GCP credentials to then generate
an auth token is not an option.

Instead, we can make an https request to a containerized Lambda function, which in turn handles executing the ECS Fargate Task. This repo
specifies the image for such a Lambda function.

## Quick Start (with Terraform)
Our Terraform module for the dragondrop.cloud proprietary container for our customers that wish to host the tool within AWS
also creates a Containerized Lambda that hosts the container created by this repository.

The repository that defines this module can be found [here](https://github.com/dragondrop-cloud/terraform-aws-dragondrop-compute).
