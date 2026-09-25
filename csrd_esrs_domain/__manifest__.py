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
    'name': 'CSRD: ESRS Datapoints Domain',
    'version': '18.0.1.0.0',
    'summary': """Adds a domain that allows one to create a connection from records in Odoo to ESRS datapoints. Example: How many employees are men and women, respectively.""",
    'category': '',
    'description': '''
ESRS Datapoints Domain
======================

    Adds a domain that allows one to create a connection from records in Odoo to ESRS datapoints.
            Example: How many employees are men and women, respectively.

    Features:

        - Automation: Scheduled jobs: CSRD Policy: check CSRD policy data point, CSRD Policy: check CSRD policy data point.
        - UI Integration: Extends 2 view(s) in the Odoo interface.
        - Extends Odoo: Builds on csrd.esrs.
    ''',
    'author': 'Vertel AB',
    'website': 'https://vertel.se/apps/odoo-csrd/csrd_esrs_domain',
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'depends': ['csrd_esrs'],
    'data': [
        'views/csrd_esrs_view.xml',
        'data/ir_cron.xml'
    ],
    'demo': [],
    'application': False,
    'installable': True,
    'auto_install': False,
}
