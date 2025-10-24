from textnode import TextNode, TextType
import os
import shutil
from generate_page import *

def main():
    if os.path.exists("static") == False:
        raise Exception("static folder not found in root directory")
    if os.path.exists("public") == True:
        shutil.rmtree("public")
        os.mkdir("public") 
    else:
        os.mkdir("public")
    move_all("static","public")
    generate_pages_recursive("content", "template.html", "public")

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

