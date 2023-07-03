# pylint: disable=unused-argument
# pylint: disable=bad-super-call

# No need pylint to shout here

from googledrive.api import GoogleService
from googledrive.api import GoogleDrive
from googledrive.api import SheetsService, DocsService
from googledrive.models import GoogleApiClientHttpError
from googledrive.exceptions import MissingGoogleDriveFolderException
from googledrive.exceptions import GoogleApiClientHttpErrorException


class MockGoogleService(GoogleService):

    __services_by_id = {}

    def __init__(self, credentials_file, scopes):
        self.__credentials_file = credentials_file
        self.__scopes = scopes

        super().__init__(credentials_file, scopes)

    def get_service(self, service_id, service_version):
        return self.__services_by_id[service_id][service_version]

    def set_service(self, service_id, service_version, service):
        if service_id not in self.__services_by_id:
            self.__services_by_id.update({service_id: {}})

        if service_version not in self.__services_by_id[service_id]:
            self.__services_by_id[service_id].update({service_version: None})

        self.__services_by_id[service_id][service_version] = service


class RawSheetsServiceMock:
    def spreadsheets(self):
        class Spreadsheets:
            def create(self, body, fields):
                class Create:
                    def execute(self):
                        return {}

                return Create()

            def values(self):
                class Values:
                    def get(self, spreadsheetId, range):
                        class Get:
                            def execute(self):
                                return {"values": ["something"]}

                        return Get()

                    def update(self, spreadsheetId, range, valueInputOption, body):
                        class Update:
                            def execute(self):
                                return {"values": []}

                        return Update()

                return Values()

        return Spreadsheets()


class RawGoogleListMock:
    def __init__(self, files=[]):
        self.files = files

    def execute(self):
        return {"files": self.files}


class RawGoogleServiceFilesMock:
    def __init__(self, raw_google_list_by_query):
        self.raw_google_list_by_query = raw_google_list_by_query

    def create(self, body, fields):
        class Create:
            def execute(self):
                return {}

        return Create()

    def update(self, fileId, addParents, removeParents):
        class Update:
            def execute(self):
                return {}

        return Update()

    def list(self, q, pageSize, spaces, corpora, fields, pageToken):
        return self.raw_google_list_by_query.get(q, RawGoogleListMock())

    def copy(self, fileId, body):
        class Copy:
            def execute(self):
                return {}

        return Copy()


class RawGoogleServiceMock:
    def __init__(self, raw_google_service_files):
        self.raw_google_service_files = raw_google_service_files

    def files(self):
        return self.raw_google_service_files

    def permissions(self):
        class Permissions:
            def create(self, fileId, body):
                class Create:
                    def execute(self):
                        return {}

                return Create()

        return Permissions()


class RawDocsServiceMock:
    def documents(self):
        class Documents:
            def get(self, documentId):
                class Execute:
                    def execute(self):
                        return

                return Execute()

            def batchUpdate(self, documentId, body):
                class Execute:
                    def execute(self):
                        return

                return Execute()

        return Documents()


class MockGoogleDrive(GoogleDrive):

    calls = {}
    googledrive_ls_response = {}
    googledrive_ls_raise_exceptions = []
    googledrive_get_file_response = {}
    googledrive_get_file_raise_exceptions = []

    def __init__(self):
        self.calls = {}
        self.response_files = []
        self.pages_requested = 0
        self.googledrive_ls_response = {}
        self.googledrive_ls_raise_exceptions = []
        self.googledrive_get_file_response = {}
        self.googledrive_get_file_raise_exceptions = []

    #
    # Mock interface
    #

    def create_folder(self, name):
        self.__update_calls("create_folder", params={"name": name})
        return {"folder": name}

    def create_file(self, path, mimetype):
        self.__update_calls("create_file", params={"path": path, "mimetype": mimetype})
        return {"file": name}

    def update_file_parent(self, file_id, current_parent, new_parent):
        self.__update_calls(
            "update_file_parent",
            params={
                "file_id": file_id,
                "current_parent": current_parent,
                "new_parent": new_parent,
            },
        )

    def list_files(self, page_token: str, query: str):
        self.__update_calls(
            "list_files", params={"page_token": page_token, "query": query}
        )
        if self.pages_requested > 0:
            self.pages_requested -= 1
            files = self.response_files
            next_page_token = "pagetoken::{}".format(self.pages_requested)
        else:
            files = []
            next_page_token = None

        return files, next_page_token

    def copy_file(self, file_id, new_filename):
        return "ID"

    def create_permission(self, document_id: str, role: str, email_address):
        self.__update_calls(
            "create_permission",
            params={
                "document_id": document_id,
                "role": role,
                "email_address": email_address,
            },
        )
        return

    def googledrive_ls(self, path: str):
        self.__update_calls("googledrive_ls", params={"path": path})

        if path in self.googledrive_ls_raise_exceptions:
            raise MissingGoogleDriveFolderException(f'Path "{path}" does not exist')

        return self.googledrive_ls_response.get(path, None)

    def googledrive_get_file(self, path: str):
        self.__update_calls("googledrive_get_file", params={"path": path})

        if path in self.googledrive_get_file_raise_exceptions:
            raise MissingGoogleDriveFolderException(f'File "{path}" does not exist')

        return self.googledrive_get_file_response.get(path, None)

    #
    # Testing Interface
    #

    def get_calls(self):
        return self.calls

    def set_pages_requested(self, pages_requested):
        self.pages_requested = pages_requested

    def set_googledrive_ls_response(self, path, response):
        self.googledrive_ls_response.update({path: response})

    def set_googledrive_ls_raise_exception(self, path):
        self.googledrive_ls_raise_exceptions.append(path)

    def clear_googledrive_ls_fixture(self):
        MockGoogleDrive.googledrive_ls_response = {}
        MockGoogleDrive.googledrive_ls_raise_exceptions = []

    def set_googledrive_get_file_response(self, path, response):
        self.googledrive_get_file_response.update({path: response})

    def set_googledrive_get_file_raise_exception(self, path):
        self.googledrive_get_file_raise_exceptions.append(path)

    def clear_googledrive_get_file_fixture(self):
        MockGoogleDrive.googledrive_get_file_response = {}
        MockGoogleDrive.googledrive_get_file_raise_exceptions = []

    def set_response_files(self, response_files):
        self.response_files = response_files

    def __update_calls(self, function, params):
        current_call_number = 0

        if function in self.calls:
            sorted_keys = sorted(self.calls[function].keys())
            sorted_keys.reverse()
            current_call_number = sorted_keys[0] + 1

            self.calls[function].update({current_call_number: params})
        else:
            self.calls.update({function: {current_call_number: params}})


class MockSheetsService(SheetsService):

    __get_file_values_will_raise_exception = []
    __get_file_values_response = {}

    def __init__(self):
        self.calls = {}
        self.__get_file_values_will_raise_exception = []

    def create_spreadsheet(self, filename):
        self.__update_calls("create_spreadsheet", params={"filename": filename})
        return {"spreadsheetId": filename}

    def get_file_values(self, spreadsheet_id, rows_range):
        if spreadsheet_id in self.__get_file_values_will_raise_exception:
            error = GoogleApiClientHttpError(
                code=429,
                message="this is a test error message",
                status=429,
                details=[],
                errors=[],
            )
            raise GoogleApiClientHttpErrorException(error)

        self.__update_calls(
            "get_file_values",
            params={"spreadsheet_id": spreadsheet_id, "rows_range": rows_range},
        )
        return self.__get_file_values_response.get(spreadsheet_id, [])

    def update_file_values(
        self, spreadsheet_id, rows_range, value_input_option, values
    ):
        self.__update_calls(
            "update_file_values",
            params={
                "spreadsheet_id": spreadsheet_id,
                "rows_range": rows_range,
                "value_input_option": value_input_option,
                "values": values,
            },
        )
        return {"values": ["whatever"]}

    def raise_exception_for_get_file_values_for_ids(self, spreadsheet_collection):
        self.__get_file_values_will_raise_exception = spreadsheet_collection

    def get_calls(self):
        return self.calls

    def set_get_file_values_response(self, spreadsheet_id, response):
        self.__get_file_values_response.update({spreadsheet_id: response})

    def __update_calls(self, function, params):
        current_call_number = 0

        if function in self.calls:
            sorted_keys = sorted(self.calls[function].keys())
            sorted_keys.reverse()
            current_call_number = sorted_keys[0] + 1

            self.calls[function].update({current_call_number: params})
        else:
            self.calls.update({function: {current_call_number: params}})


class MockDocsService(DocsService):

    end_index = 99
    start_index = 1

    def __init__(self):
        self.calls = {}
        self.end_index = 99
        self.start_index = 1

        super().__init__("")

    def get_document(self, document_id):
        self.__update_calls("get_document", params={"document_id": document_id})
        return {
            "body": {
                "content": [
                    {
                        "paragraph": {
                            "elements": [
                                {
                                    "horizontalRule": {},
                                    "endIndex": self.end_index,
                                    "startIndex": self.start_index,
                                },
                                {
                                    "textRun": {"content": "i am content"},
                                    "horizontalRule": {},
                                    "endIndex": self.end_index,
                                    "startIndex": self.start_index,
                                },
                            ]
                        }
                    }
                ]
            }
        }

    def batch_update(self, document_id, requests):
        self.__update_calls(
            "batch_update", params={"document_id": document_id, "requests": requests}
        )

    def get_calls(self):
        return self.calls

    def set_end_index(self, index):
        self.end_index = index

    def set_start_index(self, index):
        self.start_index = index

    def __update_calls(self, function, params):
        current_call_number = 0

        if function in self.calls:
            sorted_keys = sorted(self.calls[function].keys())
            sorted_keys.reverse()
            current_call_number = sorted_keys[0] + 1

            self.calls[function].update({current_call_number: params})
        else:
            self.calls.update({function: {current_call_number: params}})
