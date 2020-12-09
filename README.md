# google drive python cli

Library and cli to manage and interact with your Google Drive, sheets and docs

- https://pypi.org/project/google-drive/ 


## :bookmark_tabs: Table of Contents

0. [Introduction](#introduction)
0. [Obtaining credentials for Google APIs](#wrench-obtaining-credentials-for-google-apis)
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

## :family: Contributing

[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Contributions are welcome! Please see our [Contributing Guide](<CONTRIBUTING.md>) for more
details. 

You can visit our [TODO](TODO.md) list :)

## :page_with_curl: License

This project is licensed under the [Apache license](https://github.com/eduardogr/google-drive-python/blob/main/LICENSE).
