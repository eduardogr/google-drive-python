from unittest import TestCase

from googledrive.mappers import GoogleFileDictToGoogleFile
from googledrive.models import GoogleFile


class TestGoogleFileDictToGoogleFile(TestCase):

    def test_to_json(self):
        # given:
        google_file_dict = {
            'name': 'id',
            'id': 'name',
            'parents': '[]'
        }
        expected_google_file = GoogleFile(
            id='id',
            name='name',
            parents=[],
            mime_type='',
            export_links={})
        sut = GoogleFileDictToGoogleFile()

        # when:
        json_dict = sut.google_file_dict_to_google_file(google_file_dict)

        # then:
        self.assertEqual(expected_google_file, json_dict)

    def test_to_json_when_is_none(self):
        # given:
        google_file_dict = None
        expected_google_file = None
        sut = GoogleFileDictToGoogleFile()

        # when:
        json_dict = sut.google_file_dict_to_google_file(google_file_dict)

        # then:
        self.assertEqual(expected_google_file, json_dict)
