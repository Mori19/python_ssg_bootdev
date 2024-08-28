from functools import reduce
from re import search
from textnode import *
from htmlnode import *
import os

def split_nodes_delimiter(nodes, delim, text_type):
    def cut(a,b):
        if isinstance(b,TextNode):
            if not delim in b.text or not delim in b.text[b.text.index(delim)+1:]:
                return a +[b]
            start = b.text.index(delim)
            fin = b.text[start+1:].index(delim) + len(delim) + start + 1
            col = list()
            if len(b.text[:start]) > 0:
                col.append(TextNode(b.text[:start],b.text_type))
            if len(b.text[start:fin]) > len(delim)*2:
                col.append(text_node_to_html_node(
                    TextNode(b.text[start+len(delim):fin-len(delim)], text_type)
                    ))
            if len(b.text[fin:]) > 0:
                col.extend(cut([],TextNode(b.text[fin:],b.text_type)))
            return a+col
        if isinstance(b,LeafNode):
            if not delim in b.value or not delim in b.value[b.value.index(delim):]:
                return a + [b]
            start = b.value.index(delim)
            fin = b.value[start+1:].index(delim) + len(delim) + start + 1
            col = list()
            if len(b.value[:start]) > 0:
                col.append(LeafNode(b.tag, b.value[:start],b.props))
            if len(b.value[start:fin]) > len(delim)*2:
                col.append(LeafNode(text_type,b.value[start+len(delim):fin-len(delim)]))
            if len(b.value[fin:]) > 0:
                col.extend(cut([],TextNode(b.tag, b.value[fin:])))
            return a+col
    return reduce(cut, nodes, [])

def extract_markdown_images(text):
    def get_link(a, b):
        match = search(r"!\[(.*?)\]\((.*?)\)", b)
        if match == None:
            return a
        return a + [(match.group(1), match.group(2))] + get_link([],b[b.index(match.group(0)) + len(match.group(0)):])
    return get_link([],text)

def extract_markdown_links(text):
    def get_link(a, b):
        match = search(r"(?<!!)\[(.*?)\]\((.*?)\)", b)
        if match == None:
            return a
        return a + [(match.group(1), match.group(2))] + get_link([],b[b.index(match.group(0)) + len(match.group(0)):])
    return get_link([],text)

def split_nodes_link(nodes):
    return split_nodes_links(nodes)
def split_nodes_image(nodes):
    return split_nodes_links(nodes)

def split_nodes_links(nodes):
    def inner(a,b):
        if isinstance(b,TextNode):
            links = extract_markdown_links(b.text)
            images = extract_markdown_images(b.text)
            if links == [] and images == []: 
                return a+[b]
            elif links == []:
                val = f"![{images[0][0]}]({images[0][1]})"
                tag = "img"
                start = b.text.index(val)
            elif images == []:
                val = f"[{links[0][0]}]({links[0][1]})"
                tag = "a"
                start = b.text.index(val)
            else:
                l= f"[{links[0][0]}]({links[0][1]})"
                i = f"![{images[0][0]}]({images[0][1]})"
                links_first = b.text.index(l)
                images_first = b.text.index(i)
                start = min(links_first, images_first)
                val = l if links_first < images_first else i
                tag = "a" if links_first < images_first else "img"
            fin = start + len(val)
            col = list()
            if len(b.text[:start]) > 0:
                col.append(TextNode(b.text[:start],b.text_type))
            col.append(
                    LeafNode(tag,
                             links[0][0] if tag == "a" else "",
                             {'href':f'{links[0][1]}'} if tag == 'a' else {'src':images[0][1],
                                                                           'alt':images[0][0]})
                )
            if len(b.text[fin:]) > 0:
                col.extend(inner([],TextNode(b.text[fin:],b.text_type)))
            return a+col
        if isinstance(b,LeafNode):
            links = extract_markdown_links(b.value)
            images = extract_markdown_images(b.value)
            if links == [] and images == []: 
                return a+[b]
            elif links == []:
                val = f"![{images[0][0]}]({images[0][1]})"
                tag = "img"
                start = b.value.index(val)
            elif images == []:
                val = f"[{links[0][0]}]({links[0][1]})"
                tag = "a"
                start = b.value.index(val)
            else:
                l= f"[{links[0][0]}]({links[0][1]})"
                i = f"![{images[0][0]}]({images[0][1]})"
                links_first = b.value.index(l)
                images_first = b.value.index(i)
                start = min(links_first, images_first)
                val = l if links_first < images_first else i
                tag = "a" if links_first < images_first else "img"
            fin = start + len(val)
            col = list()
            if len(b.value[:start]) > 0:
                col.append(LeafNode(b.tag,b.value[:start]))
            col.append(
                    LeafNode(tag,
                             links[0][0] if tag == "a" else "",
                             {'href':f'{links[0][1]}'} if tag == 'a' else {'src':images[0][1],
                                                                           'alt':images[0][0]})
                )
            if len(b.value[fin:]) > 0:
                col.extend(inner([],LeafNode(b.tag,b.value[fin:])))
            return a+col
        pass
    return reduce(inner, nodes, [])

def text_to_textnodes(text):
    return split_nodes_delimiter(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_links([TextNode(text,'text')]),
                    '**', 'bold'),
                '*', 'italic'),
            '`', 'code')
def textnodes_to_htmlnodes(textnodes):
    textnodes = text_to_textnodes(textnodes)
    a =  list(map(lambda a : text_node_to_html_node(a) if isinstance(a, TextNode) else a, textnodes))
    return a

def markdown_to_blocks(markdown):
    markdown = markdown.strip()
    def cut(a,b):
        b = b.lstrip()
        if not '\n\n' in b:
            return [b.strip()]
        end = b.index('\n\n')
        return a + [b[:end].strip()] + cut([],b[end:])
    return cut([],markdown)

def ordered_list_checker(l):
    for i in range(len(l)):
        if l[i][:len(f'{str(i+1)}. ')] != f'{str(i+1)}. ':
            return False
    return True

def block_to_block_type(block):
    lines = block.split('\n')
    if lines[0][0] == "#":
        def count(l):
            if l[0] == ' ':
                return 0
            elif l[0] == '#':
                return 1 + count(l[1:])
            else:
                return 'uh oh' #this is obviously incorreclty implemented 
        return f"h{count(lines[0])}"
    elif lines[0] == '```' and lines[-1] == '```':
        return 'code'
    elif all([line[0:2] == '> ' for line in lines]):
           return "blockquote"
    elif all([line[0:2] == '* ' for line in lines]) or all([line[0:2] == '- ' for line in lines]):
        return 'ul'
    elif ordered_list_checker(lines):
        return 'ol'
    else: 
        return 'p'

def block_stripper(block):
    t = block_to_block_type(block)
    if t[0] == 'h':
        return block[int(t[1])+1:]
    elif t == 'code':
        return '\n'.join(block.split('\n')[1:-1])
    elif t == 'blockquote':
        return '\n'.join([line[line.index(' ')+1:] for line in block.split('\n')])
    elif t in ['ul','ol']:
        return '\n'.join([f"<li>{line[line.index(' ')+1:]}</li>" for line in block.split('\n')])
    else:
        return block


def blocks_to_htmlnode(blocks):
    return  list(map(lambda block: ParentNode(block_to_block_type(block),
                                             textnodes_to_htmlnodes(block_stripper(block))), blocks))

def markdown_to_html_node(markdown):
    return ParentNode('div',
                      blocks_to_htmlnode(
                          markdown_to_blocks(markdown)
                          )
                      )
def extract_title(htmlnode):
    for node in htmlnode.children:
        if isinstance(node, ParentNode) and node.tag == 'h1':
            return node.children[0].value
    raise Exception("No title found")

def generate_page(src,template,dst):
    dst_path = dst.split('/')
    if len(dst_path) > 1:
        os.makedirs('/'.join(dst_path[:-1]), exist_ok=True)
    with open(src) as f:
        md = f.read()
    with open(template) as f:
        t = f.read()
    doc = markdown_to_html_node(md)
    title = extract_title(doc)
    t = t.replace('{{ Title }}', title)
    t = t.replace('{{ Content }}', doc.to_html())
    with open(dst, 'w') as f:
        f.write(t)

def generate_page_recursive(src_path,template_path,dst_path):
    here = os.listdir(src_path)
    list(map(lambda a: print(f'Generating path: {dst_path}/{a}') if os.path.isfile(f'{src_path}/{a}') else '', here))
    list(map(lambda a : \
            generate_page(f'{src_path}/{a}',
                          template_path,
                          f'{dst_path}/{a.replace(".md",".html")}') \
                                  if os.path.isfile(f'{src_path}/{a}') \
                                  else generate_page_recursive(f'{src_path}/{a}',
                                                               template_path,
                                                               f'{dst_path}/{a}'), here))
