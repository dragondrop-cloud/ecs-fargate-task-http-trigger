"""Unit tests for _generate_update_env_vars_dict"""
from unittest import TestCase
from src.app import _generate_update_env_vars_list_of_dicts


def test_generate_update_env_vars_dict():
    """
    Unit test for the _generate_update_env_vars_dict helper function
    """
    case = TestCase()

    input_dict = {
        "DRAGONDROP_JOBID": "example",
        "DRAGONDROP_ISMODULEMODE": "false",
        "DRAGONDROP_VCSSYSTEM": "github",
    }

    expected_output_dict = [
        {
            "name": "DRAGONDROP_JOBID",
            "value": "example",
        },
        {
            "name": "DRAGONDROP_ISMODULEMODE",
            "value": "false",
        },
        {
            "name": "DRAGONDROP_VCSSYSTEM",
            "value": "github",
        },
    ]

    case.assertListEqual(
        expected_output_dict,
        _generate_update_env_vars_list_of_dicts(event_body=input_dict),
    )
