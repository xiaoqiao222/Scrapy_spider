#coding:utf8
import json
import redis
import MySQLdb

def main():
    try:
        rediscli = redis.StrictRedis(host='39.106.34.157',port=6379,db=0)

        mysqlcli = MySQLdb.connect(host='127.0.0.1',user='root',passwd='123456',db='mydb',port=3306,charset='utf8')
        print '链接失白'
    except Exception as e:
        print('数据库连接失败')
        print(str(e))
        exit()

    while True:
        source,data = rediscli.blpop(["truelove:items"])
        # data = data.decode("utf-8")
        item = json.loads(data)

        try:
            cursor = mysqlcli.cursor()
            print('111')
            sql = 'insert ignore into truelove(Nickname,Nameid,Age,Marital_status,Vocation,Height,Education,Constellation,Salay,Location,Origin,Monologue) VALUES("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
            print('222')
            # cursor.execute(sql, (item['url'], item['company'], item['position'], item['salary'], item['location'],item['work_years'], item['degree'], item['position_type'], item['tags'], item['pub_data'],item['position_desc'], item['work_address']))
            cursor.execute(sql, (item['Nickname'], item['Nameid'], item['Age'], item['Marital_status'], item['Vocation'],item['Height'], item['Education'], item['Constellation'], item['Salay'], item['Location'],item['Origin'], item['Monologue']))
            print('333')
            mysqlcli.commit()
            print('ti')
            cursor.close()
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    main()