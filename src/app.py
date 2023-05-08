import json
import os
import traceback
from typing import List
import boto3


def handler(event, _):
    """Handle lambda event and trigger the execution of the Fargate task."""
    try:
        session = boto3.Session()

        client = session.client("ecs")

        event_body = event["body"]
        print(event_body)

        event_body = json.loads(event_body)

        env_override_list_of_dicts = _generate_update_env_vars_list_of_dicts(
            event_body=event_body
        )
        print(f"Environment variable override:\n{env_override_list_of_dicts}\n")

        response = client.run_task(
            cluster=os.getenv("ECS_CLUSTER_ARN"),
            networkConfiguration={
                "awsvpcConfiguration": {
                    "subnets": [os.getenv("SUBNET")],
                    "securityGroups": [
                        os.getenv("SECURITY_GROUP"),
                    ],
                    "assignPublicIp": "ENABLED",
                }
            },
            startedBy="dragondrop-lambda-https-trigger",
            taskDefinition=os.getenv("TASK_DEFINITION"),
            overrides={
                "containerOverrides": [
                    {
                        "name": os.getenv("CONTAINER_NAME"),
                        "environment": env_override_list_of_dicts,
                    },
                ],
            },
        )

        print(f"Response from ECS invocation:\n{response}\n")
        return {"statusCode": 201, "body": json.dumps(f"Success!")}
    except Exception as e:
        stack_trace = traceback.format_exc()

        print(f"Exception:{e}\n{stack_trace}")
        return {
            "statusCode": 500,
            "body": json.dumps(f"Internal error: {e}\n{stack_trace}"),
        }


def _generate_update_env_vars_list_of_dicts(event_body: dict) -> List[dict]:
    """
    Helper function to generate the right dict of environment variable overrides.
    """
    output_list_of_dicts = []

    for key, value in event_body.items():
        output_list_of_dicts.append(
            {
                "name": key,
                "value": str(value),
            }
        )

    return output_list_of_dicts
