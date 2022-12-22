import json
import pymysql

sqlinfo = open("secret/mysql.json", "r")
sqlcon = json.load(sqlinfo)

testcheck="main"
server_type=""
pwd_type=""
print(f"testcheck : {testcheck}")
if testcheck == "test":
    testmode = True
    server_type="test_server"
    pwd_type="test_password"

elif testcheck == "main":
    testmode = False
    server_type="main_server"
    pwd_type="main_password"
else:
    mode_error = open("errorinfo.txt", "w")
    mode_error.write("bootmode.txt의 내용이 'main'이거나 'test'가 아님")
    mode_error.close()

database = pymysql.connect(
    user=sqlcon["user"],
    host=sqlcon[server_type],
    database=sqlcon["db"],
    password=sqlcon[pwd_type],
    charset=sqlcon["charset"],
    autocommit=True,
)


cur = database.cursor()

sql=f"select * from log where command='베팅'"
cur.execute(sql)
result=cur.fetchall()

totaldata=[[0,0],[0,0],[0,0],[0,0]]

for data in result:
    d=data[5]
    if d.startswith("모드 1"):
        if d.endswith("실패함"):
            totaldata[0][1]+=1
        else:
            totaldata[0][0]+=1
    elif d.startswith("모드 2"):
        if d.endswith("실패함"):
            totaldata[1][1]+=1
        else:
            totaldata[1][0]+=1
    elif d.startswith("모드 3"):
        if d.endswith("실패함"):
            totaldata[2][1]+=1
        else:
            totaldata[2][0]+=1
    elif d.startswith("모드 7"):
        if d.endswith("실패함"):
            totaldata[3][1]+=1
        else:
            totaldata[3][0]+=1

print(totaldata)

success=[]

for d in totaldata:
    success.append(d[0]/(d[0]+d[1])*100)

print(success)