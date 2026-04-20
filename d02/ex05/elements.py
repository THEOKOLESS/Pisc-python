from elem import Elem, Text

def _attrs(attr):
    return {} if attr is None else attr


class Html(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('html', _attrs(attr), content)


class Head(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('head', _attrs(attr), content)


class Body(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('body', _attrs(attr), content)


class Title(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('title', _attrs(attr), content)


class Meta(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('meta', _attrs(attr), content, tag_type='simple')


class Img(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('img', _attrs(attr), content, tag_type='simple')


class Table(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('table', _attrs(attr), content)


class Tr(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('tr', _attrs(attr), content)


class Td(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('td', _attrs(attr), content)


class Th(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('th', _attrs(attr), content)


class Ul(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('ul', _attrs(attr), content)


class Ol(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('ol', _attrs(attr), content)


class Li(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('li', _attrs(attr), content)


class P(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('p', _attrs(attr), content)


class Hr(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('hr', _attrs(attr), content, tag_type='simple')


class Br(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('br', _attrs(attr), content, tag_type='simple')


class H1(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('h1', _attrs(attr), content)


class H2(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('h2', _attrs(attr), content)


class Div(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('div', _attrs(attr), content)


class Span(Elem):
    def __init__(self, content=None, attr=None):
        super().__init__('span', _attrs(attr), content)



if __name__ == "__main__":

    page = Html([
        Head(Title(Text('"Hello ground!"'))),
        Body([
            H1(Text('"Oh no, not again!"')),
            Img(attr={'src': 'http://i.imgur.com/pfp3T.jpg'})
        ])
    ])
    print(page)