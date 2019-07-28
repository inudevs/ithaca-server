import xlrd
import json

workbook = xlrd.open_workbook('./high.xls')
worksheet = workbook.sheet_by_index(0)

local = set()
school = set()
for row in range(12, worksheet.nrows):
    local.add(worksheet.cell_value(row, 1))
    school.add(worksheet.cell_value(row, 8))
# print(school, local)

with open('./data.json', 'w') as fp:
    json.dump({
        'school': list(school),
        'local': list(local)
    }, fp, ensure_ascii=False, indent=4)
    fp.write('\n')
