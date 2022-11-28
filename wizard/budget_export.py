# -*- coding: utf-8 -*-

from datetime import date, timedelta
import xlwt
import io
import base64
import datetime
import datetime, calendar
import time
from openerp import models, fields, api, _
from openerp.http import request
from dateutil.relativedelta import relativedelta


class ExportBudgetSheet(models.TransientModel):
    _name = 'export.budget.sheet.wizard'

    # @api.multi
    def print_budget_sheet_excel(self):
        active_id = self._context.get('active_id')
        budget_id = self.env['budget.budget'].browse(active_id)
        workbook = xlwt.Workbook()
        title_style_comp = xlwt.easyxf('align: horiz center ; font: name Times New Roman,bold off, italic off, height 450')
        title_style_comp_left = xlwt.easyxf('align: horiz left ; font: name Times New Roman,bold off, italic off, height 450')
        title_style = xlwt.easyxf('align: horiz center ;font: name Times New Roman,bold off, italic off, height 350')
        title_style2 = xlwt.easyxf('font: name Times New Roman, height 200')
        title_style1 = xlwt.easyxf('font: name Times New Roman,bold off, italic off, height 190; borders: top double, bottom double, left double, right double;')
        title_style1_table_head = xlwt.easyxf('font: name Times New Roman,bold on, italic off, height 200; borders: top double, bottom double, left double, right double;')
        title_style1_table_head1 = xlwt.easyxf('font: name Times New Roman,bold on, italic off, height 200')
        title_style1_consultant = xlwt.easyxf('font: name Times New Roman,bold on, italic off, height 200; borders: top double, bottom double, left double, right double;')
        title_style1_table_head_center = xlwt.easyxf('align: horiz center ; font: name Times New Roman,bold on, italic off, height 190; borders: top thick, bottom thick, left thick, right thick;')

        title_style1_table_data = xlwt.easyxf('align: horiz right ;font: name Times New Roman,bold on, italic off, height 190')
        title_style1_table_data_sub = xlwt.easyxf('font: name Times New Roman,bold off, italic off, height 190')
        title_style1_table_data_sub_amount = xlwt.easyxf('align: horiz right ;font: name Times New Roman,bold off, italic off, height 190')
        title_style1_table_data_sub_balance = xlwt.easyxf('align: horiz right ;font: name Times New Roman,bold off, italic off, height 190')
        sheet_name = 'Budget Sheet'
        sheet = workbook.add_sheet(sheet_name)
        
        name = budget_id.name
        sheet.write_merge(0, 1, 0, 6, name, title_style_comp_left)

        user_id = budget_id.create_uid
        date_start = budget_id.date_from
        date_end = budget_id.date_to
        comp_id = budget_id.company_id
        currency_id = budget_id.company_id.currency_id
        sheet.write(3, 0, 'Responsible',title_style1_table_head1)
        sheet.write(4, 0, user_id.name, title_style1_table_data_sub)
        sheet.write(3, 1, 'Date From',title_style1_table_head1)
        sheet.write(4, 1, date_start.strftime('%m/%d/%Y'), title_style1_table_data_sub)
        sheet.write(3, 2, 'Date To',title_style1_table_head1)
        sheet.write(4, 2, date_end.strftime('%m/%d/%Y'), title_style1_table_data_sub)
        sheet.write(3, 3, 'Company',title_style1_table_head1)
        sheet.write(4, 3, comp_id.name, title_style1_table_data_sub)
        sheet.write(3, 4, 'Currency',title_style1_table_head1)
        sheet.write(4, 4, currency_id.name, title_style1_table_data_sub)

        
        sheet.write(8, 0, 'Budgetary Position',title_style1_table_head)
        sheet.write(8, 1, 'Analytic Account',title_style1_table_head)
        sheet.write(8, 2, 'Start Date',title_style1_table_head)
        sheet.write(8, 3, 'End Date',title_style1_table_head)
        sheet.write(8, 4, 'Paid Date',title_style1_table_head)
        sheet.write(8, 5, 'Budgeted Amount',title_style1_table_head)
        sheet.write(8, 6, 'Released Amount',title_style1_table_head)
        sheet.write(8, 7, 'Actual Amount',title_style1_table_head)
        sheet.write(8, 8, 'Achievement',title_style1_table_head)
        
        roww = 9
       
        budget_lines = budget_id.mapped("crossovered_budget_line")
        row_data = roww+1
        for line in budget_lines:
            column = sheet.col(0)
            column.width = 210 * 25
            sheet.write(row_data, 0, line.general_budget_id.name, title_style1_table_data_sub)
            column = sheet.col(1)
            column.width = 210 * 25
            sheet.write(row_data, 1, line.analytic_account_id.name, title_style1_table_data_sub)
            sheet.write(row_data, 2, line.date_from.strftime('%m/%d/%Y'), title_style1_table_data_sub)
            sheet.write(row_data, 3, line.date_to.strftime('%m/%d/%Y'), title_style1_table_data_sub)
            if line.paid_date:
                sheet.write(row_data, 4, line.paid_date.strftime('%m/%d/%Y'), title_style1_table_data_sub)
            else :
                sheet.write(row_data, 4, '', title_style1_table_data_sub)
            column = sheet.col(5)
            column.width = 200 * 25
            sheet.write(row_data, 5, currency_id.symbol+str(line.planned_amount) , title_style1_table_data_sub)
            column = sheet.col(6)
            column.width = 200 * 25
            sheet.write(row_data, 6, currency_id.symbol+str(line.released_amount), title_style1_table_data_sub)
            column = sheet.col(7)
            column.width = 200 * 25
            sheet.write(row_data, 7, currency_id.symbol+str(line.actual_amount), title_style1_table_data_sub)
            column = sheet.col(8)
            column.width = 200 * 25
            sheet.write(row_data, 8, str(line.percentage)+'%', title_style1_table_data_sub)

            row_data = row_data + 1
        roww = row_data + 3
            
        stream = io.BytesIO()
        workbook.save(stream)
        attach_id = self.env['budget.report.output.excel'].create({
            'name':'Budget_sheet.xls',
            'xls_output': base64.encodestring(stream.getvalue())
        })
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'budget.report.output.excel',
            'res_id':attach_id.id,
            'type': 'ir.actions.act_window',
            'target':'new'
        }
       
            
class BudgetReportOutputExcel(models.TransientModel):
    _name = 'budget.report.output.excel'
    _description = 'Wizard to store the Excel output'

    xls_output = fields.Binary(
       string='Excel Output',
       readonly=True
    )
    name = fields.Char(
        string='File Name',
        help='Save report as .xls format',
    )

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: 