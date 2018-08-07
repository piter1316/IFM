from openpyxl import load_workbook

wb = load_workbook('IFM Preisliste 2018.xlsx')
print(wb.sheetnames)
sheet = wb['Preisliste 2018']

print(sheet.max_row)

kody = []
for i in range(9,sheet.max_row):
    kody.append(sheet.cell(row=i, column=1).value)
    # print(sheet.cell(row=i, column=1).value)