# -*- coding: utf-8 -*-

import urllib2
import re
import codecs
import HTMLParser
import os

hPrs = HTMLParser.HTMLParser()

visited = []
to_be_visited = []

thaipoem_visited = []
thaipoem_to_be_visited = []


def crawl_forward(link):
    infile = urllib2.urlopen(link)
    raw_text = infile.read()
    text = raw_text.decode("utf-8")
    infile.close()
    return text


def thaipoem_parse(unclear_text):
    # This didn't work in cases with \n within tag pre
    #
    # thai_article = []
    # lines = unclear_text.split('\n')
    # fl = 0
    # for line in lines:
    #     if fl == 1:
    #         print fl, line
    #     if '</pre>' in line:
    #         fl = 0
    #     if fl == 1:
    #         line = hPrs.unescape(line)
    #         thai_article.append(line)
    #     if '<pre>' in line:
    #         fl = 1

    find_text = re.search(u'<pre.*?>(.*)</pre>', unclear_text, re.DOTALL)
    if find_text is not None:
        output = re.sub(u'<.*?>', u'', find_text.group(1), flags=re.U)
        output = re.sub(u'\.+', u'', output, flags=re.U)
        output = re.sub(u'\t+', u'', output, flags=re.U)
        output = re.sub(u'\n+', u'\n', output, flags=re.U)
        output += u'</text>'
        return output


def check_links(text, visited, to_be_visited):
    links = []
    if u"http://www.thaipoem.com/" in visited:
        links = re.findall(u' href="(.*/[0-9]+)"', text)
    for link in links:
        # print link
        if link in visited:
            continue
        else:
            if not u'img' in link:
                to_be_visited.append(link)
    to_be_visited = set(to_be_visited)
    to_be_visited = list(to_be_visited)
    return to_be_visited

thaipoem_texts = crawl_forward(u"http://www.thaipoem.com/")

thaipoem_visited.append(u"http://www.thaipoem.com/")
thaipoem_to_be_visited = check_links(thaipoem_texts, thaipoem_visited, thaipoem_to_be_visited)
i = 1
print len(thaipoem_to_be_visited)
for link in thaipoem_to_be_visited:
    # if i > 2:
    #     break
    link = link.replace(u"http://", u"")
    link = urllib2.quote(link.encode('utf-8'))
    if u'www.thaipoem.com' in link:
        link = u"http://" + link
    text = crawl_forward(link)
    thaipoem_visited.append(link)
    thaipoem_to_be_visited = check_links(thaipoem_texts, thaipoem_visited, thaipoem_to_be_visited)
    final_txt = thaipoem_parse(text)
    filename = str(i) + ".txt"
    print str(i) + u" " + link
    i += 1
    if not os.path.exists(u'thaipoem/'):
        os.makedirs(u'thaipoem/')
    outfile = codecs.open(u'thaipoem/' + filename, "w", "utf-8")
    title = ''
    initial_str = u'<?xml version="1.0" encoding="UTF-8"?>\n<meta><link>' + link + u'</link>\n' +\
              u'<title>' + title + u'</title>\n<genre>poem</genre></meta>\n<text>\n'
    outfile.write(initial_str)
    outfile.write(final_txt)
    outfile.close()
