import datetime
import os

from apiclient import discovery
from google.oauth2 import service_account

PRIVATE_KEY = os.getenv("PRIVATE_KEY_GOOGLE")

auth_dict = {
    "type": "service_account",
    "project_id": "bot-studio-tech",
    "private_key_id": "87c471994c1bb3b35849036f49842d73129ce09e",
    "private_key": PRIVATE_KEY.encode().decode("unicode_escape"),
    "client_email": "botstudio-tech@bot-studio-tech.iam.gserviceaccount.com",
    "client_id": "103955099768311558135",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/botstudio-tech%40bot-studio-tech.iam.gserviceaccount.com",
}

scopes = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/spreadsheets",
]
credentials = service_account.Credentials.from_service_account_info(
    auth_dict, scopes=scopes
)
service = discovery.build("sheets", "v4", credentials=credentials)


def add_row_to_sheet(
    spreadsheet_id,
    case_id,
    activity_name,
    sorting,
    timestamp=None,
):
    range_ = "Sheet1!A1:D1"

    value_input_option = "RAW"

    insert_data_option = "INSERT_ROWS"
    if timestamp is None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    value_range_body = {
        "majorDimension": "ROWS",
        "values": [
            [case_id, activity_name, timestamp, sorting],
        ],
    }

    request = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=spreadsheet_id,
            range=range_,
            valueInputOption=value_input_option,
            insertDataOption=insert_data_option,
            body=value_range_body,
        )
    )
    return request.execute()


if __name__ == "__main__":
    _spreadsheet_id = "1sVAf5DBDOwOx2sg-ysUj7R7bdWNTphvl8YsjV1TeOR8"
    _case_id = "123"
    _activity_name = "test"
    _sorting = "1"

    for i in range(10):
        add_row_to_sheet(_spreadsheet_id, _case_id, i, _sorting)
