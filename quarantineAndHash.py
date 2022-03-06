#!usr/bin/python3

# Filename: m3p1.py
# Author: Mandeep Parihar
# Course: ITSC-203
# Details: The program will traverse a file structure and display all of the content inside of it in a tree structure, create folders based off
    # of the extensions of the files, copy the files from the structure into their respective folder based on their extension, and rename them
    # to the SHA512 hash that is generated for the file
# Resources: https://docs.python.org/3/library/pprint.html
    # https://docs.python.org/3/library/os.html
    # https://docs.python.org/3/library/shutil.html

import hashlib
import os
from shutil import copy2
# import pprint   # Imports the Pretty Print module

# Example of Pretty Printer
# # def structure_printer():
#     # Pretty Printer parameters:
#         # Indent: Number of indents given to each recursive level
#         # Width: Number of characters that can be displayed on a single line in the output (default is 80)
#         # Depth: Maximum number of levels to be printed (if levels go beyond depth value, they are represented with '...')
#         # Compact: If true (false by default), it will fit as many levels into a single line as the depth value allows (cannot exceed the depth value)
#     # Unused Pretty Printer parameters:
#         # Stream: Sets an output stream
#         # Sort_dicts: Sorts by the keys (true by default)
#     pp = pprint.PrettyPrinter(indent=3, width=200, depth=5, compact=True)
#     for dir_tuple in os.walk(dir_path):
#         pp.pprint(dir_tuple)


def structure_printer(dir_path):
    # This single line does pretty much everything commented out below it
    # This was installed using the terminal command "sudo apt install tree"
    # Code was found from the comment:
        # https://stackoverflow.com/a/49620815
    os.system("tree /home/Lab3/folder0f8")

    # # os.walk(directory path) will traverse an entire file structure, including all sub folders
    # for root, dirs, files, in os.walk(dir_path):
    #     # Removes unnecessary parts of the file path from itself
    #     level = root.replace(dir_path, '').count(os.sep)
    #     # Multiplies a single space by 4 then by the level of depth of the sub directory
    #     indent = ' ' * 4 * level
    #
    #     # If block to create the appropriate string to add to the folder name to signify its depth
    #     if level == 0:
    #         sub_level = "[PARENT DIRECTORY]"
    #     elif level == 1:
    #         sub_level = "[LEVEL 1 DIRECTORY]"
    #     elif level == 2:
    #         sub_level = "[LEVEL 2 DIRECTORY]"
    #     elif level == 3:
    #         sub_level = "[LEVEL 3 DIRECTORY]"
    #     elif level == 4:
    #         sub_level = "[LEVEL 4 DIRECTORY]"
    #     else:
    #         sub_level = "--- ERROR ---"
    #
    #     # Prints the folder name and the sub level depth of the folder
    #     print('{}{}/'.format(indent, os.path.basename(root)), sub_level)
    #     # Indentation for the files inside of a folder
    #     sub_indent = ' ' * 4 * (level + 1)
    #
    #     # For loop to print the contents of a folder
    #     for f in files:
    #         print('{}{}'.format(sub_indent, f))


# Existing file extensions: .worm, .evp, .mal, .zip, .txt, .mpp (6 total types)
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


# Example hashing function
# def file_hasher(dir_path, hash_display):
#     hasher = hashlib.sha512()
#     hash_display = input(print("Display SHA512 hash for sub directories? [Y/N]"))
#
#     # If true, topdown scans the folder structure starting from the top
#     for root, dirs, files, in os.walk(dir_path, topdown=True):
#         for f in files:
#             file_path = os.path.join(root, f)
#             # File stream best opened in "read binary" mode
#             with open(str(file_path), "rb") as reader:
#                 buffer = reader.read()
#                 hasher.update(buffer)
#
#         if hash_display == "Y" or hash_display == "y":
#             print('{}:'.format(os.path.basename(root)), hasher.hexdigest())


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
