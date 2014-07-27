from readability import Document
from lxml import etree
from django.conf import settings


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


def elem_attr_contain(elem, terms):
    """
    Returns True if an element's id or class contains one of the given
    terms.
    """
    if elem.get('id') is not None and \
       len(list(set(elem.get('id').split(' ')) &
                set(terms))) > 0:
        return True
    elif elem.get('class') is not None and \
        len(list(set(elem.get('class').split(' ')) &
                 set(terms))) > 0:
        return True
    return False


def cleanup(root, title=None):
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
    if title and \
       len(list(root)) > 0 and \
       root[0].tag in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6'] and \
       root[0].text == title:
        root.remove(root[0])
    # check if the elements towards the end can be identified as ads or
    # post metadata
    while len(list(root)) > 1:
        last_elem = root[len(list(root))-1]
        if not contains_text(last_elem):
            root.remove(last_elem)
            continue
        if elem_attr_contain(last_elem, settings.ARTEX_METADATA_TERMS):
            root.remove(last_elem)
        else:
            break
    return root


def elem_content_to_string(root):
    """
    Converts all content wrapped by an element to a string (i.e. all child
    elements and text before, after and between them).
    """
    result = u''
    if root.text is not None and root.tag == 'div':
        result += root.text
    else:
        result += etree.tostring(root)
    for elem in list(root):
        result += etree.tostring(elem)
    return result.strip()


def extract_article(html, title=None):
    """
    Wraps around readability.Document and returns the articles
    title and content.
    """
    doc = Document(html, negative_keywords=settings.ARTEX_NEGATIVE_KEYWORDS)
    doc_title = doc.short_title()
    # invoke the summary method to invoke readability's magic
    doc.summary(html_partial=True)
    # obtain the article as HtmlElement tree:
    html_tree = doc.html
    # clean up the article html:
    clean_html = cleanup(html_tree, doc_title)
    # check if the outer element is a tag from negative_keywords
    if elem_attr_contain(clean_html, settings.ARTEX_NEGATIVE_KEYWORDS):
        bad_attr = True
    else:
        bad_attr = False
    if clean_html.tag in settings.ARTEX_NEGATIVE_KEYWORDS or bad_attr:
        # if so, redo extraction with min_text_length set to 0
        doc = Document(html,
                       negative_keywords=settings.ARTEX_NEGATIVE_KEYWORDS,
                       min_text_length=0)
        doc_title = doc.short_title()
        # invoke the summary method to invoke readability's magic
        doc.summary(html_partial=True)
        # obtain the article as HtmlElement tree:
        html_tree = doc.html
        # clean up the article html:
        clean_html = cleanup(html_tree, doc_title)
    content = elem_content_to_string(clean_html)
    if title:
        # if the extracted title is not a subset of given title, use
        # the given title (b/c we assume this is more accurate, but
        # maybe with some unneccessary boilerplate).
        if not doc_title in title or doc_title == '':
            doc_title = title
    return doc_title, content
