import MysqlDB


mydb = DB.DB('app','123','192.168.1.174','userdb')


uname = mydb.validateUsernameAvailable('atormanen')
print(uname)
