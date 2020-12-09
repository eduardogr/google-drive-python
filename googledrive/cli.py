import sys
import click

from googledrive.api import GoogleAuth
from googledrive.api import GoogleDrive

class Config:
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = [
        # drive: Full, permissive scope to access all of a user's files,
        #        excluding the Application Data folder.
        'https://www.googleapis.com/auth/drive',
        # docs: Per-file access to files that the app created or opened.
        'https://www.googleapis.com/auth/drive.file',
        # sheets:
        # Allows read-only access to the user's sheets and their properties.
        'https://www.googleapis.com/auth/spreadsheets.readonly',
    ]

@click.command()
@click.argument('credentials', type=click.Path(exists=True))
def login(credentials):
    """Perform a login with google oauth"""
    GoogleAuth().authenticate(
        credentials=credentials,
        scopes=Config.SCOPES)

@click.command()
@click.argument('credentials', type=click.Path(exists=True))
@click.argument('path')
def ls(credentials, path):
    """List directory contents"""
    google_drive = GoogleDrive(credentials, Config.SCOPES)
    files = google_drive.googledrive_ls(path)
    for file in files:
        print(file.name)  # TODO: nice print

@click.command()
@click.argument('credentials', type=click.Path(exists=True))
@click.argument('name')
def mkdir(credentials, name):
    """Make directory"""
    google_drive = GoogleDrive(credentials, Config.SCOPES)
    folder = google_drive.create_folder(name)
    print(folder) # TODO: nice print

@click.group()
def googledrive():
    pass

googledrive.add_command(login)
googledrive.add_command(ls)
googledrive.add_command(mkdir)
