# encoding:utf-8
import MySQLdb
import logger

class db_mysql(object):
    '''
    mysql数据库相关类
    '''
    # 游标#
    cur = ""
    # 数据库连接#
    conn = ""
    # 查询或者影响的行数#
    result_line = 0

    def __init__(self, host, user, passwd, db, port):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port

    def connentDB(self):
        '''
         预置条件：对象实例化
         函数功能：连接数据库
         参    数：无
         返回值：无
        '''

        self.conn = MySQLdb.connect(host=self.host, 
                                    user=self.user, 
                                    passwd=self.passwd, 
                                    db=self.db, 
                                    port=self.port,
                                    charset="utf8")
        self.cur = self.conn.cursor()
        logger.info(u"数据库连接成功")
        return self.conn

    def executeSQL(self, sql, param=None):
        '''
         预置条件：数据库连接成功
         函数功能：执行增删改相关操作
         参    数：param-参数，列表型
         返回值：无
        '''
        logger.info(u'即将执行的SQL操作语句：' + sql)
        if param is not None:
            count = 1
            param = tuple(param)
            print param
            for item in param:
                logger.info(u'参数' + str(count) + u'：' + str(item))
                count += 1
        self.result_line = self.cur.execute(sql, param)
        logger.info(u"影响行数：" + str(self.result_line))

    def executeBatchSql(self, sql):
        '''
         预置条件：数据库连接成功
         函数功能：批量执行增删改相关操作
         参   数：sql-sql语句，列表型，且为完整的sql
         返回值：无
        '''
        logger.info(u'即将批量执行')
        for one in sql:
            self.executeSQL(one)
            self.commit()

    def getResultLine(self):
        '''
         预置条件：执行完查询或者操作语句
         函数功能：获取结果行数
         参   数：无
         返回值：查询结果行数
        '''
        return self.result_line

    def querySQL(self, sql, param=None):
        '''
         预置条件：数据库连接成功
         函数功能：执行查询操作
         参   数：param-参数，列表型
         返回值：查询结果集，如果为空，返回None
        '''
        logger.info(u'执行的SQL查询语句是：' + sql)
        if param is not None:
            count = 1
            param = tuple(param)
            for item in param:
                logger.info(u'查询参数' + str(count) + u'：' + item)
                count += 1
        self.cur.execute(sql, param)
        result = self.cur.fetchall()
        # print result
        if result == ():
            logger.info(u'未查询到相关结果')
            self.result_line = 0
            return None
        self.result_line = len(result)
        logger.info(u"查询到行数：" + str(len(result)))

        return result

    def commit(self):
        '''
         预置条件：执行完数据库增删改操作
         函数功能：提交
         参    数：无
         返回值：无
        '''
        logger.info(u'数据库提交')
        self.conn.commit()

    def curClose(self):
        '''
        预置条件：数据库已经连接
        函数功能：关闭游标
        参   数：无
        返回值：无
        '''
        logger.info(u'关闭游标')
        self.cur.close()
        self.cur = ""

    def connClose(self):
        '''
         预置条件：数据库已经连接
         函数功能：断开连接
         参    数：无
         返回值：无
        '''
        logger.info(u'断开连接')
        self.conn.close()
        self.conn = ""

if __name__=="__main__":
    # db = DataBaseManager('10.101.1.118','root','O{wYim26yg','www_qianyilc_com',3306)
    db = db_mysql('10.101.1.177','root','Qian1lc','stpro_qianyilc_com',3306)
    db.connentDB()
    # db.executeSQL('INSERT INTO city(city,post_id) values(%s,%d)',['shenzhen1',300002])
    db.executeSQL("insert into lc_risk_day_record (day, create_time, update_time, risk_level, pro_id, pro_type, index1_min, index2_min, index3_min, index4_min, index5_min, index6_min, index7_min, index8_min, index9_min, index10_min, index1_max, index2_max, index3_max, index4_max, index5_max, index6_max, index7_max, index8_max, index9_max, index10_max, value1, value2, value3, value4, value5, value6, value7, value8, value9, value10, exception_field) values('2017-09-02','0','0','3','48','0','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00','0.00',NULL);")
    # db.executeSQL("UPDATE city SET post_id=%s WHERE city=%s",[100000,'beijing'])
    # db.executeSQL("delete from city WHERE city=%s",['beijing'])
    # db.commit()

    # sql = ["INSERT INTO city(city,post_id) values('nanjing1',222223)","INSERT INTO city(city,post_id) values('chongqing1',33334)"]
    # db.executeBatchSql(sql)
    result = db.querySQL('select * from lc_valuation_item where item_code like "1102%" and pro_id=1')
    print db.getResultLine()
    print result[1][4]
    db.curClose()
    db.connClose()