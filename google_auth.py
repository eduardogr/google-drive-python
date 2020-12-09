from __future__ import print_function
from googledrive.api import GoogleAuth


# If modifying these scopes, delete the file token.pickle.
SCOPES = [
    # drive: Full, permissive scope to access all of a user's files,
    #        excluding the Application Data folder.
    'https://www.googleapis.com/auth/drive',
    # gmail: Send messages only. No read or modify privileges on mailbox.
    'https://www.googleapis.com/auth/gmail.send',
    # docs: Per-file access to files that the app created or opened.
    'https://www.googleapis.com/auth/drive.file',
    # sheets:
    # Allows read-only access to the user's sheets and their properties.
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    # appscripts:
    #'https://www.googleapis.com/auth/script.projects',
]

CREDENTIALS = 'credentials.json'

def main():
    GoogleAuth().authenticate(
        CREDENTIALS,
        SCOPES)
    print('File "token.pickle" should be generated')

if __name__ == '__main__':
    main()
