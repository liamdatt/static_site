from textnode import TextNode, TextType
import os
import shutil
from generate_page import *
import sys

def main():
    if len(sys.argv) > 1:
        basepath =sys.argv[1]
    else:
        basepath = "/"
    if os.path.exists("static") == False:
        raise Exception("static folder not found in root directory")
    if os.path.exists("docs") == True:
        shutil.rmtree("docs")
        os.mkdir("docs") 
    else:
        os.mkdir("docs")
    move_all("static","docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)

def move_item(item_path,destination_path):
    shutil.copy(item_path,destination_path)

def move_all(old_directory,new_directory):
    print(f"CALL move_all({old_directory} -> {new_directory})")
    list = os.listdir(old_directory)
    for item in list:
        old_item_path = old_directory + f"/{item}"
        new_item_path = new_directory + f"/{item}"
        if os.path.isfile(old_item_path) == True:
            move_item(old_item_path,new_directory)
            print(f" FILE: {old_item_path}  -> copy to  {new_directory}")
        else:
            os.mkdir(new_item_path)
            print(f" DIR : {old_item_path}  -> recurse to {new_item_path}")
            move_all(old_item_path,new_item_path)

        

main()

