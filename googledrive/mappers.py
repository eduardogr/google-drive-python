from googledrive.models import GoogleFile

class GoogleFileDictToGoogleFile:

    def google_file_dict_to_google_file(self, google_file_dict):
        if google_file_dict is None:
            return None

        name = google_file_dict.get('name') or ''
        id = google_file_dict.get('id') or ''
        parents = google_file_dict.get('parents') or []
        mime_type = google_file_dict.get('mimeType') or ''
        export_links = google_file_dict.get('exportLinks') or {}

        return GoogleFile(
            name=name,
            id=id,
            parents=parents,
            mime_type=mime_type,
            export_links=export_links
        )
