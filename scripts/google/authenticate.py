from __future__ import print_function

from googledrive import api


# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    # drive: Full, permissive scope to access all of a user's files,
    #        excluding the Application Data folder.
    "https://www.googleapis.com/auth/drive",
    # docs: Per-file access to files that the app created or opened.
    "https://www.googleapis.com/auth/drive.file",
    # sheets:
    # Allows read-only access to the user's sheets and their properties.
    "https://www.googleapis.com/auth/spreadsheets.readonly",
]

CREDENTIALS = "credentials.json"


def main():
    api.GoogleAuth().authenticate(CREDENTIALS, SCOPES)
    print('File "token.pickle" should be generated')


if __name__ == "__main__":
    main()
