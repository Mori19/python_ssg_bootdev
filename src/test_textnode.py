import unittest 

from textnode import TextNode, text_node_to_html_node
from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq2(self):
        node = TextNode("This is NOT a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

    def test_neq3(self):
        node = TextNode("This is NOT a text node", "italic")
        node2 = TextNode("This is a text node", "bold")
        self.assertNotEqual(node, node2)

class TestText2HTML(unittest.TestCase):
    def test_bold(self):
        tnode = TextNode("Hello world", "bold")
        hnode = text_node_to_html_node(tnode)
        lnode = LeafNode("b","Hello world")
        self.assertEqual(hnode, lnode)

    def test_img(self):
        tnode = TextNode("Hello world", "image", "www.moricorp.xyz")
        hnode = text_node_to_html_node(tnode)
        lnode = LeafNode("img","", {'src':"www.moricorp.xyz", 'alt':'Hello world'})
        self.assertEqual(hnode, lnode)

if __name__ == '__main__':
    unittest.main()
