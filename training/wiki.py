###############################################################################
#
# Copyright (C) 2007-TODAY Tiny ERP Pvt Ltd. All Rights Reserved.
#
# $Id$
#
# Developed by Tiny (http://openerp.com) and Axelor (http://axelor.com).
# Redesign this code use Wiki tags to Django by Zikzakmedia (http://www.zikzakmedia.com).
#
# The OpenERP web client is distributed under the "OpenERP Public License".
# It's based on Mozilla Public License Version (MPL) 1.1 with following
# restrictions:
#
# -   All names, links and logos of Tiny, OpenERP and Axelor must be
#     kept as in original distribution without any changes in all software
#     screens, especially in start-up page and the software header, even if
#     the application source code has been changed or updated or code has been
#     added.
#
# -   All distributions of the software must keep source code with OEPL.
#
# -   All integrations to any other software must keep source code with OEPL.
#
# If you need commercial licence to remove this kind of restriction please
# contact us.
#
# You can see the MPL licence at: http://www.mozilla.org/MPL/MPL-1.1.html
#
###############################################################################

import re
import random
import locale

from base64 import b64encode
from base64 import b64decode
from StringIO import StringIO

from tools.elearning import connOOOP

import wikimarkup

_image = re.compile(r'img:(.*)\.(.*)', re.UNICODE)
_rss = re.compile(r'rss:(.*)\.(.*)', re.UNICODE)
_attach = re.compile(r'attach:(.*)\.(.*)', re.UNICODE)
_internalLinks = re.compile(r'\[\[.*\]\]', re.UNICODE)
_edit = re.compile(r'edit:(.*)\|(.*)', re.UNICODE)
_view = re.compile(r'view:(.*)\|(.*)', re.UNICODE)

class WikiParser(wikimarkup.Parser):

    def parse(self, text, id):
        text = text.replace('&nbsp;', 'n-b-s-p')
        text = text.replace('&amp;', 'n-a-m-p')
        text = text.replace('&','&amp;')
        text = text.replace('n-b-s-p', '&nbsp;')
        text = text.replace('n-a-m-p', '&amp;')
        text = text.replace('<code>', '<pre>')
        text = text.replace('</code>', '</pre>')

        text = wikimarkup.to_unicode(text)
        text = self.strip(text)

        text = super(WikiParser, self).parse(text)
        text = self.addImage(text, id)
        text = self.attachDoc(text, id)
        text = self.recordLink(text)
        text = self.viewRecordLink(text)
        text = self.addInternalLinks(text)
        #TODO : already implemented but we will implement it later after releasing the 5.0
        #text = self.addRss(text, id)
        return text

    def viewRecordLink(self, text):
        def record(path):
            return ""

        bits = _view.sub(record, text)
        return bits

    def addRss(self, text, id):
        def addrss(path):
            rssurl = path.group().replace('rss:','')
            import rss.feedparser as feedparser
            data = feedparser.parse(rssurl)
            values = "<h2>%s</h2><br/>" % (data.feed.title)
            values += "%s<br/>" % (data.channel.description)
            for entry in data['entries']:
                values += "<h3><a href='%s'> %s </a></h3><br/>" % (entry.link, entry.title)
                values += "%s <br/>" % (entry.summary)

            return values

        bits = _rss.sub(addrss, text)
        return bits

    def attachDoc(self, text, id):
        def document(path):
            file = path.group().replace('attach:','')
            if file.startswith('http') or file.startswith('ftp'):
                return "<a href='%s'>Download File</a>" % (file)
            else:
                return "" #doc ir.attachment not available

        bits = _attach.sub(document, text)
        return bits

    def addImage(self, text, id):
        def image(path):
            file = path.group().replace('img:','')
            if file.startswith('http') or file.startswith('ftp'):
                return "<img src='%s'/>" % (file)
            else:
                return "" #img ir.attachment not available

        bits = _image.sub(image, text)
        return bits

    def recordLink(self, text):
        def record(path):
            return "" #edit record not available

        bits = _edit.sub(record, text)
        return bits

    def addInternalLinks(self, text):
        #~ proxy = rpc.RPCProxy('wiki.wiki')
        
        def link(path):
            link = path.group().replace('[','').replace('[','').replace(']','').replace(']','').split("|")
            name_to_search = link[0].strip()
            conn = connOOOP()
            mids = conn.WikiWiki.filter(name__ilike=name_to_search)
            if len(mids)>0:
                link_str = "<a href='/training/[offer]/wiki/%s' alt='%s'>%s</a>" % (mids[0].alias, name_to_search, name_to_search)
            else:
                link_str = name_to_search

            return link_str

        bits = _internalLinks.sub(link, text)
        return bits

def wiki2html(text, showToc, id):
    p = WikiParser(show_toc=showToc)
    return p.parse(text, id)
