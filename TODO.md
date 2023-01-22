# TODO

## Project management

- [X] Add CLI documentation
- [ ] Add API documentation
- [ ] Add examples of usage the api.py from a piece of code.
- [ ] Add pull requests and issues templates
- [X] Add CONTRIBUTING

## Functionalities

- [X][CLI] Implement `get` to get file metadata.
- [ ][CLI] Extending `ls` for an ID file.
- [ ][CLI] Extending `mkdir` for a path folder.
- [ ][CLI] Implement `rmdir` for a path folder.
- [ ][CLI] Implement `analysis` to extract data from the google drive.
- [ ][CLI] Implement `cat` for a google doc file.
- [ ][CLI] Implement `touch` for create an empty google doc, spreadsheet, presentation, form, ...
- [ ][CLI] Implement `cp` for a google doc file. From source path to destiny path.
- [ ][CLI] Implement `mv` for a google doc file. From source path to destiny path.
- [ ][API] Implement open_file help function for spreadsheets files. This will retrieve an object that will allow us manage that file; reading (readlines); updating; removing, ...
- [ ][API] Implement readlines help function for spreadsheets files reading.
- [ ][CLI] Nice print for cli output.

## Design

- [ ] Adding design layers to point out where to place which type of code.
- [ ][CLI] Add logger with different levels of logging: {ERROR, WARNING, INFO, DEBUG}.
- [ ][CLI] Adding clean architecture layers.
- [ ][CLI] Adding layer for filter input.
- [ ][CLI] Adding layer for showing output.