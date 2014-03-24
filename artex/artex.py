from readability import Document
from lxml import etree


def contains_text(element):
    """
    Checks if the element contains any text before, after or between child
    elements.
    """
    if element.text is not None and element.text.strip() != '':
        return True
    for child in list(element):
        if child.tail is not None and child.tail.strip() != '':
            return True
    return False


def cleanup(root, title):
    """
    Remove redundant outmost divs until one remains as root. Also check
    if the div contains text that is not wrapped in other elements so
    that we don't loose the content. Also remove headers at the start if
    they contain the title of the article.
    """
    # remove outer redundant divs
    while root.tag == 'div' and len(list(root)) == 1:
        # make sure there is no non-whitespace content beyond children
        if not contains_text(root):
            root = root[0]
        else:
            break
    # if the first child is a header and its text equals the title
    # it is redundant and gets removed.
    if root[0].tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and \
       root[0].text == title:
        root = root[1:]
    return u''.join(map(lambda a: etree.tostring(a).strip(),
                        list(root)))


class Article():
    """
    Wraps around readability.Document and provides access to the article
    title and content.
    """
    negative_keywords = ['widget', 'aside', 'sidebar', 'metadata', 'cmnt',
                         'comment', 'adsense', 'advert', 'widget_text']
    min_text_length_fallback = 0

    def __init__(self, html):
        """ Sets the article html. """
        self.html = html
        self._extract()

    def _extract(self):
        doc = Document(self.html,
                       negative_keywords=self.negative_keywords)
        self.title = doc.short_title()

        # invoke the summary method to invoke readability's magic
        doc.summary(html_partial=True)
        # obtain the article as HtmlElement tree:
        html_tree = doc.html
        # clean up the article html:
        self.content = cleanup(html_tree, self.title)

