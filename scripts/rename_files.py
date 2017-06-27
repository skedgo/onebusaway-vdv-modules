
"""
Parses zip files of VDV452 files and renames them according to the table names, 
and then zips it all up again.
"""

import sys
from zipfile import ZipFile
import os
from pathlib import Path
import shutil

if len(sys.argv) < 4:
    print("Need 3 arguments: input zip file, output folder, output file name")
    exit(1)

IN_FILE = sys.argv[1]
OUT_FOLDER = sys.argv[2]
OUT_FILE = sys.argv[3]

def extract(zip_file, temp_folder):
    with ZipFile(zip_file, 'r') as in_zip:
        in_zip.extractall(path=temp_folder)

def zipup(folder, out):
    with ZipFile(out, 'w') as new_zip:
        with os.scandir(folder) as it:
            for entry in it:
                if entry.is_dir():
                    print(f"Ignoring {entry.path}")
                else:
                    new_zip.write(entry.path, arcname=entry.name)

def rename_files_in_folder(folder):
    with os.scandir(folder) as it:
        for entry in it:
            if entry.is_dir():
                return rename_files_in_folder(entry)
            else:
                rename_file(entry.path)
        return folder

def rename_file(file):
    name = find_table(file)
    if name is None:
        return
    old_file = os.path.basename(file)
    new_file = name + ".x10"
    print(f"{old_file} is {new_file}")
    os.rename(file, file.replace(old_file, new_file))

def find_table(file):
    with open(file, 'r', encoding="ISO8859-1") as f:
        for l in f:
            if l.startswith("tbl; "):
                return l[5:-1]


# 1. Extract files
print(f"Extracting '{IN_FILE}'...")
TEMP_FOLDER = os.path.normpath(OUT_FOLDER + "/temp")
os.mkdir(TEMP_FOLDER)
extract(IN_FILE, TEMP_FOLDER)

# 2. Rename all files recursively
print(f"Renaming in {TEMP_FOLDER}...")
TARGET = rename_files_in_folder(TEMP_FOLDER)
print(f"Renamed in {TARGET}")

# 3. Zip files
NEW_FILE = os.path.normpath(OUT_FOLDER + "/" + OUT_FILE)
print(f"Creating '{NEW_FILE}'")
zipup(TARGET, NEW_FILE)
shutil.rmtree(TEMP_FOLDER)
