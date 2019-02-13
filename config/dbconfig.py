#encoding=utf-8
import os

# 获取当前文件所在目录的父目录的绝对路径
parentDirPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#print os.getcwd()
#test = os.path.abspath("dbconfig.py")
#test1 = os.path.abspath(__file__)

# 需要连接的数据库
# beta数据库
host_beta = '10.101.1.124'
user_beta = 'root'
passwd_beta = '68ahfEu~Vs'
db_beta = 'www_qianyilc_com'
port_beta = 3306

#127数据库
host_127 = '10.101.1.127'
user_127 = 'root'
passwd_127 = 's6r(2wSrySoj'
db_127 = 'stpro_qianyilc_com'
port_127 = 3306

#177数据库
host_177 = '10.101.1.177'
user_177 = 'root'
passwd_177 = "Qian1lc"
db_177 = 'stpro_qianyilc_com'
port_177 = 3306

#176数据库
host_176 = '10.101.1.176'
user_176 = 'root'
passwd_176 = "Qian1lc"
db_176 = 'smyt_test_subsidiary'
port_176 = 3306

#私募云通数据库
host_sm = 'db.chfdb.cc'
user_sm = 'jr_test_shsec'
passwd_sm = 'ddeb8a0110d44694a71f7c588e4e4b77617ec5db'
db_sm = 'product'
port_sm = 4119


if __name__ == '__main__':
    print "parentDirPath:", parentDirPath

