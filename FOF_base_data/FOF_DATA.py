# encoding:utf-8
from util import db_mysql
from config import dbconfig
import pandas as pd
import numpy as np
import time
from numpy import log

class FOF_DATA:
    def __init__(self,fund_id):
        self.fund_id = fund_id #基金id
        #self.fund_data = fund_data #数据日期
        
    #连接数据库
    def conn(self):
        db = db_mysql.db_mysql(dbconfig.host_sm,
                               dbconfig.user_sm,
                               dbconfig.passwd_sm,
                               dbconfig.db_sm,
                               dbconfig.port_sm)
        conn = db.connentDB()
        return conn
    
    #1计算近三个月累计收益率
    def r_i(self):
        sql = "SELECT swanav FROM fund_nv_data_standard WHERE fund_id = '" + self.fund_id + "' ORDER BY statistic_date DESC LIMIT 1,14;"
        result = pd.read_sql(sql,con = self.conn())
        nav_it = result.loc[0,'swanav']
        nav_it1 = result.loc[13,'swanav']
        r_i = (nav_it / nav_it1 -1)
        return r_i
    
    #2计算近三个月年化收益率（以周为计算周期）
    def R_i(self):
        sql = "SELECT swanav FROM fund_nv_data_standard WHERE fund_id = '" + self.fund_id + "' ORDER BY statistic_date DESC LIMIT 1,14;"
        result = pd.read_sql(sql,con = self.conn())
        nav_it = result.loc[0,'swanav']
        nav_it1 = result.loc[13,'swanav']
        R_i = (pow((nav_it / nav_it1),(52.0 / 14.0)) - 1) #pow()用于计算乘方，/  计算除法时，分子分母为小数时计算精确
        return R_i
    
    #3计算近三个月波动率(算出来的数个私募云通给的数有差别1.35%)
    def s_i(self):
        sql = "SELECT swanav FROM fund_nv_data_standard WHERE fund_id = '" + self.fund_id + "' ORDER BY statistic_date DESC LIMIT 1,14;"
        result = pd.read_sql(sql,con = self.conn())
        r_it = [] #基金的周收益序列，算法为：ln（本月复权累计净值/上月复权累计净值），另一个算法为：本月复权累计净值/上月复权累计净值 -1，
        """
        for i in range(len(result) - 1):
            a = log(result.loc[i,'swanav'] / result.loc[i+1,'swanav'])
            r_it.append(a)
        """
        for i in range(len(result) - 1):
            a = result.loc[i,'swanav']/result.loc[i+1,'swanav'] - 1.0
            r_it.append(a)
        del r_it[6]
        T = len(r_it) #基金收益率个数
        r_i = sum(r_it) / T #基金统计区间内平均收益率
        #print r_i
        r_iti = []
        for j in range(len(r_it)):
            b = pow((r_it[j] - r_i),2)
            r_iti.append(b)
        s_i = np.sqrt(sum(r_iti) / (T-1.0))
        return s_i
    
    #4计算近三个月的年化波动率（年化标准差）
    def Ss_i(self):
        Ss_i = self.s_i() * np.sqrt(52)
        return Ss_i
        
    #5计算近三个月的夏普比率
    def SR_i(self):
        R_i = self.R_i() #基金在统计区间内的年化收益率
        S_i = self.Ss_i() #基金在统计区间内的年化波动率
        sql = "select y1_treasury_rate as rate from market_index where statistic_date between '2017-08-01' and '2017-11-30' and y1_treasury_rate is not null;"
        result = pd.read_sql(sql,con = self.conn())
        #print result['rate']
        a = pd.DataFrame.mean(result) #dataframe每列的平均值
        R_f = a.loc['rate'] / 100 #统计区间内的无风险年化收益率
        SR_i = (R_i - R_f)/ S_i
        return SR_i
    
    #6计算近三个月的下行风险（年化下行标准差）
    def DD_i(self):
        sql = "SELECT swanav FROM fund_nv_data_standard WHERE fund_id = '" + self.fund_id + "' ORDER BY statistic_date DESC LIMIT 1,14;"
        result = pd.read_sql(sql,con = self.conn())
        r_it = [] #基金的周收益序列，算法为：ln（本月复权累计净值/上月复权累计净值）
        for i in range(len(result) - 1):
            a = result.loc[i,'swanav']/result.loc[i+1,'swanav'] - 1.0
            r_it.append(a)
        del r_it[6]
        T = len(r_it)
        sql_rate = "select statistic_date, y1_treasury_rate as rate from market_index where statistic_date between '2017-08-01' and '2017-11-30' and y1_treasury_rate is not null;"
        #result_rate = pd.read_sql(sql_rate,con = self.conn())
        #print result_rate
        a = (pow((1.0 + 0.0354),(1.0/365.0))-1)*365.0/52.0
        b = (pow((1.0 + 0.034889),(1.0/365.0))-1)*365.0/52.0
        c = (pow((1.0 + 0.034753),(1.0/365.0))-1)*365.0/52.0
        d = (pow((1.0 + 0.0333),(1.0/365.0))-1)*365.0/52.0
        abcd_list = [a,a,a,b,b,b,c,c,c,d,d,d]
        #print abcd_list
        g = []
        for i in range(len(r_it)):
            e = min(0,(r_it[i]-abcd_list[i]))
            f = pow(e, 2)
            g.append(f)
        q = sum(g)
        h = np.sqrt(q / (T - 1))
        k = np.sqrt(52.0)
        DD_i = h*k
        return DD_i
    
    #7计算近三个月的年化索提诺比率
    def SortinoR(self):
        R_i = self.R_i()  #基金在统计区间内的年化收益率
        sql = "select y1_treasury_rate as rate from market_index where statistic_date between '2017-08-01' and '2017-11-30' and y1_treasury_rate is not null;"
        result = pd.read_sql(sql,con = self.conn())
        #print result['rate']
        a = pd.DataFrame.mean(result) #dataframe每列的平均值
        R_f = a.loc['rate'] / 100 #统计区间内的无风险年化收益率
        SortinoR = (R_i - R_f)/self.DD_i()
        return SortinoR

    #8计算近三个月最大回撤率
    def Mdd(self):
        sql = "SELECT nav FROM fund_nv_data_standard WHERE fund_id = '" + self.fund_id + "' ORDER BY statistic_date DESC LIMIT 1,14;"
        result = pd.read_sql(sql, con = self.conn())
        Mdd_list = []
        for i in range(len(result)):
            nav_is_list = result[i:len(result)]
            nav_is_list_np = np.array(nav_is_list)
            nav_is_max = max(nav_is_list_np.tolist())
            Mdd = ((nav_is_max - result.loc[i,'nav'])/nav_is_max)
            Mdd_list.append(Mdd)
        return max(Mdd_list)[0]
    

    #9计算近三个月卡玛比率
    def Cr(self):
        R_i = self.R_i()  #基金在统计区间内的年化收益率
        sql = "select y1_treasury_rate as rate from market_index where statistic_date between '2017-08-01' and '2017-11-30' and y1_treasury_rate is not null;"
        result = pd.read_sql(sql,con = self.conn())
        #print result['rate']
        a = pd.DataFrame.mean(result) #dataframe每列的平均值
        R_f = a.loc['rate'] / 100 #统计区间内的无风险年化收益率
        Cr = (R_i - R_f)/self.Mdd()
        return Cr
    
    #10计算近三个月的年化跟踪误差
    def TE(self):
        sql = "SELECT swanav FROM fund_nv_data_standard WHERE fund_id = '" + self.fund_id + "' ORDER BY statistic_date DESC LIMIT 1,14;"
        result = pd.read_sql(sql,con = self.conn())
        r_it = [] #基金的周收益序列，算法为：ln（本月复权累计净值/上月复权累计净值）
        for i in range(len(result) - 1):
            a = result.loc[i,'swanav']/result.loc[i+1,'swanav'] - 1.0
            r_it.append(a)
        del r_it[6]
        T = len(r_it)
        sql_mt = "SELECT m.hs300 as hs300 FROM market_index m LEFT JOIN  fund_nv_data_standard f ON m.statistic_date = f.statistic_date \
                WHERE f.fund_id = '" + self.fund_id + "' AND  f.statistic_date BETWEEN '2017-08-18' AND '2017-11-24' ORDER BY m.`statistic_date` DESC;"
        result_mt = pd.read_sql(sql_mt,con = self.conn())
        #print result_mt
        r_mt = []
        for j in range(len(result_mt)-1):
            b = result_mt.loc[j,'hs300'] / result_mt.loc[j+1,'hs300'] -1
            r_mt.append(b)
        #print r_mt
        #print result_mt
        del r_mt[6]
        c = []
        for k in range(len(r_mt)):
            d = r_it[k]-r_mt[k]
            c.append(d)
        r_it_mt_aver = sum(c)/len(r_mt) #基准的周收益率序列
        h = []
        for g in range(len(r_mt)):
            e = pow((r_it[g] - r_mt[g] - r_it_mt_aver),2)
            h.append(e)
        q = sum(h)
        w = np.sqrt(52)
        u = np.sqrt(q/(len(r_mt)-1))
        TE = w*u            
        return TE
    
    #11计算近三个月的信息比率
    def IR(self):
        R_i = self.R_i()  #基金在统计区间内的年化收益率
        sql_mt = "SELECT m.hs300 as hs300 FROM market_index m LEFT JOIN  fund_nv_data_standard f ON m.statistic_date = f.statistic_date \
        WHERE f.fund_id = '" + self.fund_id + "' AND  f.statistic_date BETWEEN '2017-08-18' AND '2017-11-24' ORDER BY m.`statistic_date` DESC;"
        result_mt = pd.read_sql(sql_mt,con = self.conn())
        #print result_mt
        nav_it = result_mt.loc[0,'hs300']
        nav_it1 = result_mt.loc[13,'hs300']
        R_m = (pow((nav_it / nav_it1),(52.0 / 14.0)) - 1) #pow()用于计算乘方，/  计算除法时，分子分母为小数时计算精确
        IR = (R_i - R_m)/self.TE()
        #print 'ss',R_i
        #print 'dd',R_m
        return IR
    
    #12-1计算近三个月年化詹森指数α
    def alpha(self):
        pass
    
    #12-2计算近三个月贝塔系数β
    def beta(self):
        pass
     
    #12-3计算近三个月非系统性风险δ
    def deerta(self):
        pass   
    
    #13计算近三个月特雷诺比率
    def TR(self):
        pass
    
    #14     


"""
    #近三个月的年化跟踪误差
    def Tes(self):
        print log(1.393/1.379) #计算log
        print np.sqrt(52) #开平方根
        print sum([1,2,3]) #求和
        #pow(x,y)用于计算乘方
        pass
"""

        
if __name__ == '__main__':
    test = FOF_DATA('JR000001')
    
    print '1近三个月累计收益率为：===================',
    print test.r_i()
    
    print '2近三个月年化收益率为（计算周期为周）：==================',
    print test.R_i()
    
    print '3近三个月波动率为：====================',
    print '私募云通给的数是1.35%---:',
    print test.s_i()
    
    print '4近三个月年化波动率为：==================',
    print test.Ss_i()
    
    print '5近三个月年化夏普率为：================',
    print test.SR_i()
    
    print '6近三个月下行风险为：===================',
    print test.DD_i()
    
    print '7近三个月年化索提诺比率为：====================',
    print test.SortinoR()
    
    print '8近三个月最大回撤率为：===================',
    print test.Mdd()
    
    print '9近三个月卡玛比率为：==============',
    print test.Cr()
    
    print '10近三个月年化跟踪误差为：==============',
    print test.TE()
    
    print '11近三个月年化信息比率为:=============',
    print test.IR()

    
        