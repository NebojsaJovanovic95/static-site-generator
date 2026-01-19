from textnode import TextNode, TextType, BlockNode, BlockType
from htmlnode import LeafNode, ParentNode
from util import markdown_to_blocks
import subprocess
import re

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
    copy_static()
    from_path = "./content/index.md"
    template_path = "./static/template.html"
    dest_path = "./public/index.html"
    generate_page(from_path, template_path, dest_path)

if __name__ == "__main__":
    main()
