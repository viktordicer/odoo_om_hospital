from odoo import api, fields, models

class PatientTag(models.Model):
  _name = "patient.tag"
  _description = "Patient Tag"
  
  name = fields.Char(string='Name', required=True)
  active = fields.Boolean(string='Active', default=True)
  color =fields.Integer(string='Color')
  
  _sql_constraints = [
    ('unique_tag_name', 'unique (name, active)', 'Key must be unique.')
  ]