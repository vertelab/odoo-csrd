# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) {year} {company} (<{mail}>)
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
#
# https://www.odoo.com/documentation/14.0/reference/module.html
#
{
    'name': 'CSRD: Product ESRS Line',
    'version': '18.0.1.0.0',
    'summary': """This module makes it possible to add ESRS information to products, like the amount of CO2 used in manufacturing.""",
    'category': '', # Technical Settings|Localization|Payroll Localization|Account Charts|User types|Invoicing|Sales|Human Resources|Operations|Marketing|Manufacturing|Website|Theme|Administration|Appraisals|Sign|Helpdesk|Administration|Extra Rights|Other Extra Rights|
    'description': '''
Product ESRS Line
=================

    This module makes it possible to add ESRS information to products, like the amount of CO2 used in manufacturing.

    Features:

        - UI Integration: Extends 2 view(s) in the Odoo interface.
        - Extends Odoo: Builds on account.move, csrd.esrs, esrs.data.type, esrs.line.
    ''',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-csrd/csrd_product_esrs',
    'images': ['static/description/banner.png'], # 560x280
    'license': 'AGPL-3',
    'depends': ["mrp","csrd_esrs_line"],
    'data': ["security/ir.model.access.csv", "views/product_product_views.xml"],
    'demo': [],
    'application': False,
    'installable': True,    
    'auto_install': False,
    #"post_init_hook": "post_init_hook",
}
