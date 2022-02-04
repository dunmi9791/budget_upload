# -*- coding:utf-8 -*-

import base64
import xlrd
import datetime

from odoo import models,fields,api,_
from odoo.exceptions import ValidationError
from openerp.exceptions import UserError

class ImportBudgetLineWizard(models.TransientModel):
    _name = "import.budget.line.wizard"

    files = fields.Binary(
        string="Import Excel File",
        redonly=True
    )
    datas_fname = fields.Char(
        string = 'Import File Name'
    )

    @api.multi
    def budget_file(self):
        active_id = self._context.get('active_id')
        budget_id = self.env['account.analytic.crossovered.budget'].browse(active_id)
        try:
            workbook = xlrd.open_workbook(file_contents = base64.decodestring(self.files))
        except:
            raise ValidationError("Please select .xls/xlsx file.")
        sheet_name = workbook.sheet_names()
        sheet = workbook.sheet_by_name(sheet_name[0])
        date_from = budget_id.date_from
        date_to = budget_id.date_to
        number_of_rows = sheet.nrows
        row = 1
        while(row < number_of_rows):
            general_budget_id = self.env['account.analytic.budget.post'].search([('name','=',sheet.cell(row,0).value)])
            if not general_budget_id:
                raise ValidationError('Budgetory Position not found for Budgetory Position :%s at row number %s '%(sheet.cell(row,0).value,row+1))
            analytic_account_id = self.env['account.analytic.account'].search([('code','=',sheet.cell(row,1).value)])
            if not analytic_account_id:
                raise ValidationError('Analytic Account not found for Analytic Account :%s at row number %s '%(sheet.cell(row,1).value,row+1))
            try:
                date_from = sheet.cell(row,2).value
                date_from = datetime.datetime.strptime(date_from, "%m/%d/%Y")
            except:
                raise ValidationError('Start Date not found for Start Date :%s at row number %s '%(sheet.cell(row,2).value,row+1))
            try:
                date_to = sheet.cell(row,3).value
                date_to = datetime.datetime.strptime(date_to, "%m/%d/%Y")
            except:
                raise ValidationError('End Date not found for End Date :%s at row number %s '%(sheet.cell(row,3).value,row+1))
            try:
                planned_amount = sheet.cell(row,4).value
            except:
                raise ValidationError('Planned Amount not found for Planned Amount :%s at row number %s '%(sheet.cell(row,4).value,row+1))
            row = row + 1
            vals = {
                'crossovered_budget_id' : budget_id.id,
                'general_budget_id': general_budget_id.id,
                'analytic_account_id': analytic_account_id.id, 
                'date_from': date_from,
                'date_to' : date_to,
                'planned_amount': planned_amount,
                }
            self.env['account.analytic.crossovered.budget.lines'].create(vals)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: 