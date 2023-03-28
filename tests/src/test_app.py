"""Unit tests for _generate_update_env_vars_dict"""
from unittest import TestCase
from src.app import _generate_update_env_vars_list_of_dicts, _parse_event_body_to_dict


def test_generate_update_env_vars_dict():
    """
    Unit test for the _generate_update_env_vars_dict helper function
    """
    case = TestCase()

    input_dict = {
        "job_run_id": "example",
        "vcs_system": "github",
        "is_module_mode": "false",
    }

    expected_output_dict = [
        {
            "name": "DRAGONDROP_JOBID",
            "value": "example",
        },
        {
            "name": "DRAGONDROP_VCSSYSTEM",
            "value": "github",
        },
        {
            "name": "DRAGONDROP_ISMODULEMODE",
            "value": "false",
        },
    ]

    case.assertListEqual(
        expected_output_dict, _generate_update_env_vars_list_of_dicts(event=input_dict)
    )


def test_parse_event_body_to_dict():
    input_event_string = """{'version': '2.0', 'routeKey': '$default', 'rawPath': '/', 'rawQueryString': '', 'headers': {'x-amzn-lambda-proxying-cell': '0', 'content-length': '517', 'x-amzn-tls-version': 'TLSv1.2', 'x-forwarded-proto': 'https', 'x-forwarded-port': '443', 'x-forwarded-for': '21:6', 'x-amzn-lambda-proxy-auth': 'HmacSHA256, SignedHeaders=x-amzn-lambda-forwarded-client-ip;x-amzn-lambda-forwarded-host;x-amzn-lambda-proxying-cell, Signature=8=', 'accept': '*/*', 'x-amzn-lambda-forwarded-client-ip': '2:6', 'x-amzn-tls-cipher-suite': 'DJH', 'x-amzn-trace-id': 'Self=1-6;Root=1-64', 'host': 'mi.cell-1-lambda-url.us-.on.aws', 'content-type': 'application/json', 'x-amzn-lambda-forwarded-host': 'm.lambda-url.us.on.aws', 'accept-encoding': 'gzip, deflate', 'user-agent': 'python-requests/2.27.1'}, 'requestContext': {'accountId': 'anonymous', 'apiId': 'm', 'domainName': 'm.cell-1-lambda-url.us.on.aws', 'domainPrefix': 'm', 'http': {'method': 'POST', 'path': '/', 'protocol': 'HTTP/1.1', 'sourceIp': '::0', 'userAgent': 'python-requests/2.27.1'}, 'requestId': 'f4', 'routeKey': '$default', 'stage': '$default', 'time': '28/Mar/2023:00:45:12 +0000', 'timeEpoch': 1679964312356}, 'body': '{"job_run_id": "fe4", "reviewers": "{\\"email\\":\\"example@test.cloud\\",\\"first_name\\":\\"Example\\",\\"github_username\\":\\"ExampleUser\\",\\"id\\":\\"test-uuid\\",\\"invitation_status\\":\\"Account Confirmed\\",\\"is_active\\":true,\\"is_admin\\":true,\\"last_name\\":\\"Example\\",\\"organization_id\\":\\"example-uuid\\",\\"role\\":\\"Admin\\",\\"user_image\\":\\"https://avatars.githubusercontent.com/4\\"}", "resource_white_list": null}', 'isBase64Encoded': False}"""

    output = _parse_event_body_to_dict(event=input_event_string)

    assert output["reviewers"]["first_name"] == "Example"
    assert output["job_run_id"] == "fe4"
