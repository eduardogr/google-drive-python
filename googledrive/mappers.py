from googledrive.models import GoogleFile

class GoogleFileDictToGoogleFile:

    def google_file_dict_to_google_file(self, google_file_dict):
        if google_file_dict is None:
            return None

        return GoogleFile(
            name=google_file_dict.get('name'),
            id=google_file_dict.get('id'),
            parents=google_file_dict.get('parents'),
        )
