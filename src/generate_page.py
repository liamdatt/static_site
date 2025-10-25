from block_to_html import markdown_to_html_node
from htmlnode import *
from extract_title import extract_title
import os

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(f"{from_path}", "r", encoding="utf-8") as f:
        markdown = f.read()
    with open(f"{template_path}", "r", encoding="utf-8") as t:
        template = t.read()
    html_node = markdown_to_html_node(markdown)
    html_string = html_node.to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_string)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    if os.path.exists(os.path.dirname(dest_path)) == False:
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as p:
        p.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    list = os.listdir(dir_path_content)
    for item in list:
        old_item_path = dir_path_content + f"/{item}"
        new_item_path = dest_dir_path + f"/{item}"
        if os.path.isfile(old_item_path) == True:
            new_item_path = dest_dir_path + f'/{item.split(".")[0]}.html'
            if item.endswith(".md"):
                generate_page(old_item_path, template_path, new_item_path, basepath)
            else:
                continue
        else:
            os.mkdir(new_item_path)
            generate_pages_recursive(old_item_path,template_path,new_item_path, basepath)
            

    
