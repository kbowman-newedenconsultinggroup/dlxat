# Create CAB file from folder

Create CAB files based on the contents of a folder.
Adds all files, folders and keeps the folder structure intact!

Just <b>drag and drop the folder</b> you want on to either the file "<b>Create CAB</b>" or "Create DDF Only".

## Scripts
"<b>Create CAB</b>" creates both the DDF and CAB files.

"<b>Create DDF Only</b>" only creates the DDF file.

## Compatibility
The CAB files seems to work fine in Windows 98SE, Vista and 11 so far in my tests.
Would expect the files to work in Windows XP, 7, 8 and 10 as well.

## Alternatives

1. Windows application named "CabMaker": https://github.com/sapientcoder/CabMaker
2. Manually create DDF files and run the "makecab" command :-P 

There are other scripts and examples, but none of the ones I found actually worked correctly. 

## Enable running scripts!

In order to run Powershell scripts, run the file [Set-ExecutionPolicy Unrestricted.bat](https://github.com/runeandre/create_cab/tree/main/Set-ExecutionPolicy/Set-ExecutionPolicy%20Unrestricted.bat)

Or run the powershell command "Set-ExecutionPolicy Unrestricted".

You can revert to default settings with "Set-ExecutionPolicy Default" and "Set-ExecutionPolicy Default All" for all scopes.