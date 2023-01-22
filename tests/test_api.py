from unittest import TestCase

from googledrive.api import FilesAPI, GoogleDrive
from googledrive.api import SheetsService, DocsService
from googledrive.models import GoogleFile
from googledrive.exceptions import MissingGoogleDriveFolderException
from googledrive.exceptions import MissingGoogleDriveFileException
from googledrive.exceptions import GoogleApiClientHttpErrorException

from tests.common.mocks import RawSheetsServiceMock
from tests.common.mocks import RawDocsServiceMock
from tests.common.mocks import RawGoogleListMock
from tests.common.mocks import RawGoogleServiceFilesMock
from tests.common.mocks import RawGoogleServiceMock
from tests.common.mocks import MockGoogleService
from tests.common.mocks import MockGoogleDrive, MockSheetsService
from tests.common.mocks import MockDocsService

class DocServiceSut(DocsService, MockGoogleService):
    'Inject a mock into the DocsService dependency'

    def __init__(self):
        super().__init__('', [])

class SheetsServiceSut(SheetsService, MockGoogleService):
    'Inject a mock into the SheetsService dependency'

    def __init__(self):
        super().__init__('', [])

class GoogleDriveSut(GoogleDrive, MockGoogleService):
    'Inject a mock into the GoogleDrive dependency'

    def __init__(self):
        super().__init__('', [])

class FilesAPISut(
        FilesAPI,
        MockGoogleDrive,
        MockSheetsService,
        MockDocsService):
    'Inject mocks into FilesAPI dependencies'

class TestGoogleDrive(TestCase):

    def setUp(self):
        self.sut = GoogleDriveSut()

        files_by_query = {
            '': RawGoogleListMock()
        }
        raw_google_service_files = RawGoogleServiceFilesMock(files_by_query)
        drive_service = RawGoogleServiceMock(raw_google_service_files)

        self.sut.set_service(
            GoogleDrive.DRIVE_SERVICE_ID,
            GoogleDrive.DRIVE_SERVICE_VERSION,
            drive_service
        )

    def test_create_folder_ok(self):
        name = ''

        self.sut.create_folder(name)

    def test_create_file_when_no_parent_ok(self):
        path = 'filename'
        mimetype = GoogleDrive.MIMETYPE_DOCUMENT

        self.sut.create_file(path, mimetype)

    def test_create_file_when_parent_ok(self):
        # given:
        parent_folder = 'parentfolder'
        path = f"{parent_folder}/filename"
        mimetype = GoogleDrive.MIMETYPE_DOCUMENT
        files = [
            {
                'name': parent_folder,
                'id': parent_folder,
                'parents': []
            }
        ]
        files_by_query = {
            GoogleDrive.QUERY_IS_FOLDER: RawGoogleListMock(files),
        }
        raw_google_service_files = RawGoogleServiceFilesMock(files_by_query)
        drive_service = RawGoogleServiceMock(raw_google_service_files)
        self.sut.set_service(
            GoogleDrive.DRIVE_SERVICE_ID,
            GoogleDrive.DRIVE_SERVICE_VERSION,
            drive_service
        )

        # when:
        self.sut.create_file(path, mimetype)

    def test_googledrive_ls_when_folder_no_exists(self):
        # when:
        with self.assertRaises(MissingGoogleDriveFolderException):
            self.sut.googledrive_ls('/unexistent')

    def test_googledrive_ls_when_for(self):
        # given:
        files = [
            {
                'name': 'basefolder',
                'id': 'basefolder',
                'parents': []
            }
        ]
        listed_files = [
            {
                'name': 'file_1',
                'id': 'file_1',
                'parents': ['basefolder']
            },
            {
                'name': 'file_2',
                'id': 'file_2',
                'parents': ['basefolder']
            }
        ]
        files_by_query = {
            "mimeType='application/vnd.google-apps.folder'": RawGoogleListMock(files),
            f"{GoogleDrive.QUERY_IS_FILE} and 'basefolder' in parents": RawGoogleListMock(listed_files)
        }
        raw_google_service_files = RawGoogleServiceFilesMock(files_by_query)
        drive_service = RawGoogleServiceMock(raw_google_service_files)

        self.sut.set_service(
            GoogleDrive.DRIVE_SERVICE_ID,
            GoogleDrive.DRIVE_SERVICE_VERSION,
            drive_service
        )

        # when:
        files = self.sut.googledrive_ls('/basefolder')

        # then:
        self.assertEqual(2, len(files))

    def test_googledrive_ls_when_for_none(self):
        # given:
        listed_files = [
            {
                'name': 'something',
                'id': 'something',
                'parents': []
            }
        ]
        files_by_query = {
            "mimeType='application/vnd.google-apps.folder'": RawGoogleListMock(listed_files)
        }
        raw_google_service_files = RawGoogleServiceFilesMock(files_by_query)
        drive_service = RawGoogleServiceMock(raw_google_service_files)

        self.sut.set_service(
            GoogleDrive.DRIVE_SERVICE_ID,
            GoogleDrive.DRIVE_SERVICE_VERSION,
            drive_service
        )

        # when:
        with self.assertRaises(MissingGoogleDriveFolderException):
            self.sut.googledrive_ls('/something/unexistent')

    def test_googledrive_ls_when_no_for(self):
        # given:
        listed_files = [
            {
                'name': 'file_1',
                'id': 'file_1',
                'parents': []
            },
            {
                'name': 'file_2',
                'id': 'file_2',
                'parents': []
            }
        ]
        files_by_query = {
            GoogleDrive.QUERY_IS_FILE: RawGoogleListMock(listed_files)
        }
        raw_google_service_files = RawGoogleServiceFilesMock(files_by_query)
        drive_service = RawGoogleServiceMock(raw_google_service_files)

        self.sut.set_service(
            GoogleDrive.DRIVE_SERVICE_ID,
            GoogleDrive.DRIVE_SERVICE_VERSION,
            drive_service
        )

        # when:
        files = self.sut.googledrive_ls('/')

        # then:
        self.assertEqual(2, len(files))

    def test_googledrive_get_file_when_incorrect_path(self):
        # when:
        google_file = self.sut.googledrive_get_file('/')

        # then:
        self.assertEqual(None, google_file)

    def test_googledrive_get_file_when_unexistent_file(self):
        # when:
        with self.assertRaises(MissingGoogleDriveFolderException):
            self.sut.googledrive_get_file('/unexistent/path/file')

    def test_googledrive_get_file_for(self):
        # given:
        files = [
            {
                'name': 'base',
                'id': 'base',
                'parents': []
            },
            {
                'name': 'path',
                'id': 'path',
                'parents': ['base']
            }
        ]
        listed_files = [
            {
                'name': 'file_1',
                'id': 'file_1',
                'parents': ['path']
            },
            {
                'name': 'existent_file',
                'id': 'existent_file',
                'parents': ['path']
            }
        ]
        files_by_query = {
            GoogleDrive.QUERY_IS_FOLDER: RawGoogleListMock(files),
            f"{GoogleDrive.QUERY_IS_FOLDER} and 'base' in parents": RawGoogleListMock(files),
            f"{GoogleDrive.QUERY_IS_FILE} and 'path' in parents": RawGoogleListMock(listed_files)
        }
        raw_google_service_files = RawGoogleServiceFilesMock(files_by_query)
        drive_service = RawGoogleServiceMock(raw_google_service_files)

        self.sut.set_service(
            GoogleDrive.DRIVE_SERVICE_ID,
            GoogleDrive.DRIVE_SERVICE_VERSION,
            drive_service
        )

        # when:
        file = self.sut.googledrive_get_file('/base/path/existent_file')

        self.assertEqual('existent_file', file.name)

    def test_googledrive_get_file_for_none(self):
        # given:
        files = [
            {
                'name': 'base',
                'id': 'base',
                'parents': []
            }
        ]
        files_by_query = {
            GoogleDrive.QUERY_IS_FOLDER: RawGoogleListMock(files),
            f"{GoogleDrive.QUERY_IS_FOLDER} and 'base' in parents": RawGoogleListMock(),
        }
        raw_google_service_files = RawGoogleServiceFilesMock(files_by_query)
        drive_service = RawGoogleServiceMock(raw_google_service_files)

        self.sut.set_service(
            GoogleDrive.DRIVE_SERVICE_ID,
            GoogleDrive.DRIVE_SERVICE_VERSION,
            drive_service
        )

        # when:
        with self.assertRaises(MissingGoogleDriveFolderException):
            self.sut.googledrive_get_file('/base/unexistent/unexistent_file')

    def test_googledrive_get_file_no_for(self):
        # given:
        files = [
            {
                'name': 'base',
                'id': 'base',
                'parents': []
            }
        ]
        listed_files = [
            {
                'name': 'file_1',
                'id': 'file_1',
                'parents': ['path']
            },
            {
                'name': 'existent_file',
                'id': 'existent_file',
                'parents': ['path']
            }
        ]
        files_by_query = {
            GoogleDrive.QUERY_IS_FOLDER: RawGoogleListMock(files),
            f"{GoogleDrive.QUERY_IS_FILE} and 'base' in parents": RawGoogleListMock(listed_files)
        }
        raw_google_service_files = RawGoogleServiceFilesMock(files_by_query)
        drive_service = RawGoogleServiceMock(raw_google_service_files)

        self.sut.set_service(
            GoogleDrive.DRIVE_SERVICE_ID,
            GoogleDrive.DRIVE_SERVICE_VERSION,
            drive_service
        )

        # when:
        file = self.sut.googledrive_get_file('/base/existent_file')

        self.assertEqual('existent_file', file.name)

    def test_update_file_parent_ok(self):
        file_id = 'ID'
        current_parent = 'father'
        new_parent = 'i am your father'

        self.sut.update_file_parent(file_id, current_parent, new_parent)

    def test_list_files_ok(self):
        page_token = ''
        query = ''

        self.sut.list_files(page_token, query)

    def test_copy_file_ok(self):
        file_id = 'EFAWEF'
        new_filename = 'brand new file'

        self.sut.copy_file(file_id, new_filename)

    def test_create_permission_ok(self):
        document_id = 'ASDFASDF'
        role = 'comenter'
        email_address = 'myemail@email.com'

        self.sut.create_permission(document_id, role, email_address)


class TestSheetsService(TestCase):

    def setUp(self):
        self.sut = SheetsServiceSut()
        self.sut.set_service(
            SheetsService.SHEETS_SERVICE_ID,
            SheetsService.SHEETS_SERVICE_VERSION,
            RawSheetsServiceMock()
        )

    def test_create_spreadsheet_ok(self):
        file_metadata = {}
        self.sut.create_spreadsheet(file_metadata)

    def test_get_file_values_ok(self):
        spreadsheet_id = 'id'
        self.sut.get_file_values(spreadsheet_id, 'A1:D3')

    def test_get_file_values_ok_when_cached(self):
        spreadsheet_id = 'id'

        self.sut.get_file_values(spreadsheet_id, 'A1:D3')
        self.sut.get_file_values(spreadsheet_id, 'A1:D3')

        # TODO: do assertion for cache

    def test_update_file_values_ok(self):
        spreadsheet_id = 'id'
        rows_range = 'A3:D4'
        value_input_option = 'RAW'
        values = []
        self.sut.update_file_values(spreadsheet_id, rows_range, value_input_option, values)


class TestDocsService(TestCase):

    def setUp(self):
        self.sut = DocServiceSut()
        self.sut.set_service(
            DocsService.DOCS_SERVICE_ID,
            DocsService.DOCS_SERVICE_VERSION,
            RawDocsServiceMock()
        )

    def test_get_document_ok(self):
        document_id = 'ID'

        self.sut.get_document(document_id)

    def test_batch_update(self):
        document_id = 'ID'
        requests = []

        self.sut.batch_update(document_id, requests)


class TestFilesAPI(TestCase):

    def setUp(self):
        self.sut = FilesAPISut()
        self.sut.raise_exception_for_get_file_values_for_ids([])

    def tearDown(self):
        self.sut.clear_googledrive_ls_fixture()
        self.sut.clear_googledrive_get_file_fixture()

    def test_create_folder(self):
        # given:
        folder_name = 'test folder'

        # when:
        self.sut.create_folder(folder_name)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(1, len(calls))
        self.assertIn('create_folder', calls)

        call = calls['create_folder'][0]
        self.assertIn('name', call)
        self.assertEqual(
            folder_name,
            call['name'])

    def test_create_spreadsheet(self):
        # given:
        folder_parent = 'parent'
        filename = 'filename'
        folder = GoogleFile(id='new_parent_id', name='folder', parents=[], mime_type='', export_links={})

        # when:
        self.sut.create_sheet(folder_parent, folder, filename)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(2, len(calls))

        self.assertIn('create_spreadsheet', calls)
        self.assertIn('update_file_parent', calls)

        call = calls['create_spreadsheet'][0]
        self.assertIn('filename', call)
        self.assertEqual(
            filename,
            call['filename'])

        call = calls['update_file_parent'][0]
        self.assertIn('file_id', call)
        self.assertIn('current_parent', call)
        self.assertIn('new_parent', call)
        self.assertEqual(
            filename,
            call['file_id'])
        self.assertEqual(
            folder_parent,
            call['current_parent'])
        self.assertEqual(
            'new_parent_id',
            call['new_parent'])

    def test_get_folder_when_not_exists(self):
        # given:
        folder_name = 'name'
        self.sut.set_pages_requested(0)

        # when:
        folder = self.sut.get_folder(folder_name)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(1, len(calls))

        self.assertEqual(None, folder)

    def test_correct_number_executions_when_get_folder_and_exists(self):
        # given:
        folder_name = 'my_folder'
        self.sut.set_pages_requested(1)
        self.sut.set_response_files([
            GoogleFile(id='some id', name=folder_name, parents=[], mime_type='', export_links={})
        ])

        # when:
        folder = self.sut.get_folder(folder_name)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(1, len(calls))
        self.assertIn('list_files', calls)

        self.assertEqual(folder_name, folder.name)

    def test_correct_query_when_get_folder(self):
        # given:
        folder_name = 'name'

        # when:
        self.sut.get_folder(folder_name)

        # when:
        calls = self.sut.get_calls()
        self.assertEqual(1, len(calls))
        self.assertIn('list_files', calls)

        self.assertEqual(
            GoogleDrive.QUERY_IS_FOLDER,
            calls['list_files'][0]['query']
        )

    def test_get_file_rows_from_folder(self):
        # given:
        foldername = 'my_folder'
        filename = 'filename'
        file_id = 'file_id'
        self.sut.set_googledrive_get_file_response(
            f"/{foldername}/{filename}",
            GoogleFile(id=file_id, name=filename, parents=[], mime_type='', export_links={}))
        rows_range = 'A2::F4'

        # when:
        self.sut.get_file_rows_from_folder(foldername, filename, rows_range)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(2, len(calls))

        self.assertIn('googledrive_get_file', calls)
        self.assertEqual(1, len(calls['googledrive_get_file']))
        self.assertIn('get_file_values', calls)
        self.assertEqual(1, len(calls['get_file_values']))

        call = calls['get_file_values'][0]
        self.assertEqual(file_id, call['spreadsheet_id'])

    def test_get_file_rows_from_folder_when_missing_google_folder_exception(self):
        # given:
        foldername = 'my_folder'
        filename = 'filename'
        rows_range = 'A2::F4'
        self.sut.set_googledrive_get_file_raise_exception(f"/{foldername}/{filename}")

        # when:
        with self.assertRaises(MissingGoogleDriveFolderException):
            self.sut.get_file_rows_from_folder(foldername, filename, rows_range)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(1, len(calls))
        self.assertIn('googledrive_get_file', calls)
        self.assertEqual(1, len(calls['googledrive_get_file']))

    def test_get_file_rows_from_folder_when_missing_google_file_exception(self):
        # given:
        foldername = 'my_folder'
        filename = 'filename'
        self.sut.set_googledrive_get_file_response(
            f"/{foldername}/{filename}",
            None)
        rows_range = 'A2::F4'

        # when:
        with self.assertRaises(MissingGoogleDriveFileException):
            self.sut.get_file_rows_from_folder(foldername, filename, rows_range)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(1, len(calls))
        self.assertIn('googledrive_get_file', calls)
        self.assertEqual(1, len(calls['googledrive_get_file']))

    def test_get_file_rows_when_ok(self):
        # given:
        file_id = 'file_id'
        rows_range = 'A2::F4'

        # when:
        self.sut.get_file_values(file_id, rows_range)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(1, len(calls))
        self.assertIn('get_file_values', calls)
        self.assertEqual(1, len(calls['get_file_values']))

    def test_get_file_rows_when_http_error(self):
        # given:
        file_id = 'file_id'
        rows_range = 'A2::F4'
        self.sut.raise_exception_for_get_file_values_for_ids([file_id])

        # when:
        with self.assertRaises(GoogleApiClientHttpErrorException):
            self.sut.get_file_values(file_id, rows_range)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(0, len(calls))

    def test_update_file_values_when_ok(self):
        # given:
        file_id = 'file_id'
        rows_range = 'A2::F4'

        # when:
        self.sut.update_file_values(file_id, rows_range, 'RAW', [])

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(1, len(calls))
        self.assertIn('update_file_values', calls)
        self.assertEqual(1, len(calls['update_file_values']))

    def test_empty_document_when_empty_file(self):
        # given:
        document_id = 'ID'
        start_index = 4
        end_index = 0

        # when:
        self.sut.empty_document(document_id, start_index, end_index)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(1, len(calls))
        self.assertIn('get_document', calls)

    def test_empty_document_when_document_exist(self):
        # given:
        document_id = 'ID'
        start_index = 0
        end_index = 4
        self.sut.set_start_index(start_index)
        self.sut.set_end_index(end_index)

        # when:
        self.sut.empty_document(document_id, start_index, end_index)

        # then:
        calls = self.sut.get_calls()
        self.assertEqual(2, len(calls))
        self.assertIn('get_document', calls)
        self.assertIn('batch_update', calls)
