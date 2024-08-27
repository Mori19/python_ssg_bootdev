import unittest 

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_empty_props(self):
        node = HTMLNode(props=None)
        self.assertEqual(node.props_to_html(), '')

    def test_single_prop(self):
        node = HTMLNode(props={'href':'www.lol.com'})
        self.assertEqual(node.props_to_html(), '')
    def test_single_prop(self):
        node = HTMLNode(props={'href':'www.lol.com'})
        self.assertEqual(node.props_to_html(), ' href="www.lol.com"')
    def test_multiple_props(self):
        node = HTMLNode(props={'href':'www.lol.com', 'img':'haha'})
        self.assertEqual(node.props_to_html(), ' href="www.lol.com" img="haha"')

class TestLeafNode(unittest.TestCase):
    def test_leaf_p(self):
        node = LeafNode('p','hello world',None)
        self.assertEqual(node.to_html(), "<p>hello world</p>")
    def test_leaf_none(self):
        node = LeafNode(None,'hello world',None)
        self.assertEqual(node.to_html(), "hello world")
    def test_leaf_href(self):
        node = LeafNode('a','hello world',{"href":"www.moricorp.xyz"})
        self.assertEqual(node.to_html(), '<a href="www.moricorp.xyz">hello world</a>')

class TestParentNode(unittest.TestCase):
    def test_parent_single(self):
        children = [
                LeafNode('b', 'hello'),
                ]
        node = ParentNode('p', children)
        self.assertEqual(node.to_html(), '<p><b>hello</b></p>')

    def test_parent_two(self):
        children = [
                LeafNode('b', 'hello'),
                LeafNode('i', 'world'),
                ]
        node = ParentNode('p', children)
        self.assertEqual(node.to_html(), '<p><b>hello</b><i>world</i></p>')
    
    def test_parent_nested(self):
        children = [
                LeafNode('b', 'hello'),
                ParentNode('i', [LeafNode(None,'world')]),
                ]
        node = ParentNode('p', children)
        self.assertEqual(node.to_html(), '<p><b>hello</b><i>world</i></p>')

    def test_parent_nexted_two_layers(self):
        children = [
                LeafNode('b', 'hello'),
                ParentNode('i', [ParentNode('strong',
                                            [
                                                LeafNode('a','world', {'href':'lol'}),
                                                LeafNode('b', 'this is cool'),
                                                ]
                                            )
                                 ]),
                ]
        node = ParentNode('p', children)
        self.assertEqual(node.to_html(), '<p><b>hello</b><i><strong><a href="lol">world</a><b>this is cool</b></strong></i></p>')

if __name__ == '__main__':
    unittest.main()
