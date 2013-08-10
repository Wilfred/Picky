from urllib import quote

from django.core.urlresolvers import reverse

from creoleparser.dialects import create_dialect, creole10_base
from creoleparser.core import Parser

from bs4 import BeautifulSoup


def is_external(url):
    # FIXME: detect when external URLs are actually for the current
    # host
    if url.startswith('http://') or url.startswith('https://'):
        return True

    return False


def render_creole(source):
    dialect = create_dialect(creole10_base, wiki_links_base_url="/page/")
    parser = Parser(dialect=dialect, method='html', encoding=None)

    html = parser.render(source)

    # add favicons to external URLs
    soup = BeautifulSoup(html)
    for a_tag in soup.find_all('a'):
        url = a_tag['href']
        if is_external(url):
            favicon = soup.new_tag('img')
            favicon['src'] = "//getfavicon.appspot.com/" + quote(url)
            favicon['class'] = 'favicon'

            a_tag.insert_before(favicon)

    # circular import fix
    from .models import Page

    # build a set of all possible internal links
    page_urls = set()
    for page in Page.objects.all():
        # Since we can link to both slugs and original names, we
        # consider both.
        page_urls.add(reverse('view_page', args=[page.name]))
        page_urls.add(reverse('view_page', args=[page.name_slug]))

    # add a class to links to nonexistent pages
    for a_tag in soup.find_all('a'):
        url = a_tag['href']
        if not is_external(url):
            if not url.endswith('/'):
                url = url + '/'

            if url not in page_urls:
                a_tag['class'] = 'nonexistent'

    return soup.find('body').encode_contents().decode('utf8')

