import json
import os
import traceback
from ast import literal_eval
from typing import List
import boto3


def handler(event, _):
    """Handle lambda event and trigger the execution of the Fargate task."""
    try:
        session = boto3.Session()

        client = session.client("ecs")

        print(event["body"])

        env_override_list_of_dicts = _generate_update_env_vars_list_of_dicts(
            event_body=literal_eval(event["body"])
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
    request_var_to_env_var = {
        "is_module_mode": "ISMODULEMODE",
        "migration_history_storage": "MIGRATIONHISTORYSTORAGE",
        "provider_versions": "PROVIDERS",
        "resource_white_list": "RESOURCEWHITELIST",
        "resource_black_list": "RESOURCEBLACKLIST",
        "reviewers": "PULLREVIEWERS",
        "s3_bucket_name": "S3BACKENDBUCKET",
        "state_backend": "STATEBACKEND",
        "terraform_cloud_organization_name": "TERRAFORMCLOUDORGANIZATION",
        "terraform_version": "TERRAFORMVERSION",
        "vcs_system": "VCSSYSTEM",
        "vcs_repo_name": "VCSREPO",
        "vcs_user": "VCSUSER",
        "vcs_base_branch": "VCSBASEBRANCH",
    }

    output_list_of_dicts = [
        {
            "name": "DRAGONDROP_JOBID",
            "value": event_body["job_run_id"],
        }
    ]

    for request_var in request_var_to_env_var.keys():
        if request_var in event_body:
            output_list_of_dicts.append(
                {
                    "name": f"DRAGONDROP_{request_var_to_env_var[request_var]}",
                    "value": f"{event_body[request_var]}",
                }
            )

    return output_list_of_dicts
