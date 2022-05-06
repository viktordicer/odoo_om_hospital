from odoo import api, fields, models, _

class HospitalAppointment(models.Model):
  _name = "hospital.appointment"
  _inherit = ['mail.thread', 'mail.activity.mixin']
  _description ="Hospital Appointment"
  #_rec_name = 'ref'
  
  name = fields.Char(string='Name', default=lambda self: _('New'))
  patient_id = fields.Many2one('hospital.patient', string="Patient")
  gender = fields.Selection(related='patient_id.gender')
  appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
  booking_date = fields.Date(string='Booking Date',  default=fields.Date.context_today)
  ref = fields.Char(string='Reference')
  prescription = fields.Html(string='Prescription')
  priority = fields.Selection([
    ('0', 'Normal'),
    ('1', 'Low'),
    ('2', 'High'),
    ('3', 'Very High')], string='Priority')
  
  state = fields.Selection([
    ('draft', 'Draft'),
    ('in_consultation', 'In Consultation'),
    ('done', 'Done'),
    ('cancel', 'Cancel')], default='draft', string='Status', required=True, tracking=True)
  
  doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)
  pharmacy_line_ids = fields.One2many('apointment.pharmacy.lines', 'appointment_id', string='Pharmacy')
  
  @api.model
  def create(self,vals):
    vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
    return super(HospitalAppointment, self).create(vals)

  def write(self, vals):
    if not self.name and not vals.get('name'):
      vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
    return super(HospitalAppointment,self).write(vals)
  
  @api.onchange('patient_id')
  def onchange_patient_id(self):
    self.ref = self.patient_id.ref
    
  def action_in_cunsultation(self):
    for rec in self:
      if rec.state == 'draft':
        rec.state = 'in_consultation'
      
  def action_done(self):
    for rec in self:
      rec.state = 'done'
      
  def action_cancel(self):
    for rec in self:
      rec.state = 'cancel'
      
  def action_draft(self):
    for rec in self:
      rec.state = 'draft'
      
      
class AppointmentPharmacyLines(models.Model):
  _name = "apointment.pharmacy.lines"
  _description = "Appointment Pharmacy Lines"
  
  product_id = fields.Many2one('product.product', required=True)
  price_unit = fields.Float(related='product_id.list_price')
  qty = fields.Integer(string='Quantity', default=1)
  appointment_id = fields.Many2one('hospital.appointment', string='Appointment')