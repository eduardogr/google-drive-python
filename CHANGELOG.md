# CHANGELOG

## PENDING

- Character of version update: **MINOR**
- New target version: **0.6.0**
- Pending changes:
  - Upgrading `google-api-python-client` to `2.166.0`
  - Upgrading `google-auth-httplib2`to `0.2.0`
  - Using `pyproject.toml`instead of `setup.py`
  - Changing format of importing code

## 0.5.1

- Formatting code
- New style guide
- Adding missing requirements
- Adapting release script to upload pip package using a pip token

## 0.5.0 / 0.4.0

Same as v0.4.0

This version was created to be able to upload again the version to Pypi because I had to remove 0.4.0 from pypi.
Now in pypi there is just 0.5.0, no 0.4.0 in pypi.

## 0.3.2


## 0.3.1


## 0.3.0


## 0.2.1

- fixing models.GoogleApiClientHttpErrorBuilder.from_http_error(), it wasn't  working.

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
