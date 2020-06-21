
import xlrd
import xlwt
import xlutils.copy
path = 'D://蘑菇租房.xlsx'
line = 7
data = xlrd.open_workbook(path)
ws = xlutils.copy.copy(data)
table=ws.get_sheet(0)
table.write(0,line,'区域')
data1 = xlrd.open_workbook(path)
table1 = data1.sheets()[0]
nrows = table1.nrows
cols = table1.col_values(0)
print(nrows)
print(len(cols))
print('开始写入')
for i in range(nrows):
    if(i == 0):
        continue
    title = cols[i]
    value = title[:title.index('-')]
    table.write(i,line,value)
ws.save(path)