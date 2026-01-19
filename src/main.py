from textnode import TextNode, TextType, BlockNode, BlockType
from htmlnode import LeafNode, ParentNode
from util import markdown_to_blocks
import subprocess
import re
import os
import sys


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    # Use find to get all .md files
    result = subprocess.run(
        ["find", dir_path_content, "-type", "f", "-name", "*.md"],
        capture_output=True,
        text=True,
        check=True
    )

    md_files = result.stdout.strip().split("\n")

    for md_file in md_files:
        # Compute relative path as a string
        rel_path = os.path.relpath(md_file, dir_path_content)
        dest_file = os.path.join(dest_dir_path, os.path.splitext(rel_path)[0] + ".html")

        # Make sure destination directory exists
        dest_dir = os.path.dirname(dest_file)
        os.makedirs(dest_dir, exist_ok=True)

        # Call your generate_page function
        generate_page(md_file, template_path, dest_file)
        print(f"Generated: {md_file} -> {dest_file}")

def extract_title(md_text):
    match = re.compile(r'^#\s+(.*)', re.MULTILINE).search(md_text)
    if match:
        return match.group(1)
    else:
        raise ValueError("No title found in md file")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = []
    title = None
    with open(from_path, "r", encoding="utf-8") as f:
        md_text = f.read()
        title = extract_title(md_text)
        md = BlockNode(BlockType.DIV, md_text)
    html = md.to_html()
    content = html.to_html()
    page = ""
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()
        page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)
        with open(dest_path, "w", encoding="utf-8") as write_file:
            write_file.write(page)

def copy_static():
    subprocess.run("rsync -av --exclude='template.html' static/ public/", shell=True, check=True)

def main():
    basepath = "/"
    if len(sys.argv) >= 2:
        basepath = sys.argv[1]
    os.chdir(basepath)
    copy_static()
    from_path = "./content/"
    template_path = "./static/template.html"
    dest_path = "./public/"
    generate_pages_recursive(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()
