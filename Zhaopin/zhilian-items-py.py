#coding:utf8
import json
import redis
import MySQLdb

def main():
    try:
        rediscli = redis.StrictRedis(host='39.106.37.83',port=6379,db=0)
        mysqlcli = MySQLdb.connect(host='39.108.153.55',user='root',passwd='root',db='spider',port=3306,charset='utf8')
    except Exception as e:
        print('数据库连接失败')
        print(str(e))
        exit()

    while True:
        source,data = rediscli.blpop(["zhilian:items"])
        # data = data.decode("utf-8")
        item = json.loads(data)

        try:
            cursor = mysqlcli.cursor()
            print('111')
            sql = 'insert ignore into lagou(url,company,position,salary,location,work_years,degree,position_type,tags,pub_date,position_desc,work_address) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
            print('222')
            # cursor.execute(sql, (item['url'], item['company'], item['position'], item['salary'], item['location'],item['work_years'], item['degree'], item['position_type'], item['tags'], item['pub_data'],item['position_desc'], item['work_address']))
            cursor.execute(sql, (item['url'], item['company'], item['position'], item['salary'], item['location'],item['work_years'], item['degree'], item['position_type'], item['tags'], item['pub_data'],item['position_desc'], item['work_address']))
            print('333')
            mysqlcli.commit()
            print('ti')
            cursor.close()
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    main()