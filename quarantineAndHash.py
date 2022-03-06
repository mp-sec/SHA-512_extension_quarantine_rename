#!usr/bin/python3

import hashlib
import os
from shutil import copy2


def structure_printer(dir_path):
    os.system("tree /home/Lab3/folder0f8")


# Function that will create folders based on a files extension
def folder_creator(dir_path):
    creation_path = "/home/Lab3/Container"

    for root, dirs, files, in os.walk(dir_path):
        # For loop to print the contents of a folder
        for f in files:
            # Splits the filename into the files name [0th element] and its extension [1st element]
            file_ext_parse = f.split(".")
            # Together, both elements make a list, but they are strings on their own
            # print(type(file_ext_parse), type(file_ext_parse[0]), type(file_ext_parse[1]))
            dir_name = creation_path + "/" + file_ext_parse[1]

            for extension in f:
                # Checks if a folder for the file extension exists
                if not os.path.exists(dir_name):
                    try:
                        # If a folder does not exist, a folder is made of the same name as the file extension
                        # os.mkdir creates a single directory; whereas os.makedirs creates multiple
                        # os.makedirs also has the exist_ok flag, used to handle the FileExistsError flag
                        os.makedirs(dir_name, exist_ok=True)
                        print("Directory", dir_name, "created.")
                    except FileExistsError:
                        print("Directory", dir_name, "already exists.")


# Function to copy all files inside of dir_path into their respective folder based on their file extension
def file_copier(dir_path):
    copy_path = "/home/Lab3/Container"
    view_copy = input(print("Do you wish to see a list of all files that were successfully copied? [Y/N]"))

    for root, dirs, files, in os.walk(dir_path):
        # For loop to print the contents of a folder
        for f in files:
            file_ext_parse = f.split(".")
            # Copy2 can copy files to directories whilst also trying to copy its metadata and permissions over:
                # https://stackeroverflow.com/a/30359308
            # Source requires an absolute path to file an destination
            # Resource used:
                # https://www.geeksforgeeks.org/python-shutil-copy2-method/
            file_path = os.path.join(root, f)
            copy2(file_path, copy_path + "/" + file_ext_parse[1])

            if view_copy == "Y" or view_copy == "y":
                print("File", ".".join(file_ext_parse), "copied to sub-folder", file_ext_parse[1])


# Function to rename files to their SHA512 hash while retaining their extension
def file_hasher_and_renamer():
    rename_path = "/home/Lab3/Container"
    hasher = hashlib.sha512()
    view_renaming = input(print("Do you wish to see the names for the renamed files? [Y/N]"))

    # If true, topdown scans the folder structure starting from the top
    for root, dirs, files, in os.walk(dir_path, topdown=True):
        for f in files:
            file_ext_parse = f.split(".")
            os.chdir(rename_path + "/" + file_ext_parse[1])
            file_path = os.path.join(rename_path + "/" + file_ext_parse[1], f)
            # File stream best opened in "read binary" mode
            with open(str(file_path), "rb") as reader:
                buffer = reader.read()
                hasher.update(buffer)

            if view_renaming == "Y" or view_renaming == "y":
                print("File", f, "renamed ", end="")
                os.rename(rename_path + "/" + file_ext_parse[1] + "/" + f, str(hasher.hexdigest()) + "." + file_ext_parse[1])
                print(str(hasher.hexdigest()) + "." + file_ext_parse[1])
            else:
                os.rename(rename_path + "/" + file_ext_parse[1] + "/" + f, str(hasher.hexdigest()) + "." + file_ext_parse[1])


# Change the current directory to the location of the parent folder for the lab
dir_path = "/home/Lab3/folder0f8"
os.chdir(dir_path)
# print("PWD:", os.getcwd())

structure_printer(dir_path)
print("")
folder_creator(dir_path)
print("")
file_copier(dir_path)
print("")
file_hasher_and_renamer()
