from datetime import date
from odoo import api, fields, models

class HospitalPatient(models.Model):
  _name = "hospital.patient"
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _description = "Hospital Patient"
  
  name = fields.Char(string='Name', tracking=True)
  date_of_birth = fields.Date(string='Date Of Birth', tracking=True)
  ref = fields.Char(string='Reference')
  age = fields.Integer(string="Age", compute='_compute_age')
  gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
  active = fields.Boolean(string="Active", default=True)
  tag_ids = fields.Many2many('patient.tag', string="Tags")
  appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
  appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
  parent = fields.Char(string="Parent")
  marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="Marital Status",
                                    tracking=True)
  partner_name = fields.Char(string="Partner")
  
  
  @api.depends('appointment_ids')
  def _compute_appointment_count(self):
    for rec in self:
      rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
  
  @api.model
  def create(self,vals):
    vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
    return super(HospitalPatient, self).create(vals)
  
  def write(self, vals):
    if not self.ref and not vals.get('ref'):
      vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
    return super(HospitalPatient,self).write(vals)
  
  @api.depends('date_of_birth')
  def _compute_age(self):
    for rec in self:
      today = date.today()
      if rec.date_of_birth:
        rec.age = today.year - rec.date_of_birth.year - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
      else:
        rec.age = 0
        
  def name_get(self):
    return [(rec.id, "[%s] %s" % (rec.ref, rec.name)) for rec in self]
  
  def action_open_appointments(self):
    return {
      'type': 'ir.actions.act_window',
      'name' : 'Appointments',
      'res_model' : 'hospital.appointment',
      'domain' : [('patient_id', '=', self.id)],
      'view_mode' : 'tree',
      'target' : 'current', 
    }