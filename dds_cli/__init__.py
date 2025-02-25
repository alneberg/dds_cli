"""DDS CLI."""

import datetime
import os
import pathlib
import pkg_resources
import prompt_toolkit
import rich.console


###############################################################################
# PROJECT SPEC ################################################# PROJECT SPEC #
###############################################################################

__title__ = "Data Delivery System"
__version__ = pkg_resources.get_distribution("dds_cli").version
__url__ = "https://www.scilifelab.se/data"
__author__ = "SciLifeLab Data Centre"
__author_email__ = "datacentre@scilifelab.se"
__license__ = "MIT"
__all__ = [
    "DDS_METHODS",
    "DDS_DIR_REQUIRED_METHODS",
    "DDS_KEYS_REQUIRED_METHODS",
    "DDSEndpoint",
    "FileSegment",
    "dds_questionary_styles",
]


###############################################################################
# VARIABLES ####################################################### VARIABLES #
###############################################################################

# Keep track of all allowed methods
DDS_METHODS = ["put", "get", "ls", "rm", "create", "add"]

# Methods to which a directory created by DDS
DDS_DIR_REQUIRED_METHODS = ["put", "get"]

# Methods which require a project ID
DDS_KEYS_REQUIRED_METHODS = ["put", "get"]

# Token related variables
TOKEN_FILE = pathlib.Path(os.path.expanduser("~/.dds_cli_token"))
TOKEN_MAX_AGE = datetime.timedelta(days=2)
TOKEN_WARNING_AGE = datetime.timedelta(days=1, hours=18)


###############################################################################
# CLASSES ########################################################### CLASSES #
###############################################################################


class DDSEndpoint:
    """Defines all DDS urls."""

    # Base url - local or remote
    BASE_ENDPOINT_LOCAL = "http://127.0.0.1:5000/api/v1"
    BASE_ENDPOINT_REMOTE = "https://dds.dckube.scilifelab.se/api/v1"
    BASE_ENDPOINT = (
        BASE_ENDPOINT_LOCAL if os.getenv("DDS_CLI_ENV") == "development" else BASE_ENDPOINT_REMOTE
    )

    # User creation
    USER_ADD = BASE_ENDPOINT + "/user/add"

    # Authentication - user and project
    ENCRYPTED_TOKEN = BASE_ENDPOINT + "/user/encrypted_token"

    # S3Connector keys
    S3KEYS = BASE_ENDPOINT + "/s3/proj"

    # File related urls
    FILE_NEW = BASE_ENDPOINT + "/file/new"
    FILE_MATCH = BASE_ENDPOINT + "/file/match"
    FILE_INFO = BASE_ENDPOINT + "/file/info"
    FILE_INFO_ALL = BASE_ENDPOINT + "/file/all/info"
    FILE_UPDATE = BASE_ENDPOINT + "/file/update"

    # Project specific urls

    # Listing urls
    LIST_PROJ = BASE_ENDPOINT + "/proj/list"
    LIST_FILES = BASE_ENDPOINT + "/files/list"
    LIST_PROJ_USERS = BASE_ENDPOINT + "/proj/users"

    # Deleting urls
    REMOVE_PROJ_CONT = BASE_ENDPOINT + "/proj/rm"
    REMOVE_FILE = BASE_ENDPOINT + "/file/rm"
    REMOVE_FOLDER = BASE_ENDPOINT + "/file/rmdir"

    # Encryption keys
    PROJ_PUBLIC = BASE_ENDPOINT + "/proj/public"
    PROJ_PRIVATE = BASE_ENDPOINT + "/proj/private"

    # Display facility usage
    USAGE = BASE_ENDPOINT + "/usage"
    INVOICE = BASE_ENDPOINT + "/invoice"

    # Project creation urls
    CREATE_PROJ = BASE_ENDPOINT + "/proj/create"

    TIMEOUT = 5


class FileSegment:
    """Defines information on signatures, file chunks, etc."""

    DDS_SIGNATURE = b"DelSys"
    SEGMENT_SIZE_RAW = 65536  # Size of chunk to read from raw file
    SEGMENT_SIZE_CIPHER = SEGMENT_SIZE_RAW + 16  # Size of chunk to read from encrypted file


# Custom styles for questionary
dds_questionary_styles = prompt_toolkit.styles.Style(
    [
        ("qmark", "fg:ansiblue bold"),  # token in front of the question
        ("question", "bold"),  # question text
        ("answer", "fg:ansigreen nobold bg:"),  # submitted answer text behind the question
        ("pointer", "fg:ansiyellow bold"),  # pointer used in select and checkbox prompts
        ("highlighted", "fg:ansiblue bold"),  # pointed-at choice in select and checkbox prompts
        ("selected", "fg:ansiyellow noreverse bold"),  # style for a selected item of a checkbox
        ("separator", "fg:ansiblack"),  # separator in lists
        ("instruction", ""),  # user instructions for select, rawselect, checkbox
        ("text", ""),  # plain text
        ("disabled", "fg:gray italic"),  # disabled choices for select and checkbox prompts
        ("choice-default", "fg:ansiblack"),
        ("choice-default-changed", "fg:ansiyellow"),
        ("choice-required", "fg:ansired"),
    ]
)

# Determine if the user is on an old terminal without proper Unicode support
dds_on_legacy_console = rich.console.detect_legacy_windows()
