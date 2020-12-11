# CHANGELOG

## Pending

## 0.2.0

- Now credentials is the last arugment expected
  - e.g.: google-drive ls <path> <credentials-file>
- Now credentials could be a envvar
  - export CREDENTIALS=credentials.json && google-drive ls <path> <credentials-file>
- New command `get`. This will retrieve us file's metadata.
  - e.g.: google-drive get <ID>
- Extending models.GoogleFile.
  - Adding: mimeType and exportLinks fields.
  - Adding export types constants to get export type from a GoogleFile

## 0.1.3

- fixing cli usecases
  - google-drive ls
  - google-drive mkdir
- adding usage of click for cli interaction

## 0.1.2

- fixing api.GoogleService.__get_credentials function, adding scopes argument to its __init__ funciton

## 0.1.1

- api.GoogleAuth class now receives an argument to specify api-token scopes
- fixing api.FilesAPI().empty_document, now receives two more args: insert_index and end_index,
- adding unit tests

## 0.1.0

- api.GoogleAuth
- api.GoogleService
- api.GoogleDrive
- api.SheetsService
