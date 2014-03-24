from readability import Document


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
        self.__extract()

    def __extract(self):
        doc = Document(self.html,
                       negative_keywords=self.negative_keywords)
        self.title = doc.short_title()
        self.content = doc.summary(html_partial=True)
