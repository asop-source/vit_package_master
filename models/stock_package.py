
from odoo import api, fields, models, _
import time
import datetime
from odoo.exceptions import UserError
import logging
from odoo.http import request
_logger = logging.getLogger(__name__)


class Package_Quant(models.Model):
	_inherit = "stock.quant.package"
	
	package_ids = fields.One2many('stock.quant.package', 'package_baru_id', string='Child Package',)
	package_baru_id = fields.Many2one(string='Package Baru', comodel_name='stock.quant.package', store=True)
	active = fields.Boolean('Active', default=True)
	jenis_package = fields.Selection([
        ('besar', 'Package Besar'),
        ('kecil','Package Kecil')],
        compute ='_onchange_package', store=True)

	keterangan = fields.Text(string='Keterangan')
	
	# @api.one
	# @api.constrains('package_ids')
	@api.depends('package_ids','name','active')
	def _onchange_package(self):
		for rec in self:
			if rec.package_ids:
				rec.jenis_package = 'besar'
			else:
				rec.jenis_package = 'kecil'



	@api.multi
	def create_package_ids(self):
		action = self.env.ref('vit_package_master.action_repack_wizard')
		result = action.read()[0]

		id_pack = []
		for x in self.package_ids:
			id_pack.append(x.id)

		result['context'] = {
			'default_package_ids': id_pack,
		}
		
		return result