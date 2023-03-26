import os
import boto3
from typing import List


def handler(event, _):
    """Handle lambda event and trigger the execution of the Fargate task."""
    try:
        session = boto3.Session()

        client = session.client('ecs')

        env_override_list_of_dicts = _generate_update_env_vars_list_of_dicts(event=event)

        print(
            f"Environment variable override:\n{env_override_list_of_dicts}\n"
        )

        response = client.run_task(
            cluster=os.getenv("ECS_CLUSTER_ARN"),
            networkConfiguration={
                'awsvpcConfiguration': {
                    'subnets': [
                        os.getenv("SUBNET")
                    ],
                    'securityGroups': [
                        os.getenv("SECURITY_GROUP"),
                    ],
                    'assignPublicIp': 'ENABLED'
                }
            },
            startedBy="dragondrop-lambda-https-trigger",
            taskDefinition=os.getenv("TASK_DEFINITION"),
            overrides={
                'containerOverrides': [
                    {
                        "name": os.getenv("CONTAINER_NAME"),
                        'environment': env_override_list_of_dicts,
                    },
                ],
            },
        )

        print(f"Response from ECS invocation:\n{response}\n")
    except Exception as e:
        print(f"Exception: {e}")


def _generate_update_env_vars_list_of_dicts(event: dict) -> List[dict]:
    """
    Helper function to generate the right dict of environment variable overrides.
    """
    request_var_to_env_var = {
        "migration_history_storage": "MIGRATIONHISTORYSTORAGE",
        "terraform_providers": "PROVIDERS",
        "terraform_version": "TERRAFORMVERSION",
        "vcs_user": "VCSUSER",
        "vcs_repo": "VCSREPO",
        "vcs_system": "VCSSYSTEM",
        "vcs_base_branch": "VCSBASEBRANCH",
        "state_backend": "STATEBACKEND",
        "terraform_cloud_organization": "TERRAFORMCLOUDORGANIZATION",
        "s3_backend_bucket": "S3BACKENDBUCKET",
        "reviewers": "PULLREVIEWERS",
        "resource_white_list": "RESOURCEWHITELIST",
        "resource_black_list": "RESOURCEBLACKLIST",
        "is_module_mode": "ISMODULEMODE",
     }

    output_list_of_dicts = [
        {
            "name": "DRAGONDROP_JOBID",
            "value": event["job_run_id"],
        }
    ]

    for request_var in request_var_to_env_var.keys():
        if request_var in event:
            output_list_of_dicts.append(
                {
                    "name": f"DRAGONDROP_{request_var_to_env_var[request_var]}",
                    "value": f"{event[request_var]}"
                }
            )

    return output_list_of_dicts
