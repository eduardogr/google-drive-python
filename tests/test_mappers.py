from unittest import TestCase

from googledrive import mappers
from googledrive import models


class TestGoogleFileDictToGoogleFile(TestCase):
    def test_to_json(self):
        # given:
        google_file_dict = {"name": "id", "id": "name", "parents": "[]"}
        expected_google_file = models.GoogleFile(
            id="id", name="name", parents=[], mime_type="", export_links={}
        )
        sut = mappers.GoogleFileDictToGoogleFile()

        # when:
        json_dict = sut.google_file_dict_to_google_file(google_file_dict)

        # then:
        self.assertEqual(expected_google_file, json_dict)

    def test_to_json_when_is_none(self):
        # given:
        google_file_dict = None
        expected_google_file = None
        sut = mappers.GoogleFileDictToGoogleFile()

        # when:
        json_dict = sut.google_file_dict_to_google_file(google_file_dict)

        # then:
        self.assertEqual(expected_google_file, json_dict)
