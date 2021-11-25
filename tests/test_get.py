# Standard library
import unittest.mock
import copy

# Installed
import pytest
import requests

# Own modules
import dds_cli


@pytest.fixture
def get_runner(runner):
    """Run dds ls without a project specified."""

    def _run(cmd_list):
        return runner(cmd_list)

    yield _run


@pytest.fixture
def base_get_request():
    """A fixture that mocks the requests.get method for base.py.

    The functioned returned by this fixture takes parameters that adjust the status_code,
    return_json, ok, and side_effect.
    """
    with unittest.mock.patch.object(dds_cli.base.requests, "get") as mock_obj:

        def _request_mock(status_code, return_json=dict(), ok=True, side_effect=None):
            mock_returned_request = unittest.mock.MagicMock(status_code=status_code, ok=ok)
            if side_effect:
                mock_returned_request.json.side_effect = side_effect
            else:
                mock_returned_request.json.return_value = return_json
            mock_obj.return_value = mock_returned_request
            return mock_obj

        yield _request_mock


@pytest.fixture
def file_handler_get_request():
    """A fixture that mocks the requests.get method for base.py.

    The functioned returned by this fixture takes parameters that adjust the status_code,
    return_json, ok, and side_effect.
    """
    with unittest.mock.patch.object(dds_cli.file_handler_remote.requests, "get") as mock_obj:

        def _request_mock(status_code, return_json=dict(), ok=True, side_effect=None):
            mock_returned_request = unittest.mock.MagicMock(status_code=status_code, ok=ok)
            if side_effect:
                mock_returned_request.json.side_effect = side_effect
            else:
                mock_returned_request.json.return_value = return_json
            mock_obj.return_value = mock_returned_request
            return mock_obj

        yield _request_mock


def test_get_all(
    get_runner,
    base_get_request,
):
    """Test that the list command works when no project is specified nor returned."""
    base_get_request_OK = base_get_request(
        200,
        side_effect=[
            {"public": "project_public_key"},
            {"private": "project_private_key"},
            {
                "files": {
                    "dir_with_both_types/simple_file2.txt": {
                        "checksum": "7531965bb3ac5c2204c3c3875d292976184d78a3c44ecb7c12ffe841051d92e8",
                        "compressed": True,
                        "key_salt": "salt1",
                        "name_in_bucket": "dir_with_both_types/8c673557-f2fe-5338-996a-359a0e3bf107",
                        "public_key": "public_key1",
                        "size_original": 4083,
                        "size_stored": 1507,
                        "subpath": "dir_with_both_types",
                    },
                    "dir_with_both_types/simple_file3.txt": {
                        "checksum": "7531965bb3ac5c2204c3c3875d292976184d78a3c44ecb7c12ffe841051d92e8",
                        "compressed": True,
                        "key_salt": "salt2",
                        "name_in_bucket": "dir_with_both_types/d4aca206-f986-5dc3-afbc-794e7f38df99",
                        "public_key": "public_key2",
                        "size_original": 4083,
                        "size_stored": 1507,
                        "subpath": "dir_with_both_types",
                    },
                }
            },
        ],
    )
    print(base_get_request_OK.calls)
    result = get_runner(["get", "-p", "project_1", "-a"])
    print(result.stdout)
    print(result.stderr)
    print(result.exception)
    assert result.exit_code == 0
    list_request_OK.assert_called_with(
        dds_cli.DDSEndpoint.LIST_PROJ,
        headers=unittest.mock.ANY,
        params={"usage": False, "project": None},
    )

    assert "No project info was retrieved" in result.stderr
    assert "" == result.stdout
