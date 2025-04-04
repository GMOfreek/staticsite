import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    # testing for HTMLNode class
    def test_to_html_props(self):
        prop_test = {"href": "https://www.google.com", "target": "_blank",}
        node = HTMLNode(None, None, None, prop_test)
        node2 = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), node2)

    def test_values(self):
        node = HTMLNode("div", "I wish I could read",)
        self.assertEqual(node.tag, "div",)
        self.assertEqual(node.value, "I wish I could read",)
        self.assertEqual(node.children, None,)
        self.assertEqual(node.props, None,)

    def test_html_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(
            node.__repr__(), 
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})"
        )

    
    #testing for LeafNode class
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("a", None)
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(str(context.exception), "All leaf nodes must have a value.")
    

    #testing for ParentNode class
    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_to_html_no_children(self):
        parent_node = ParentNode("a", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have a child node.")

    def test_parent_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertEqual(str(context.exception), "All parent nodes must have a tag.")


if __name__ == "__main__":
    unittest.main()