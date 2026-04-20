from elem import Elem, Text
from elements import (
    Html,
    Head,
    Body,
    Title,
    Meta,
    Img,
    Table,
    Tr,
    Td,
    Th,
    Ul,
    Ol,
    Li,
    H1,
    H2,
    P,
    Div,
    Span,
    Hr,
    Br,
)


class Page:
    """
    Page will permit us to represent an entire HTML page, including the
    doctype.
    """
    DOCTYPE = "<!DOCTYPE html>"

    def __init__(self, root):
        if not isinstance(root, Elem):
            raise TypeError("Page content must be an instance of an inherited class Elem.")
        self.root = root

    def __str__(self):
        content = str(self.root)
        if isinstance(self.root, Html):
            return self.DOCTYPE + "\n" + content
        return content

    def write_to_file(self, filename):
        with open(filename, "w", encoding="utf-8") as file:
            file.write(str(self))

    def is_valid(self):
        return self._validate_node(self.root)

    def _children(self, node):
        if isinstance(node, Text):
            return []
        return node.content

    def _validate_node(self, node):
        allowed = (
            Html,
            Head,
            Body,
            Title,
            Meta,
            Img,
            Table,
            Th,
            Tr,
            Td,
            Ul,
            Ol,
            Li,
            H1,
            H2,
            P,
            Div,
            Span,
            Hr,
            Br,
            Text,
        )

        if not isinstance(node, allowed):
            return False

        children = self._children(node)

        if isinstance(node, Html):
            if len(children) != 2:
                return False
            if not isinstance(children[0], Head) or not isinstance(children[1], Body):
                return False

        elif isinstance(node, Head):
            if len(children) != 1 or not isinstance(children[0], Title):
                return False

        elif isinstance(node, (Body, Div)):
            allowed_children = (H1, H2, Div, Table, Ul, Ol, Span, Text)
            if any(not isinstance(child, allowed_children) for child in children):
                return False

        elif isinstance(node, (Title, H1, H2, Li, Th, Td)):
            if len(children) != 1 or not isinstance(children[0], Text):
                return False

        elif isinstance(node, P):
            if any(not isinstance(child, Text) for child in children):
                return False

        elif isinstance(node, Span):
            if any(not isinstance(child, (Text, P)) for child in children):
                return False

        elif isinstance(node, (Ul, Ol)):
            if len(children) == 0:
                return False
            if any(not isinstance(child, Li) for child in children):
                return False

        elif isinstance(node, Tr):
            if len(children) == 0:
                return False
            if any(not isinstance(child, (Th, Td)) for child in children):
                return False
            has_th = any(isinstance(child, Th) for child in children)
            has_td = any(isinstance(child, Td) for child in children)
            if has_th and has_td:
                return False

        elif isinstance(node, Table):
            if any(not isinstance(child, Tr) for child in children):
                return False

        for child in children:
            if not self._validate_node(child):
                return False
        return True


if __name__ == "__main__":
    valid_page = Page(
        Html(
            [
                Head(Title(Text('"Hello ground!"'))),
                Body(
                    [
                        H1(Text('"Oh no, not again!"')),
                        Div([Span([Text("inside span")])]),
                        Ul([Li(Text("item 1")), Li(Text("item 2"))]),
                        Table([Tr([Th(Text("header"))]), Tr([Th(Text("header 2"))])]),
                    ]
                ),
            ]
        )
    )

    invalid_head = Page(Html([Head([Title(Text("a")), Meta(attr={"charset": "utf-8"})]), Body()]))
    invalid_ul = Page(Html([Head(Title(Text("x"))), Body([Ul()])]))
    invalid_tr_mix = Page(Html([Head(Title(Text("x"))), Body([Table([Tr([Th(Text("h")), Td(Text("d"))])])])]))
    valid_span_p = Page(Html([Head(Title(Text("x"))), Body([Span([P([Text("ok")]), Text("ok")])])]))
    html_not_root = Page(Body([H1(Text("x"))]))

    assert valid_page.is_valid() is True
    assert invalid_head.is_valid() is False
    assert invalid_ul.is_valid() is False
    assert invalid_tr_mix.is_valid() is False
    assert valid_span_p.is_valid() is True
    assert html_not_root.is_valid() is True

    assert str(valid_page).startswith("<!DOCTYPE html>\n")

    out_file = "page_test_output2.html"
    valid_page.write_to_file(out_file)
    with open(out_file, "r", encoding="utf-8") as read_back:
        assert read_back.read() == str(html_not_root)

    print("All Page tests succeeded!")