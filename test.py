from os import getenv
import psycopg2
from psycopg2.extensions import connection
import time
import csv


def get_connection() -> connection:
    return psycopg2.connect('postgresql://{}:{}@postgresql:5432/{}'.format(getenv("POSTGRES_USER"), getenv("POSTGRES_PASSWORD"), getenv("POSTGRES_USER")))

def select(cur, l:list, num:int) -> list:
    sql = 'SELECT '
    selectCols = []
    for j in range(1, num+1):
        selectCols.append('col' + str(j))
    sql += ','.join(selectCols)
    sql += ' FROM test'
    start_time = time.time()
    cur.execute(sql)
    end_time = time.time()
    
    l.append((end_time - start_time) * 1000)
    return l

def selectJson(cur, l:list, num:int) -> list:
    sql = 'SELECT '
    selectCols = []
    for j in range(1, num+1):
        selectCols.append("col_json->>'key" + str(j) + "'")
    sql += ','.join(selectCols)
    sql += ' FROM test'
    start_time = time.time()
    cur.execute(sql)
    end_time = time.time()
    
    l.append((end_time - start_time) * 1000)
    return l

def selectJsonPath(cur, l:list, num:int) -> list:
    sql = 'SELECT '
    selectCols = []
    if num == 100:
        selectCols.append("""
            jsonb_path_query(col_json, '$.keyvalue() ? (@.key like_regex "^key[1-9]$|^key[1-9][0-9]$|^key100$") .value')
        """)
    elif num == 300:
        selectCols.append("""
            jsonb_path_query(col_json, '$.keyvalue() ? (@.key like_regex "^key[1-9]$|^key[1-9][0-9]$|^key[1-3][0-9][0-9]$") .value')
        """)
    else:
        selectCols.append("""
            jsonb_path_query(col_json, '$.keyvalue() ? (@.key like_regex "^key[1-9]$|^key[1-9][0-9]$|^key[1-5][0-9][0-9]$") .value')
        """)
    sql += ' FROM test'
    start_time = time.time()
    cur.execute(sql)
    end_time = time.time()
    
    l.append((end_time - start_time) * 1000)
    return l

def selectJsonDummy(cur, l:list, num:int) -> list:
    sql = 'SELECT '
    selectCols = []
    for j in range(1, num+1):
        selectCols.append("t.tmp_json->>'key" + str(j) + "'")
    sql += ','.join(selectCols)
    sql +=  'FROM ('\
            'SELECT '\
            "col_json #- '{aaa}' as tmp_json"\
            'FROM test'\
            ') as t'
    start_time = time.time()
    cur.execute(sql)
    end_time = time.time()
    
    l.append((end_time - start_time) * 1000)
    return l


def calclist(l:list) -> list:
    res = []
    res.append(sum(l) / len(l))
    res.append(max(l))
    res.append(min(l))
    return res

list100 = []
list300 = []
list500 = []

listJson100 = []
listJson300 = []
listJson500 = []

listJsonPath100 = []
listJsonPath300 = []
listJsonPath500 = []

listJsonDummy100 = []
listJsonDummy300 = []
listJsonDummy500 = []

with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            list100 = select(cur, list100, 100)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            list300 = select(cur, list300, 300)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            list500 = select(cur, list500, 500)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            listJson100 = selectJson(cur, listJson100, 100)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            listJson300 = selectJson(cur, listJson300, 300)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            listJson500 = selectJson(cur, listJson500, 500)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            listJsonPath100 = selectJsonPath(cur, listJsonPath100, 100)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            listJsonPath300 = selectJsonPath(cur, listJsonPath300, 300)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            listJsonPath500 = selectJsonPath(cur, listJsonPath500, 500)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            listJsonDummy100 = selectJsonPath(cur, listJsonDummy100, 100)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            listJsonDummy300 = selectJsonPath(cur, listJsonDummy300, 300)
with get_connection() as conn:
    with conn.cursor() as cur:
        for i in range(5):
            listJsonDummy500 = selectJsonPath(cur, listJsonDummy500, 500)

with open('result.tsv', mode='a', newline='', encoding='utf-8') as fo:
    csv_writer = csv.writer(fo, delimiter='\t', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['', '平均', '最大', '最小'])
    csv_writer.writerow(['json型カラム以外 100件'] + calclist(list100))
    csv_writer.writerow(['json型カラム以外 300件'] + calclist(list300))
    csv_writer.writerow(['json型カラム以外 500件'] + calclist(list500))
    csv_writer.writerow(['json型カラム 100件'] + calclist(listJson100))
    csv_writer.writerow(['json型カラム 300件'] + calclist(listJson300))
    csv_writer.writerow(['json型カラム 500件'] + calclist(listJson500))
    csv_writer.writerow(['jsonPath 100件'] + calclist(listJsonPath100))
    csv_writer.writerow(['jsonPath 300件'] + calclist(listJsonPath300))
    csv_writer.writerow(['jsonPath 500件'] + calclist(listJsonPath500))
    csv_writer.writerow(['jsonDummy 100件'] + calclist(listJsonDummy100))
    csv_writer.writerow(['jsonDummy 300件'] + calclist(listJsonDummy300))
    csv_writer.writerow(['jsonDummy 500件'] + calclist(listJsonDummy500))
