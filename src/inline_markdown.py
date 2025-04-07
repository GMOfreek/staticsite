from textnode import TextNode, TextType
import re

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        markdowns = extract_markdown_images(original_text)
        if len(markdowns) == 0:
            new_nodes.append(old_node) 
            continue
        for markdown in markdowns:
            split_lines = original_text.split(f"![{markdown[0]}]({markdown[1]})", 1)
            if len(split_lines) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if split_lines[0] != "":
                new_nodes.append(TextNode(split_lines[0], TextType.TEXT))
            new_nodes.append(TextNode(markdown[0], TextType.IMAGE, markdown[1]))
            original_text = split_lines[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        markdowns = extract_markdown_links(original_text)
        if len(markdowns) == 0:
            new_nodes.append(old_node) 
            continue
        for markdown in markdowns:
            split_lines = original_text.split(f"[{markdown[0]}]({markdown[1]})", 1)
            if len(split_lines) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if split_lines[0] != "":
                new_nodes.append(TextNode(split_lines[0], TextType.TEXT))
            new_nodes.append(TextNode(markdown[0], TextType.LINK, markdown[1]))
            original_text = split_lines[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

