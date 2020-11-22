import sys
import argparse

from googledrive.api import GoogleAuth
from googledrive.api import GoogleDrive

def help():
    return '''
Usage: google-drive [OPTIONS] COMMAND

Manage and interact with your Google Drive.

Commands:

    login   Perform a login with google oauth
    ls      List directory contents
    mkdir   Make directory
    '''

def googledrive(args=sys.argv):
    args = args[1:]

    if len(args) == 0:
        print(help())
        exit()

    command = args[0]
    args = args[1:] or []

    if 'login' == command:
        credentials = args[0]
        GoogleAuth().authenticate(credentials)

    elif 'ls' == command:
        credentials = args[0]
        path = args[1]
        files = GoogleDrive(credentials).googledrive_ls(path)
        for file in files:
            print(file.name)  # TODO: nice print

    elif 'mkdir' == command:
        credentials = args[0]
        name = args[1]
        folder = GoogleDrive(credentials).create_folder(name)
        print(folder) # TODO: nice print

    # TODO
    elif 'cat' == command:
        credentials = args[0]
        path = args[1]

        print(f"cat command for file: {path}")

    # TODO
    elif 'analysis' == command:
        # would be nice to expose interesting data
        # e.g. duplicated files that we cannot disambiguate through API
        print('analyzing your drive...')

    else:
        print(f"Command {command} not expected.")


if __name__ == '__main__':
    googledrive()
