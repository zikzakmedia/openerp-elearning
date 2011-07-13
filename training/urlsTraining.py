# -*- encoding: utf-8 -*-
############################################################################################
#
#    OpenERP e-learning, Open Source Management Solution
#    Copyright (C) 2011 Zikzakmedia S.L. (<http://www.zikzakmedia.com>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
############################################################################################

from django.conf.urls.defaults import *
from training.views import *

"""Urls Training"""
urlpatterns = patterns("",
    (r'^$', 'training.views.index'),
    (r"^(?P<offer>[^/]+)/$", 'training.views.offer'),
    (r"^(?P<offer>[^/]+)/wiki/(?P<wiki>[^/]+)$", 'training.views.wiki'),
    (r"^(?P<offer>[^/]+)/(?P<course>[^/]+)/questionarie/(?P<exam>[^/]+)$", 'training.views.exam'),
    (r"^(?P<offer>[^/]+)/(?P<course>[^/]+)/answer/(?P<exam>[^/]+)$", 'training.views.exam'),
    (r"^(?P<offer>[^/]+)/(?P<course>[^/]+)/(?P<exam>[^/]+)$", 'training.views.exam'),
)
