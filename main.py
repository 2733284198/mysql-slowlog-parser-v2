# encoding:utf-8
import os
import sys
import re
# from config import mysqlconnection as mc

reload(sys)
sys.setdefaultencoding('utf8')

baseDir  = os.path.dirname(os.path.abspath(__file__))
fileName = os.path.join(baseDir, 'data/slow.log')
res = []

# 逐行读取
# with open(fileName, 'r') as f:
#     for line in f:
#         print(line.rstrip())

# 全部读取
with open(fileName, 'r') as f:
    log = f.read().decode('utf-8')

    '''
    # Time: 2017-01-20T09:33:18.704450+08:00
    # User@Host: test_user_db[test_user_db] @  [192.168.137.111]  Id: 137686
    # Query_time: 1.782185  Lock_time: 0.000094 Rows_sent: 22459  Rows_examined: 22459
    SET timestamp=1484875998;
    SELECT * FROM dbname.tbl1;
    '''

    pat = ''.join([
            r'#\s+Time:\s+(.*?)\s+',
            r'#\s+User@Host:\s+(.*?)\[(.*?)\]\s+@\s+\[(.*?)\]\s+Id:\s+(.*?)\s+',
            r'#\s+Query_time:\s+(.*?)\s+Lock_time:\s+(.*?)\s+Rows_sent:\s+(.*?)\s+Rows_examined:\s+(.*?)\s+',
            r'SET timestamp=(.*?)\s+',
            r'(.*)'
        ])
    # pat = r'#\s+Time:\s+(.*?)\s+#\s+User@Host:\s+(.*?)\[(.*?)\]\s+@\s+\[(.*?)\]\s+Id:\s+(.*?)\s+#\s+Query_time:\s+(.*?)\s+Lock_time:\s+(.*?)\s+Rows_sent:\s+(.*?)\s+Rows_examined:\s+(.*?)\s+SET timestamp=(.*?)\s+(.*)'
    # print(pat)
    
    # 将正则表达式编译成Pattern对象
    pattern = re.compile(pat)
    # 使用Pattern匹配文本，获得匹配结果，无法匹配时将返回None
    matched = pattern.findall(log)

    '''
+----------------+---------------------+------+-----+-------------------+-----------------------------+
| Field          | Type                | Null | Key | Default           | Extra                       |
+----------------+---------------------+------+-----+-------------------+-----------------------------+
| start_time     | timestamp           | NO   |     | CURRENT_TIMESTAMP | on update CURRENT_TIMESTAMP |
| query_time     | time                | NO   |     | NULL              |                             |
| lock_time      | time                | NO   |     | NULL              |                             |
| rows_sent      | int(11)             | NO   |     | NULL              |                             |
| sql_text       | mediumtext          | NO   |     | NULL              |                             |
| user_host      | mediumtext          | NO   |     | NULL              |                             |
| db             | varchar(512)        | NO   |     | NULL              |                             |
| rows_examined  | int(11)             | NO   |     | NULL              |                             |
| thread_id      | bigint(21) unsigned | NO   |     | NULL              |                             |
+----------------+---------------------+------+-----+-------------------+-----------------------------+
    '''


    if matched:
        for item in matched:
            res.append({
                'query_time': item[5],
                'lock_time' : item[6],
                'rows_sent' : item[7],
                'start_time': item[9],
                'sql_text'  : item[10],
                'user_host' : '',
                'db'        : '',
            })

print(res)