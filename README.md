<h1 align="center"> google drive python </h1> <br>

Library and cli to manage and interact with your Google Drive, sheets and docs

- https://pypi.org/project/google-drive/ 


## :bookmark_tabs: Table of Contents

0. [Introduction](#introduction)
0. [Obtaining credentials for Google APIs](#wrench-obtaining-credentials-for-google-apis)
0. [Installing google-drive CLI](#installing-google-drive-cli)
0. [CLI Documentation](#cli-documentation)
0. [Contributing](#family-contributing)
0. [License](#page_with_curl-license)

# Introduction 
[![Build Status](https://travis-ci.org/eduardogr/google-drive-python.svg?branch=main)](https://travis-ci.org/github/eduardogr/google-drive-python)
[![codecov](https://codecov.io/gh/eduardogr/google-drive-python/branch/main/graph/badge.svg?token=E183Y3LLXX)](https://codecov.io/gh/eduardogr/google-drive-python)
[![Python](https://img.shields.io/badge/Python-v3.6%2B-blue)]()
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![GitHub license](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://github.com/eduardogr/google-drive-python/blob/main/LICENSE)  

## :wrench: Obtaining credentials for Google APIs

### Google API credentials

#### Create a Google project :zap:

Just access to [Google APIs](https://console.developers.google.com/).

  - Or [click here](https://console.developers.google.com/projectcreate) for a quick project creation.

#### Create credentials for your project :key:

Once you have created your project, you can create your project's credentials.

To manage project's credentials you have the section [api/credentials](https://console.developers.google.com/apis/credentials) within [Google APIs](https://console.developers.google.com/). But if this is your first credentials creation you better follow these steps:

  - First, you have to create the [consent](https://console.developers.google.com/apis/credentials/consent) for your project
  - Once the consent is already created and you have a name for you google app you can create your credentials:
      - Go to *+ Create Credentials* and select *OAuth ID client*
      - Or access to [api/credentials/oauthclient](https://console.developers.google.com/apis/credentials/oauthclient)
      - The OAuth client type is *other* and choose the name you prefer :smiley:

You have already created your credentials! :fireworks:

Just place them in a `credentials.json` file in the root of this repository. :heavy_exclamation_mark::heavy_exclamation_mark:

#### Enable Google APIs :books:

You can see where you have to access for each google api in the doc [google apis usage](./google-apis-usage.md)

#### Generating your token.pickle :unlock:

To authenticate us we have to send a token.pickle to Google APIs, this token.pickle is generated using the file credentials.json.

To generate this we have the make target google-auth, so, you just have to tun

  - `make google-auth`


:warning: Credentials files to authenticate yourself are included in our [.gitignore](.gitignore)

:angel: So, you don't have to worry about that :smiley:


# Installing google-drive CLI

## Using make

```
make install
```

## Using pip

```
pip install google-drive
```

### With specific version

Look for available versions with:

```
pip install google-drive==
```

And select one and run:

```
pip install google-drive==<VERSION>
```

# CLI Documentation

## google-drive --help

Shows the help message

### Usage

```
> google-drive --help
Usage: google-drive [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  get    Get file metadata
  login  Perform a login with google oauth
  ls     List directory contents
  mkdir  Make directory
```

## google-drive login

Perform a login with google oauth.

### Usage

```
> google-drive login <path-to-credentials-file.json>
```

## google-drive ls

List directory contents

### Usage

```
> google-drive ls <directory>/<maybe-some-subdir> <path-to-credentials-file.json>
- (<GOOGLE_DOC_ID_1>, <FILENAME_1>, <FILE_MIMETYPE_1>)
- (<GOOGLE_DOC_ID_2>, <FILENAME_2>, <FILE_MIMETYPE_2>)
- (<GOOGLE_DOC_ID_3>, <FILENAME_3>, <FILE_MIMETYPE_3>)
...
- (<GOOGLE_DOC_ID_N>, <FILENAME_N>, <FILE_MIMETYPE_N>)
```

## google-drive get

Get file metadata

### Usage

```
> google-drive get <GOOGLE_DOC_ID> <path-to-credentials-file.json>

File Metadata:
==
id: <GOOGLE_DOC_ID>
name: <FILENAME>
parents: ['<GOOGLE_DOC__PARENT_ID>']
mime_type: <FILE_MIMETYPE>
export_links:
  - application/rtf: https://docs.google.com/feeds/download/documents/export/Export?id=<GOOGLE_DOC_ID>&exportFormat=rtf
  - application/vnd.oasis.opendocument.text: https://docs.google.com/feeds/download/documents/export/Export?id=<GOOGLE_DOC_ID>&exportFormat=odt
  - text/html: https://docs.google.com/feeds/download/documents/export/Export?id=<GOOGLE_DOC_ID>&exportFormat=html
  - application/pdf: https://docs.google.com/feeds/download/documents/export/Export?id=<GOOGLE_DOC_ID>&exportFormat=pdf
  - application/epub+zip: https://docs.google.com/feeds/download/documents/export/Export?id=<GOOGLE_DOC_ID>&exportFormat=epub
  - application/zip: https://docs.google.com/feeds/download/documents/export/Export?id=<GOOGLE_DOC_ID>&exportFormat=zip
  - application/vnd.openxmlformats-officedocument.wordprocessingml.document: https://docs.google.com/feeds/download/documents/export/Export?id=<GOOGLE_DOC_ID>&exportFormat=docx
  - text/plain: https://docs.google.com/feeds/download/documents/export/Export?id=<GOOGLE_DOC_ID>&exportFormat=txt
  ```

## google-drive mkdir

Make directory

### Usage

```
> google-drive mkdir <DIR_NAME> <path-to-credentials-file.json>
(<GOOGLE_DOC_ID>, <DIR_NAME>, application/vnd.google-apps.folder)
```

# Using googledrive as API SDK

## :family: Contributing

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Contributions are welcome! Please see our [Contributing Guide](<CONTRIBUTING.md>) for more
details. 

You can visit our [TODO](TODO.md) list :)

## :page_with_curl: License

This project is licensed under the [Apache license](https://github.com/eduardogr/google-drive-python/blob/main/LICENSE).
