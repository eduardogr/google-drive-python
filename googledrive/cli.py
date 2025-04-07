import click

from googledrive import api
from googledrive import exceptions


class Config:
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


@click.command()
@click.argument("credentials", envvar="CREDENTIALS", type=click.Path(exists=True))
def login(credentials):
    """Perform a login with google oauth"""
    api.GoogleAuth().authenticate(credentials=credentials, scopes=Config.SCOPES)


@click.command()
@click.argument("path")
@click.argument("credentials", envvar="CREDENTIALS", type=click.Path(exists=True))
def ls(credentials, path):
    """List directory contents"""
    try:
        google_drive = api.GoogleDrive(credentials, Config.SCOPES)
        files = google_drive.googledrive_ls(path)
    except exceptions.GoogleApiClientHttpErrorException as e:
        error = e.get_google_api_client_http_error()
        print(f"An http exception occured requesting google's API:\n")
        print(f" - Code: {error.code}")
        print(f" - Message: {error.message}")
        print(f" - Status: {error.status}")
        print(f" - Details: {error.details}")
        print(f" - Errors: {error.errors}\n")
        return

    for file in files:
        print(f"- {file}")  # TODO: nice print


@click.command()
@click.argument("id")
@click.argument("credentials", envvar="CREDENTIALS", type=click.Path(exists=True))
def get(id, credentials):
    """Get file metadata"""
    try:
        google_drive = api.GoogleDrive(credentials, Config.SCOPES)
        google_file = google_drive.get_file_from_id(id)
    except exceptions.GoogleApiClientHttpErrorException as e:
        error = e.get_google_api_client_http_error()
        print(f"An http exception occured requesting google's API:\n")
        print(f" - Code: {error.code}")
        print(f" - Message: {error.message}")
        print(f" - Status: {error.status}")
        print(f" - Details: {error.details}")
        print(f" - Errors: {error.errors}\n")
        return

    print("\nFile Metadata:\n==")
    print(f"id: {google_file.id}")
    print(f"name: {google_file.name}")
    print(f"parents: {google_file.parents}")
    print(f"mime_type: {google_file.mime_type}")
    print(f"export_links:")

    for link_type, link in google_file.export_links.items():
        print(f"  - {link_type}: {link}")


@click.command()
@click.argument("name")
@click.argument("credentials", envvar="CREDENTIALS", type=click.Path(exists=True))
def mkdir(credentials, name):
    """Make directory"""
    try:
        google_drive = api.GoogleDrive(credentials, Config.SCOPES)
        folder = google_drive.create_folder(name)
    except exceptions.GoogleApiClientHttpErrorException as e:
        error = e.get_google_api_client_http_error()
        print(f"An http exception occured requesting google's API:\n")
        print(f" - Code: {error.code}")
        print(f" - Message: {error.message}")
        print(f" - Status: {error.status}")
        print(f" - Details: {error.details}")
        print(f" - Errors: {error.errors}\n")
        return

    print(folder)  # TODO: nice print


@click.command()
@click.argument("credentials", envvar="CREDENTIALS", type=click.Path(exists=True))
def get_mimetypes(credentials):
    """Get Mimetypes availables in this API implementation"""
    try:
        google_drive = api.GoogleDrive(credentials, Config.SCOPES)
        mimetypes = google_drive.get_mymetypes()
    except exceptions.GoogleApiClientHttpErrorException as e:
        error = e.get_google_api_client_http_error()
        print(f"An http exception occured requesting google's API:\n")
        print(f" - Code: {error.code}")
        print(f" - Message: {error.message}")
        print(f" - Status: {error.status}")
        print(f" - Details: {error.details}")
        print(f" - Errors: {error.errors}\n")
        return

    for mimetype in mimetypes:
        print(f"  - {mimetype}")  # TODO: nice print


@click.command()
@click.argument("name")
@click.argument("mymetype")
@click.argument("credentials", envvar="CREDENTIALS", type=click.Path(exists=True))
def touch(credentials, mymetype, name):
    """Create empty file of specified mimetype"""
    try:
        google_drive = api.GoogleDrive(credentials, Config.SCOPES)
        file = google_drive.create_file(name=name, mimetype=mymetype)
    except exceptions.GoogleApiClientHttpErrorException as e:
        error = e.get_google_api_client_http_error()
        print(f"An http exception occured requesting google's API:\n")
        print(f" - Code: {error.code}")
        print(f" - Message: {error.message}")
        print(f" - Status: {error.status}")
        print(f" - Details: {error.details}")
        print(f" - Errors: {error.errors}\n")
        return

    print(file)  # TODO: nice print


@click.group()
def googledrive():
    pass


googledrive.add_command(login)
googledrive.add_command(ls)
googledrive.add_command(get)
googledrive.add_command(mkdir)
googledrive.add_command(get_mimetypes)
googledrive.add_command(touch)
