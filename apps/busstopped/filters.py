import re

from tipfy.ext.jinja2 import get_jinja2_instance
from django.utils.text import truncate_html_words

def filter_date(value, format):
    return value.strftime(format)

def filter_truncate_html_words(value, length):
    return truncate_html_words(value, length)

def filter_slugify(value):
    """
    Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    import unicodedata
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = unicode(re.sub('[^\w\s-]', '', value).strip().lower())
    return re.sub('[-\s]+', '-', value)

# Templating functions
env = get_jinja2_instance()
env.filters['date'] = filter_date
env.filters['truncatewords_html'] = filter_truncate_html_words
env.filters['slugify'] = filter_slugify
