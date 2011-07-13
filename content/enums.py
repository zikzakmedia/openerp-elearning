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

"""
Home base for all application enums.
"""
from django.utils.translation import ugettext_lazy as _

STATUS_ACTIVE = 1
STATUS_INACTIVE = 0

STATUS_CHOICES = (
    (STATUS_ACTIVE, _('Active')),
    (STATUS_INACTIVE, _('Inactive')),
)
