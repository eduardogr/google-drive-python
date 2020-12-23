import pickle
import os.path
import json

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from googledrive.models import GoogleApiClientHttpError
from googledrive.models import GoogleApiClientHttpErrorBuilder
from googledrive.mappers import GoogleFileDictToGoogleFile
from googledrive.exceptions import MissingGoogleDriveFolderException
from googledrive.exceptions import MissingGoogleDriveFileException

class GoogleAuth:

    def authenticate(self, credentials, scopes):
        """
        Obtaining auth with needed apis
        """
        creds = None
        # The file token.pickle stores the user's access
        # and refresh tokens, and is created automatically
        # when the authorization flow completes for the first time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials,
                    scopes)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return creds

class GoogleService:

    __services_by_id = {}
    __credentials = None

    def __init__(self, credentials_file, scopes):
        self.__credentials_file = credentials_file
        self.__scopes = scopes

    def get_service(self, service_id, service_version):
        if not service_id in self.__services_by_id:
            self.__services_by_id.update({
                service_id: {}
            })

        if not service_version in self.__services_by_id[service_id]:
            self.__services_by_id[service_id].update({
                service_version: build(
                    service_id,
                    service_version,
                    credentials=self.__get_credentials(),
                    cache_discovery=False)
            })

        return self.__services_by_id[service_id][service_version]

    def __get_credentials(self):
        if self.__credentials is None:
            self.__credentials = GoogleAuth().authenticate(
                self.__credentials_file,
                self.__scopes)
        return self.__credentials

class GoogleDrive(GoogleService):

    DRIVE_SERVICE_ID = 'drive'
    DRIVE_SERVICE_VERSION = 'v3'

    PERMISSION_ROLE_COMMENTER = 'commenter'

    MIMETYPE_FOLDER = 'application/vnd.google-apps.folder'
    MIMETYPE_DOCUMENT = 'application/vnd.google-apps.document'
    MIMETYPE_SPREADSHEET = 'application/vnd.google-apps.spreadsheet'

    FIELDS_BASIC_FILE_METADATA = 'id, name, parents, mimeType'
    FIELDS_FILE_METADATA = f'{FIELDS_BASIC_FILE_METADATA}, exportLinks'

    QUERY_IS_FOLDER = f"mimeType='{MIMETYPE_FOLDER}'"
    QUERY_IS_DOCUMENT = f"mimeType='{MIMETYPE_DOCUMENT}'"
    QUERY_IS_SPREADSHEET = f"mimeType='{MIMETYPE_SPREADSHEET}'"
    QUERY_IS_FILE = f"({QUERY_IS_SPREADSHEET} or {QUERY_IS_DOCUMENT})"

    #
    # Simple structures for cached responses
    #

    cached_get_file = {}
    cached_ls = {}

    def create_folder(self, name):
        file_metadata = {
            'name': name,
            'mimeType': GoogleDrive.MIMETYPE_FOLDER
        }
        drive_service = super().get_service(
            self.DRIVE_SERVICE_ID,
            self.DRIVE_SERVICE_VERSION
        )
        folder = drive_service.files().create(
            body=file_metadata,
            fields=self.FIELDS_BASIC_FILE_METADATA).execute()

        return GoogleFileDictToGoogleFile().google_file_dict_to_google_file(folder)

    def update_file_parent(self, file_id, current_parent, new_parent):
        drive_service = super().get_service(
            self.DRIVE_SERVICE_ID,
            self.DRIVE_SERVICE_VERSION
        )
        file_update = drive_service.files().update(
            fileId=file_id,
            addParents=new_parent,
            removeParents=current_parent)
        file_update.execute()

    def get_file_from_id(self, file_id: str):
        drive_service = super().get_service(
            self.DRIVE_SERVICE_ID,
            self.DRIVE_SERVICE_VERSION
        )
        try:
            google_file_dict = drive_service.files().get(
                fileId=file_id,
                fields=self.FIELDS_FILE_METADATA).execute()

            return GoogleFileDictToGoogleFile().google_file_dict_to_google_file(google_file_dict)
        except HttpError as e:
            http_error = GoogleApiClientHttpErrorBuilder().from_http_error(e)
            raise GoogleApiClientHttpErrorException(http_error)

    def list_files(self, page_token: str, query: str):
        drive_service = super().get_service(
            self.DRIVE_SERVICE_ID,
            self.DRIVE_SERVICE_VERSION
        )
        response = drive_service.files().list(
            q=query,
            pageSize=100,
            spaces='drive',
            corpora='user',
            fields=f'nextPageToken, files({self.FIELDS_BASIC_FILE_METADATA})',
            pageToken=page_token).execute()

        google_files = [
            GoogleFileDictToGoogleFile().google_file_dict_to_google_file(google_file_dict)
            for google_file_dict in response.get('files', [])]
        next_page_token = response.get('nextPageToken', None)

        return google_files, next_page_token

    def copy_file(self, file_id, new_filename):
        drive_service = super().get_service(
            self.DRIVE_SERVICE_ID,
            self.DRIVE_SERVICE_VERSION
        )
        results = drive_service.files().copy(
            fileId=file_id,
            body={
                'name': new_filename,
                'mimeType': self.MIMETYPE_DOCUMENT
            }
        ).execute()
        return results.get('id')

    def create_permission(self, document_id: str, role: str, email_address):
        drive_service = super().get_service(
            self.DRIVE_SERVICE_ID,
            self.DRIVE_SERVICE_VERSION
        )
        drive_service.permissions().create(
            fileId=document_id,
            body={
                'type': 'user',
                'emailAddress': email_address,
                'role': role,
            }
        ).execute()

    #
    # High level API access
    #

    def get_folder(self, name):
        query = GoogleDrive.QUERY_IS_FOLDER
        return self.__get_file(query, name)

    #
    # TODO: thinking about a speed up for this, it's very slow
    #
    def googledrive_ls(self, path: str):
        if path in self.cached_ls:
            return self.cached_ls[path]

        splitted_path = list(self.__split_path(path))

        if len(splitted_path) == 0:
            query = f"{GoogleDrive.QUERY_IS_FILE}"

        else:
            folder = self.get_folder(splitted_path[0])
            if folder is None:
                raise MissingGoogleDriveFolderException(
                        "Missing folder: {}".format(splitted_path[0]))

            for path_element in splitted_path[1:]:
                query = f"{GoogleDrive.QUERY_IS_FOLDER} and '{folder.id}' in parents"
                folder = self.__get_file(query, path_element)

                if folder is None:
                    raise MissingGoogleDriveFolderException(
                        "Missing folder: {}".format(path_element))

            query = f"{GoogleDrive.QUERY_IS_FILE} and '{folder.id}' in parents"

        google_files = self.__get_files(query)

        if google_files is not None:
            self.cached_ls.update({path: google_files})

        return google_files

    def googledrive_get_file(self, path: str):
        if path in self.cached_get_file:
            return self.cached_get_file[path]

        splitted_path = list(self.__split_path(path))

        if len(splitted_path) == 0:
            return None

        folder = self.get_folder(splitted_path[0])
        if folder is None:
            raise MissingGoogleDriveFolderException(
                        "Missing folder: {}".format(path[0]))

        path_elements = splitted_path[1 : len(splitted_path)-1]

        for path_element in path_elements:
            query = f"{GoogleDrive.QUERY_IS_FOLDER} and '{folder.id}' in parents"
            folder = self.__get_file(query, path_element)

            if folder is None:
                raise MissingGoogleDriveFolderException(
                    "Missing folder: {}".format(path_element))

        filename = splitted_path[len(splitted_path)-1]
        query = f"{GoogleDrive.QUERY_IS_FILE} and '{folder.id}' in parents" 
        google_file = self.__get_file(query, filename)

        if google_file is not None:
            self.cached_get_file.update({path: google_file})

        return google_file

    # TODO: this will be called for the touch command
    def create_file(self, path, mimetype):
        pass

    def __split_path(self, path):
        return filter(lambda x: x != '', path.split('/'))

    def __get_file(self, query: str, filename):
        files = self.__get_files(query)
        for google_file in files:
            if google_file.name == filename:
                return google_file
        return None

    def __get_files(self, query: str):
        try:
            page_token = None
            total_google_files = []
            while True:
                google_files, next_page_token = self.list_files(
                    page_token=page_token,
                    query=query
                )
                total_google_files = total_google_files + google_files

                if next_page_token is None:
                    return total_google_files
                else:
                    page_token = next_page_token
            return None
        except HttpError as e:
            http_error = GoogleApiClientHttpErrorBuilder().from_http_error(e)
            raise GoogleApiClientHttpErrorException(http_error)

class SheetsService(GoogleService):

    SHEETS_SERVICE_ID = 'sheets'
    SHEETS_SERVICE_VERSION = 'v4'

    cached_file_values = {}

    def create_spreadsheet(self, filename):
        file_metadata = {
            'properties': {
                'title': filename,
            }
        }
        sheets_service = super().get_service(
            self.SHEETS_SERVICE_ID,
            self.SHEETS_SERVICE_VERSION
        )
        spreadsheet = sheets_service.spreadsheets().create(
            body=file_metadata,
            fields='spreadsheetId').execute()
        return spreadsheet

    # TODO:
    # file = sheets_service.open_file(spreadheet_id)
    # values = file.readlines(rows_range)
    # for row in values:
    #   print(row)
    #
    def get_file_values(self, spreadsheet_id, rows_range):
        if spreadsheet_id is None:
            raise MissingGoogleDriveFileException('Missing file: {}'.format(spreadsheet_id))

        sheets_service = super().get_service(
            self.SHEETS_SERVICE_ID,
            self.SHEETS_SERVICE_VERSION
        )

        if spreadsheet_id in self.cached_file_values:
            if rows_range in self.cached_file_values[spreadsheet_id]:
                return self.cached_file_values[spreadsheet_id][rows_range]

        sheet = sheets_service.spreadsheets()

        try:
            result = sheet.values().get(
                spreadsheetId=spreadsheet_id,
                range=rows_range
            ).execute()
            values = result.get('values', [])

            if len(values) > 0:
                self.cached_file_values.update({
                    spreadsheet_id: {
                        rows_range: values
                    }
                })
            return values
        except HttpError as e:
            http_error = GoogleApiClientHttpErrorBuilder().from_http_error(e)
            raise GoogleApiClientHttpErrorException(http_error)

    def update_file_values(self, spreadsheet_id, rows_range, value_input_option, values):
        sheets_service = super().get_service(
            self.SHEETS_SERVICE_ID,
            self.SHEETS_SERVICE_VERSION
        )
        sheet = sheets_service.spreadsheets()

        value_range_body = {
            'values': values
        }
        result = sheet.values().update(
            spreadsheetId=spreadsheet_id,
            range=rows_range,
            valueInputOption=value_input_option,
            body=value_range_body
        ).execute()
        return result.get('values', [])

    #
    # High level API access
    #

    def open_file(self, spreadheet_id):
        pass

class DocsService(GoogleService):

    DOCS_SERVICE_ID = 'docs'
    DOCS_SERVICE_VERSION = 'v1'

    ELEMENTS = 'elements'
    START_INDEX = 'startIndex'
    END_INDEX = 'endIndex'

    PARAGRAPH = 'paragraph'
    HORIZONTAL_RULE = 'horizontalRule'

    TEXT_RUN = 'textRun'
    CONTENT = 'content'

    def get_document(self, document_id):
        docs_service = super().get_service(
            self.DOCS_SERVICE_ID,
            self.DOCS_SERVICE_VERSION
        )
        return docs_service.documents().get(documentId=document_id).execute()

    def batch_update(self, document_id, requests):
        docs_service = super().get_service(
            self.DOCS_SERVICE_ID,
            self.DOCS_SERVICE_VERSION
        )
        docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}).execute()

class FilesAPI(GoogleDrive, SheetsService, DocsService):
    '''
    Composition of google APIs
    '''

    def create_sheet(self, folder_parent, folder, filename: str):
        spreadsheet = super().create_spreadsheet(filename)
        spreadsheet_id = spreadsheet.get('spreadsheetId')
        super().update_file_parent(
            file_id=spreadsheet_id,
            current_parent=folder_parent,
            new_parent=folder.id
        )
        # TODO:
        # return create('/folder_parent/folder/filename', mimetype='blablabal.spreadsheet')
        return spreadsheet_id

    def get_file_rows_from_folder(self,
                                  foldername: str,
                                  filename: str,
                                  rows_range: str):
        file_path = f"/{foldername}/{filename}"
        google_file = super().googledrive_get_file(file_path)

        if google_file is None:
            raise MissingGoogleDriveFileException('Missing file: {}'.format(filename))

        values = super().get_file_values(
            google_file.id,
            rows_range)

        return values

    def empty_document(self, document_id, insert_index, end_index):
        document = super().get_document(document_id)
        content = document.get('body').get('content')

        # Empty file
        if end_index in range(0, 2) or \
            insert_index >= end_index:
            return

        requests = [
            {
                'deleteContentRange':{
                    'range': {
                        'segmentId': '',
                        'startIndex': insert_index,
                        'endIndex': end_index
                    }
                }
            }
        ]
        super().batch_update(document_id=document_id, requests=requests)
