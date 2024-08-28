import unittest 

from textnode import *
from htmlnode import *
from operations import *

class TestSplitNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This *is* a text node", "text")
        node_list = split_nodes_delimiter([node], '*', 'italic')
        self.assertEqual(node_list, [
            TextNode("This ", "text"),
            LeafNode("i", "is"),
            TextNode(" a text node", "text")
            ]
            )

    def test_code(self):
        node = TextNode("This `is` a text node", "text")
        node_list = split_nodes_delimiter([node], '`', 'code')
        self.assertEqual(node_list, [
            TextNode("This ", "text"),
            LeafNode("code", "is"),
            TextNode(" a text node", "text")
            ]
            )

    def test_bold(self):
        node = TextNode("This **is** a text node", "text")
        node_list = split_nodes_delimiter([node], '**', 'bold')
        self.assertEqual(node_list, [
            TextNode("This ", "text"),
            LeafNode("b", "is"),
            TextNode(" a text node", "text")
            ]
            )

    def test_two(self):
        node = TextNode("This **is** a **text** node", "text")
        node_list = split_nodes_delimiter([node], '**', 'bold')
        self.assertEqual(node_list, [
            TextNode("This ", "text"),
            LeafNode("b", "is"),
            TextNode(" a ", "text"),
            LeafNode("b", "text"),
            TextNode(" node", "text"),
            ]
            )

    def test_list(self):
        node = TextNode("This **is** a **text** node", "text")
        node2 = TextNode("This **is** a **text** node", "text")
        node_list = split_nodes_delimiter([node,node2], '**', 'bold')
        self.assertEqual(node_list, [
            TextNode("This ", "text"),
            LeafNode("b", "is"),
            TextNode(" a ", "text"),
            LeafNode("b", "text"),
            TextNode(" node", "text"),
            TextNode("This ", "text"),
            LeafNode("b", "is"),
            TextNode(" a ", "text"),
            LeafNode("b", "text"),
            TextNode(" node", "text"),
            ]
            )

    def test_nest(self):
        node = TextNode("This **is** a *text* node", "text")
        node_list = split_nodes_delimiter([node], '**', 'bold')
        node_list = split_nodes_delimiter(node_list, '*', 'italic')
        self.assertEqual(node_list, [
            TextNode("This ", "text"),
            LeafNode("b", "is"),
            TextNode(" a ", "text"),
            LeafNode("i", "text"),
            TextNode(" node", "text"),
            ]
            )
class TestGetLink(unittest.TestCase):
    def test_one_img(self):
        text = "Hello ![link](lol) world"
        self.assertEqual([('link','lol')],extract_markdown_images(text))
    def test_two_img(self):
        text = "Hello ![link](lol) world this ![is](linky)"
        self.assertEqual([("link","lol"),("is","linky")],extract_markdown_images(text))
    def test_one_link(self):
        text = "Hello [link](lol) world"
        self.assertEqual([('link','lol')],extract_markdown_links(text))
    def test_two_links(self):
        text = "Hello [link](lol) world this [is](linky)"
        self.assertEqual([("link","lol"),("is","linky")],extract_markdown_links(text))
    def test_img_and_link(self):
        text = "Hello ![link](lol) world this [is](linky)"
        self.assertEqual([("link","lol"),],extract_markdown_images(text))
    def test_img_and_link(self):
        text = "Hello ![link](lol) world this [is](linky)"
        self.assertEqual([("is","linky"),],extract_markdown_links(text))

class TestSplitLink(unittest.TestCase):
    def test_text(self):
        node = TextNode("Hello ![lol](link) world","text")
        split = [
                TextNode("Hello ", "text"),
                LeafNode("img", "", {'src':'link','alt':'lol'}),
                TextNode(" world", "text"),
                ]
        self.assertEqual(split,split_nodes_links([node]))
    def test_text2(self):
        node = TextNode("Hello [lol](link) world","text")
        split = [
                TextNode("Hello ", "text"),
                LeafNode("a", "lol", {'href':'link'}),
                TextNode(" world", "text"),
                ]
        self.assertEqual(split,split_nodes_links([node]))

    def test_leaves(self):
        node = LeafNode('i',"Hello ![alt](link) world")
        split = [
                LeafNode("i", "Hello "),
                LeafNode("img", "", {'src':'link','alt':'alt'}),
                LeafNode("i", " world"),
                ]
        self.assertEqual(split,split_nodes_links([node]))

    def test_both_text(self):
        node = TextNode("Hello ![lol](link) world with [two](links)", 'text')
        split = [
                TextNode( "Hello ", 'text'),
                LeafNode("img", "", {'src':'link','alt':'lol'}),
                TextNode(" world with ", 'text'),
                LeafNode("a", "two", {'href':'links'}),
                ]
        self.assertEqual(split,split_nodes_links([node]))
    def test_both(self):
        node = LeafNode('i',"Hello ![lol](link) world with [two](links)")
        split = [
                LeafNode("i", "Hello "),
                LeafNode("img", "", {'src':'link','alt':'lol'}),
                LeafNode("i", " world with "),
                LeafNode("a", "two", {'href':'links'}),
                ]
        self.assertEqual(split,split_nodes_links([node]))

    def test_both2(self):
        node = LeafNode('i',"Hello ![lol](link) world with [two](links)")
        node2 = LeafNode('b',"llama ![lol](link) ballama lamaa lambada [two](links) wow")
        split = [
                LeafNode("i", "Hello "),
                LeafNode("img", "", {'src':'link','alt':'lol'}),
                LeafNode("i", " world with "),
                LeafNode("a", "two", {'href':'links'}),
                LeafNode("b", "llama "),
                LeafNode("img", "", {'src':'link','alt':'lol'}),
                LeafNode("b", " ballama lamaa lambada "),
                LeafNode("a", "two", {'href':'links'}),
                LeafNode("b", " wow"),
                ]
        self.assertEqual(split,split_nodes_links([node, node2]))

class TestIngest(unittest.TestCase):
    def test_text(self):
        text = "This is **text** with an *italic* word and a `code block` and an \
![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        split = [
                TextNode("This is ", "text"),
                LeafNode("b","text"),
                TextNode(" with an ", "text"),
                LeafNode("i", "italic"),
                TextNode(" word and a ", "text"),
                LeafNode("code", "code block"),
                TextNode(" and an ", "text"),
                LeafNode("img", "", {'src':'https://i.imgur.com/fJRm4Vk.jpeg','alt':'obi wan image'}),
                TextNode(" and a ", "text"),
                LeafNode("a", "link", {'href':'https://boot.dev'}),
                ]
        self.assertEqual(split,text_to_textnodes(text))

class TestTextNodes2HtmlNodes(unittest.TestCase):
    def test_do_they_all_leaves(self):
        text = "This is **text** with an *italic* word and a `code block` and an \
![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        split = [
                LeafNode(None,"This is "),
                LeafNode("b","text"),
                LeafNode(None," with an "),
                LeafNode("i", "italic"),
                LeafNode(None," word and a "),
                LeafNode("code", "code block"),
                LeafNode(None," and an "),
                LeafNode("img", "", {'src':'https://i.imgur.com/fJRm4Vk.jpeg','alt':'obi wan image'}),
                LeafNode(None," and a "),
                LeafNode("a", "link", {'href':'https://boot.dev'}),
                ]
        self.assertEqual(split,textnodes_to_htmlnodes(text))
        self.assertEqual(list, type(textnodes_to_htmlnodes(text)))
        self.assertNotEqual(list, type(textnodes_to_htmlnodes(text)[0]))
        self.assertEqual(LeafNode, type(textnodes_to_htmlnodes(text)[0]))

class TestMarkdown2Block(unittest.TestCase):
    def test_blocks(self):
        text = '''Hello world, this is **cool text**

        additionally, this is a second paragraph

        finally, *this* is the last paragraph
        '''
        blocks = [
                'Hello world, this is **cool text**',
                'additionally, this is a second paragraph',
                'finally, *this* is the last paragraph',
                ]

        self.assertEqual(blocks, markdown_to_blocks(text))

    def test_blocks_trailing(self):
        text = '''Hello world, this is **cool text**

        additionally, this is a second paragraph

        finally, *this* is the last paragraph



        '''
        blocks = [
                'Hello world, this is **cool text**',
                'additionally, this is a second paragraph',
                'finally, *this* is the last paragraph',
                ]

        self.assertEqual(blocks, markdown_to_blocks(text))

    def test_blocks_middle(self):
        text = '''Hello world, this is **cool text**

        additionally, this is a second paragraph



        finally, *this* is the last paragraph
        '''
        blocks = [
                'Hello world, this is **cool text**',
                'additionally, this is a second paragraph',
                'finally, *this* is the last paragraph',
                ]

        self.assertEqual(blocks, markdown_to_blocks(text))

    def test_blocks_long(self):
        text = '''Hello world, this is **cool text**

        additionally, this is a second paragraph
this is an additional sentence in this block



        finally, *this* is the last paragraph
        '''
        blocks = [
                'Hello world, this is **cool text**',
                'additionally, this is a second paragraph\nthis is an additional sentence in this block',
                'finally, *this* is the last paragraph',
                ]

        self.assertEqual(blocks, markdown_to_blocks(text))

class TestBlock2BlockType(unittest.TestCase):
    def test_heading3(self):
        block = "### Hello world"
        block_type = "h3"

        self.assertEqual(block_type, block_to_block_type(block))

    def test_code(self):
        block = "```\nHello world\n```"
        block_type = "code"

        self.assertEqual(block_type, block_to_block_type(block))

    def test_quote(self):
        block = "> hello\n> world"
        block_type = "blockquote"

        self.assertEqual(block_type, block_to_block_type(block))

    def test_unordered(self):
        block = "- hello\n- world"
        block_type = "ul"

        self.assertEqual(block_type, block_to_block_type(block))

    def test_ordered(self):
        block = "1. hello\n2. world"
        block_type = "ol"

        self.assertEqual(block_type, block_to_block_type(block))

    def test_other(self):
        block = "hello\nworld"
        block_type = "p"

        self.assertEqual(block_type, block_to_block_type(block))

class TestExtractTitle(unittest.TestCase):
    def test_basic(self):
        html = ParentNode('div',[
            ParentNode('h2',[LeafNode(None,'fail')]),
            ParentNode('h1',[LeafNode(None,'test')]),
            ])
        self.assertEqual('test',extract_title(html))
        # The title
    def test_fail(self):
        html = ParentNode('div',[
            ParentNode('h2',[LeafNode(None,'fail')]),
            ParentNode('h3',[LeafNode(None,'test')]),
            ])
        self.assertRaises(Exception,extract_title,html)

class TestMD2HTMLnodes(unittest.TestCase):
    def test_basic(self):
        markdown = '''
        # The title

        This is a cool *document* that is written
this is another line

        On a computer at [moricorp](moricorp.xyz)
        '''
        html = ParentNode('div',[
            ParentNode('h1',[LeafNode(None,'The title')]),
            ParentNode('p',[
            LeafNode(None,'This is a cool '),
            LeafNode('i','document'),
            LeafNode(None, ' that is written\nthis is another line'),
            ]),
            ParentNode('p',[
                LeafNode(None, 'On a computer at '),
                LeafNode('a', 'moricorp',{'href':'moricorp.xyz'}),
                ]),
            ])


        self.assertEqual(html, markdown_to_html_node(markdown))

    def test_basic(self):
        markdown = '''
        ## The title

        > This is a cool *document* that is written
> this is another line

        - On a computer at 
- A secret location
        '''
        html = ParentNode('div',[
            ParentNode('h2',[LeafNode(None,'The title')]),
            ParentNode('blockquote',[
            LeafNode(None,'This is a cool '),
            LeafNode('i','document'),
            LeafNode(None, ' that is written\nthis is another line'),
            ]),
            ParentNode('ul',[
                LeafNode(None, '<li>On a computer at </li>\n<li>A secret location</li>'),
                ]),
            ])


        self.assertEqual(html, markdown_to_html_node(markdown))


if __name__ == '__main__':
    unittest.main()
