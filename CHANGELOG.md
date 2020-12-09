# CHANGELOG

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
