import json
from dataclasses import dataclass

from googleapiclient.errors import HttpError

@dataclass
class GoogleFile:

    EXPORT_TYPE_RTF                  = 'application/rtf'
    EXPORT_TYPE_VND_OASIS            = 'application/vnd.oasis.opendocument.text'
    EXPORT_TYPE_HTML                 = 'text/html'
    EXPORT_TYPE_PDF                  = 'application/pdf'
    EXPORT_TYPE_EPUB_ZIP             = 'application/epub+zip'
    EXPORT_TYPE_ZIP                  = 'application/zip'
    EXPORT_TYPE_VND_WORDPROCESSINGML = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    EXPORT_TYPE_PLAIN                = 'text/plain'

    def __init__(
            self,
            name,
            id,
            parents,
            mime_type,
            export_links):
        self.id = id
        self.name = name
        self.parents = parents
        self.mime_type = mime_type
        self.export_links = export_links

    def get_export_link(self, export_type):
        export_link = self.export_links[export_type] or ''
        return export_link

    def __str__(self):
        return f'({self.id}, {self.name}, {self.mime_type})'

@dataclass
class GoogleApiClientHttpError:

    def __init__(self, code, message, status, details):
        self.code = code
        self.message = message
        self.status = status
        self.details = details

class GoogleApiClientHttpErrorBuilder:

    def from_http_error(self, http_error: HttpError):
        error_reason = json.loads(http_error.content)
        error = error_reason['error']
        return GoogleApiClientHttpError(
            error['code'],
            error['message'],
            error['status'],
            error['details'] if 'details' in error else []
        )
