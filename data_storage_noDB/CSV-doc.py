'''
CSV文件以纯文本的方式存表格数据，由任意数目的记录组成，记录之间用换行符隔开；每条记录由字段组成，字段之间用其他字符或字符串隔开，
常见的有逗号和制表符，通常所有记录都有相同的字段序列，示例
ID,UserName,Password,age,country
1001,"qiye","qiye_pass",24,"China"
1002,"Mary","Mary_pass",20,"USA"
1003,"Jack","Jack_pass",20,"USA"
'''

# ---> 写入
import csv
headers = ['ID', 'UserName', 'Password', 'Age', 'Country']
rows = [
    (1001, 'qiye', 'qiye_pass', 24, 'China'),
    (1002, 'Mary', 'Mary_pass', 20, 'USA'),
    (1003, 'Jack', 'Jack_pass', 20, 'USA')
]

with open('testCSV.csv', 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)     # 写一条记录，即一行
    f_csv.writerows(rows)       # 写多条记录

# 可以将字典当作参数
rows = [
    {'ID': 1001, 'UserName': 'qiye', 'Password': 'qiye_pass', 'Age': 24, 'Country': 'China'},
    {'ID': 1002, 'UserName': 'Mary', 'Password': 'Mary_pass', 'Country': 'USA', 'Age': 20}
]

with open('testCSV.csv', 'w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)


# ---> 读取
with open(r'./testCSV.csv', 'r') as f:
    f_csv = csv.reader(f)
    headers = next(f_csv)       # 读取头部信息
    print(headers)
    for row in f_csv:
        print(row)
# 上面代码中row是一个元组，可以使用row[0]来访问ID，row[3]来访问Age，但是会引起混淆，因此使用命名元组
from collections import namedtuple
import csv
with open('./testCSV.csv', 'r') as f:
    f_csv = csv.reader(f)               # f_csv是一个tuple组成的list
    headings = next(f_csv)
    Row = namedtuple('Row', headings)   # namedtuple的第一个参数'Row'是新元组的名字，作用不大
    for r in f_csv:
        row = Row(*r)
        print(row.UserName, row.Password)
        print(row)

# 也可以使用读取到字典的方式
with open('./testCSV.csv', 'r') as f:
    f_csv = csv.DictReader(f)       # f_csv是一个字典组成的list
    for row in f_csv:
        print(row.get('UserName'), row.get('Password'))
        print(row)