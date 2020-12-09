# Google APIs

## Authentication

We should have a credentials.json file to use for the authentication process.
You could obtain your credentials using [google developer console](https://console.developers.google.com/apis/)

Using the same credentials you could specify all scopes you need, e.g:

    - 'https://www.googleapis.com/auth/drive'
    - 'https://www.googleapis.com/auth/script.projects'
    - 'https://www.googleapis.com/auth/gmail.readonly'
    - 'https://www.googleapis.com/auth/documents.readonly'
    - 'https://www.googleapis.com/auth/spreadsheets.readonly'

As we did it in this `examples/google-api-client/auth.py`.
Note that we are using python for this but you could try other programming languages

## google drive

- [quickstart](https://developers.google.com/sheets/api/quickstart/python)
- [enabling api](https://console.developers.google.com/apis/api/drive.googleapis.com/overview)
- [api reference](https://developers.google.com/drive/api/v3/reference/)
- [permissions level doc](https://developers.google.com/drive/api/v3/about-auth)
    - permissions used: "https://www.googleapis.com/auth/drive"


## google sheets

- [quickstar](https://developers.google.com/sheets/api/quickstart/python)
- [enabling api](https://console.developers.google.com/apis/api/sheets.googleapis.com/overview)
- [api reference](https://developers.google.com/sheets/api/reference/rest)
- [permissions level doc](https://developers.google.com/sheets/api/guides/authorizing)
    - permissions used: "https://www.googleapis.com/auth/spreadsheets.readonly"

## gmail

- [quickstart](https://developers.google.com/gmail/api/quickstart/python)
- [enabling api](https://console.developers.google.com/apis/api/gmail.googleapis.com/overview)
- [api reference](https://developers.google.com/gmail/api/v1/reference/)
- [permissions level doc](https://developers.google.com/gmail/api/auth/scopes)
    - permissions used: "https://www.googleapis.com/auth/gmail.send"

## google docs

- [quickstart](https://developers.google.com/docs/api/quickstart/python)
- [enabling api](https://console.developers.google.com/apis/api/docs.googleapis.com/overview)
- [api reference](https://developers.google.com/docs/api/reference/rest)
- [permissions level doc](https://developers.google.com/docs/api/how-tos/authorizing)
    - permissions used: "https://www.googleapis.com/auth/drive.file"

## app scrips

- [quickstart](https://developers.google.com/apps-script/api/quickstart/python)
- [enabling api](https://console.developers.google.com/apis/api/script.googleapis.com/overview)
- [api reference](https://developers.google.com/apps-script/api/reference/rest)
- [permissions level doc](https://developers.google.com/apps-script/api/how-tos/enable)
    - permissions used: No permission right now

# General things

A shareable URL of a Google Form is of the form

`https://docs.google.com/forms/d/{ID}/viewform`

where id is the ID associated with the file containing the form. 
We can obtain that id via API.
