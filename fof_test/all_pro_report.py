#encoding=utf-8
from util import db_mysql
from config import dbconfig
import pandas as pd
from util import logger

pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
#pd.set_option('display.max_rows',500)
#pd.set_option('display.max_columns',500)

#此脚本用于查询总产品股票、基金、债券的日报数据
class all_pro_report():
    date = ''
    
    def __init__(self,date):
        self.date = date
    
    #连接数据库
    def conn(self):
        db = db_mysql.db_mysql(dbconfig.host_177,
                               dbconfig.user_177,
                               dbconfig.passwd_177,
                               dbconfig.db_177,
                               dbconfig.port_177)
        conn = db.connentDB()
        return conn
    
    #获取某日全部产品的市值和
    def pro_value_all(self):
        sql = "SELECT SUM(s.total_market_value) as value_all FROM lc_valuation_stats s LEFT JOIN \
        lc_valuation_file f ON s.valuation_id = f.valuation_id LEFT JOIN lc_pro p ON s.pro_code = \
        p.code WHERE s.item_code = 'asset_net_value' AND s.date = '"+ self.date +"' AND p.type < 4 \
        AND f.is_valid = 1 AND f.status = 1;"
        logger.info('即将执行的sql语句：'+ sql)
        value_all = pd.read_sql(sql, con = self.conn())
        return value_all.loc[0]['value_all']
        
    #《报告期末持仓市值前10的股票投资明细》   
    def pro_stock_all(self):
        stock_sql = "SELECT RIGHT(i.item_code,6) AS code,ss.stockname AS name,i.total_market_value,\
        i.amount,i.unit_market_value AS price FROM lc_valuation_item i LEFT JOIN lc_valuation_file f \
        ON i.valuation_id = f.valuation_id LEFT JOIN lc_wd_stock ss ON RIGHT(i.item_code,6) = ss.stocknum \
        WHERE i.item_code LIKE '1102%' AND LENGTH(i.item_code)>8 AND i.date='"+ self.date +"' AND \
        f.is_valid = 1 AND f.status = 1 AND i.pro_code IN (SELECT CODE FROM lc_pro WHERE TYPE < 4);"
        logger.info("即将执行的sql语句：" + stock_sql)
        result = pd.read_sql(stock_sql, con = self.conn())
        result1 = result.groupby('code',as_index = False)['total_market_value'].sum()
        result2 = result.groupby('code',as_index = False)['amount'].sum()
        result3 = result1.merge(result2,on = 'code') #按照code合并两个dataframe
        result3 = pd.merge(result3,result,on = 'code')
        result4 = result3.drop_duplicates('code')#去除重复的code行
        del result4['total_market_value_y']
        del result4['amount_y'] 
        result5 = result4.sort_values('total_market_value_x',0, ascending=False)
        result6 = result5.to_dict(orient = 'records')
        result7 = pd.DataFrame(result6)
        for i in range(len(result7)):
            result7.loc[i,'percent'] = int(result7.loc[i,'total_market_value_x']/self.pro_value_all()*10000)
            result7.loc[i,'percent'] = result7.loc[i,'percent']/100
        result7.rename(columns={'total_market_value_x': 'market_value', 'amount_x': 'hold'}, inplace=True)
        return result7
    
    #《报告期末持仓市前10的基金投资明细》
    def pro_fund_all(self):
        fund_sql = "SELECT RIGHT(i.item_code,6) as code,i.item_name,i.amount,i.unit_cost,i.unit_market_value,\
        i.total_market_value FROM lc_valuation_item i LEFT JOIN lc_valuation_file f ON i.`valuation_id` \
        = f.`valuation_id` WHERE (i.item_code LIKE '1105%' OR i.item_code LIKE '1116%') AND \
        LENGTH(i.item_code)>8 AND i.DATE='"+ self.date +"' AND f.is_valid = 1 AND f.status = 1 AND \
        i.pro_code IN (SELECT CODE FROM lc_pro WHERE TYPE < 4);"
        logger.info("即将执行的sql语句：" + fund_sql)
        result = pd.read_sql(fund_sql, con = self.conn())
        result1 = result.groupby('code',as_index = False)['total_market_value'].sum()
        result2 = result.groupby('code',as_index = False)['amount'].sum()
        result3 = pd.merge(result1,result2,on = 'code')
        result3 = pd.merge(result3,result,on = 'code')
        result4 = result3.drop_duplicates('code')
        del result4['amount_y']
        del result4['total_market_value_y']
        result5 = result4.sort_values('total_market_value_x',0, ascending=False)
        result6 = result5.to_dict(orient = 'records')
        result7 = pd.DataFrame(result6)
        for i in range(len(result7)):
            result7.loc[i,'percent'] = int(result7.loc[i,'total_market_value_x']/self.pro_value_all()*10000)
            result7.loc[i,'percent'] = result7.loc[i,'percent']/100
        result7.rename(columns={'total_market_value_x': 'market_value', 'amount_x': 'units','item_name':'name',
                                'unit_cost':'start_value','unit_market_value':'current_value'}, inplace=True)
        return result7
    
    #《 报告期末按公允价值占集合计划资产净值比例大小排名的前五名债券投资》
    def pro_bond_all(self):
        bond_sql = "SELECT b.bond_code,i.item_name,b.wd_hy_cate1,b.zx_zxpj,i.amount,i.total_market_value \
        FROM lc_wd_bond b LEFT JOIN lc_valuation_item i ON b.bond_intro = i.item_name left join \
        lc_valuation_file f on f.valuation_id = i.valuation_id WHERE i.item_code LIKE '1103%' AND \
        (LENGTH(i.item_code)=14 OR LENGTH(i.item_code)=17) AND i.date ='"+ self.date +"' and \
        f.is_valid = 1 and f.status = 1 AND i.pro_code IN (SELECT CODE FROM lc_pro WHERE TYPE < 4);"
        logger.info("即将执行的sql语句：" + bond_sql)
        result = pd.read_sql(bond_sql, con = self.conn())
        result1 = result.groupby('bond_code',as_index = False)['amount'].sum()
        result2 = result.groupby('bond_code',as_index = False)['total_market_value'].sum()
        result3 = pd.merge(result1,result2,on = 'bond_code')
        result3 = pd.merge(result3,result,on = 'bond_code')
        del result3['amount_y']
        result4 = result3.drop_duplicates('bond_code')
        result5 = result4.sort_values('total_market_value_x',0, ascending=False)
        result6 = result5.to_dict(orient = 'records')
        result7 = pd.DataFrame(result6)
        for i in range(len(result7)):
            result7.loc[i,'percent'] = int(result7.loc[i,'total_market_value_x']/self.pro_value_all()*10000)
            result7.loc[i,'percent'] = result7.loc[i,'percent']/100
        result7.rename(columns={'bond_code': 'code', 'item_name': 'name','item_name':'name','total_market_value_y':'market_value',
                                'zx_zxpj':'credit','wd_hy_cate1':'cate','total_market_value_x':'fair_value','amount_x':'amount'}, inplace=True)        
        return result7
    
    #《报告期末按按合约价值占集合计划资产净值比例大小排名的前五名商品期货投资》
    def pro_goods_all(self):
        goods_sql = "select i.total_market_value,c.name,ABS(i.total_market_value) AS ABS\
        from lc_valuation_item i left join lc_valuation_file f on i.valuation_id = f.valuation_id \
        left join lc_wd_goods_cate c on SUBSTR(i.item_code,9,2) = c.code where i.item_code like \
        '3102%' and length(i.item_code)>8 and SUBSTring(i.item_code,7,2)='01' AND i.pro_code IN \
        (SELECT CODE FROM lc_pro WHERE TYPE < 4) and f.status=1 AND f.is_valid=1 and i.date = \
        '"+ self.date +"';"
        logger.info("即将执行的sql语句：" + goods_sql)
        result = pd.read_sql(goods_sql,con = self.conn())
        result_poor = result.groupby('name',as_index = False)['total_market_value'].sum()#轧差数据
        result_tvalue = result.groupby('name',as_index = False)['ABS'].sum()#合约价值数据
        for i in range(len(result_tvalue)):
            result_tvalue.loc[i,'percent'] = result_tvalue.loc[i,'ABS']/self.pro_value_all()*100
            result_tvalue.loc[i,'percent'] = round(result_tvalue.loc[i,'percent'],2)
        for i in range(len(result)):
            if result.loc[i,'total_market_value']>0:
                result.loc[i,'long'] = result.loc[i,'total_market_value']
                result.loc[i,'bear'] = 0
            else:
                result.loc[i,'long'] = 0
                result.loc[i,'bear'] = result.loc[i,'total_market_value']
        result_long = result.groupby('name',as_index = False)['long'].sum()
        result_bear = result.groupby('name',as_index = False)['bear'].sum()
        result_bear['long'] = result_long['long']
        result_bear['percent'] = result_tvalue['percent']
        result_bear['tvalue'] = result_tvalue['ABS']
        result_bear['poor'] = result_poor['total_market_value']
        #goods_report = result_bear.sort_values('total_market_value_x',0, ascending=False)
        return result_bear
    
    
    #《报告期末按行业分类股票投资组合》
    def pro_stockHY_all(self):
        stockHY_sql = "SELECT s.wd_trade_pname,i.total_market_value \
        FROM lc_wd_stock s LEFT JOIN lc_valuation_item i ON s.stocknum = RIGHT(i.item_code,6) \
        LEFT JOIN lc_valuation_file f ON f.valuation_id = i.valuation_id WHERE \
        LENGTH(i.item_code)>8 AND i.item_code LIKE '1102%' AND i.date = '"+ self.date +"' \
        AND f.is_valid = 1 AND f.status = 1 AND i.pro_code IN \
        ( SELECT CODE FROM lc_pro WHERE TYPE < 4);"
        logger.info("即将执行的sql语句：" + stockHY_sql)
        result = pd.read_sql(stockHY_sql,con = self.conn())
        result1 = result.groupby('wd_trade_pname',as_index = False)['total_market_value'].sum()
        result2 = result1.sort_values('total_market_value',0, ascending=False)
        result3 = result2.to_dict(orient = 'records')
        result4 = pd.DataFrame(result3)
        for i in range(len(result4)):
            result4.loc[i,'percent'] = int(result4.loc[i,'total_market_value']/self.pro_value_all()*10000)
            result4.loc[i,'percent'] = result4.loc[i,'percent']/100
        circle = sum(result['total_market_value'])
        for i in range(len(result4)):
            result4.loc[i,'circle_percent'] = int(result4.loc[i,'total_market_value']/circle*10000)
            result4.loc[i,'circle_percent'] = result4.loc[i,'circle_percent']/100
        result4.rename(columns = {'wd_trade_pname':'name','total_market_value':'amount'},inplace = True)
        return result4
    
    #《报告期末基金投资组合》
    def pro_fundHY_all(self):
        fundHY_sql = "select f.invest_ptype,i.total_market_value from lc_valuation_item i \
        left join lc_wd_fund f on right(i.item_code,6) = f.fund_num left join lc_valuation_file \
        ff on ff.valuation_id = i.valuation_id where (i.item_code LIKE '1105%' OR i.item_code \
        LIKE '1116%') AND LENGTH(i.item_code)>8 AND i.DATE='"+ self.date +"' and ff.is_valid = 1 \
        AND ff.status = 1 AND i.pro_code IN (SELECT CODE FROM lc_pro WHERE TYPE < 4);"
        logger.info("即将执行的sql语句：" + fundHY_sql)
        result = pd.read_sql(fundHY_sql,con = self.conn())
        if len(result) > 0:
            result = result.groupby('invest_ptype',as_index = False)['total_market_value'].sum()
            result1 = result.sort_values('total_market_value',0, ascending=False)
            result2 = result1.to_dict(orient = 'records')
            result3 = pd.DataFrame(result2)
            for i in range(len(result3)):
                result3.loc[i,'percent'] = int(result3.loc[i,'total_market_value']/self.pro_value_all()*10000)
                result3.loc[i,'percent'] = result3.loc[i,'percent']/100
            circle = sum(result3['total_market_value'])
            for i in range(len(result3)):
                result3.loc[i,'circle_percent'] = int(result3.loc[i,'total_market_value']/circle*10000)
                result3.loc[i,'circle_percent'] = result3.loc[i,'circle_percent']/100
            result3.rename(columns = {'invest_ptype':'name','total_market_value':'amount'},inplace = True)
            return result3
        else:
            return result
    
    #《报告期末按债券品种分类投资组合》
    def pro_bondHY_all(self):
        bondHY_sql = "select b.wd_bond_pcate,i.total_market_value FROM lc_wd_bond b LEFT JOIN \
        lc_valuation_item i ON b.bond_intro = i.item_name left join lc_valuation_file f on \
        f.valuation_id = i.valuation_id WHERE LENGTH(i.item_code)>8 AND i.item_code LIKE '1103%' \
        AND i.date = '"+ self.date +"' and f.is_valid = 1 and f.status = 1 and i.pro_code in \
        ( SELECT CODE FROM lc_pro WHERE TYPE < 4);"
        logger.info("即将执行的sql语句：" + bondHY_sql)
        result = pd.read_sql(bondHY_sql,con = self.conn())
        if len(result) > 0:
            result = result.groupby('wd_bond_pcate',as_index = False)['total_market_value'].sum()
            result1 = result.sort_values('total_market_value',0, ascending=False)
            result2 = result1.to_dict(orient = 'records')
            result3 = pd.DataFrame(result2)
            for i in range(len(result3)):
                result3.loc[i,'percent'] = int(result3.loc[i,'total_market_value']/self.pro_value_all()*10000)
                result3.loc[i,'percent'] = result3.loc[i,'percent']/100
            circle = sum(result3['total_market_value'])
            for i in range(len(result3)):
                result3.loc[i,'circle_percent'] = int(result3.loc[i,'total_market_value']/circle*10000)
                result3.loc[i,'circle_percent'] = result3.loc[i,'circle_percent']/100
            result3.rename(columns = {'wd_bond_pcate':'name','total_market_value':'amount'},inplace = True)
            return result3
        else:
            return result
    
    #《报告期末按商品板块分类投资组合》
    def pro_goodsHY_all(self):
        goods_sql = "select c.board as name,abs(i.total_market_value) as amount from lc_valuation_item i left \
        join lc_valuation_file f on i.valuation_id = f.valuation_id left join lc_wd_goods_cate c on \
        SUBSTR(i.item_code,9,2) = c.code where i.item_code like '3102%' and length(i.item_code)>8 and \
        SUBSTring(i.item_code,7,2)='01' AND i.pro_code IN (SELECT CODE FROM lc_pro WHERE TYPE < 4) and \
        f.status=1 AND f.is_valid=1 and i.date = '"+ self.date +"';"
        logger.info("即将执行的sql语句：" + goods_sql)
        result = pd.read_sql(goods_sql,con = self.conn())
        result1 = result.groupby('name',as_index = False)['amount'].sum()
        for i in range(len(result1)):
            result1.loc[i,'percent'] = int(result1.loc[i,'amount']/self.pro_value_all()*10000)
            result1.loc[i,'percent'] = result1.loc[i,'percent']/100
        circle = sum(result1['amount'])
        for i in range(len(result1)):
            result1.loc[i,'circle_percent'] = int(result1.loc[i,'amount']/circle*10000)
            result1.loc[i,'circle_percent'] = result1.loc[i,'circle_percent']/100
        goodsHY_report = result1.sort_values('amount',0, ascending=False)
        return goodsHY_report
    
if __name__ == "__main__":
        
    test = all_pro_report('2017-06-12')
    value_all = test.pro_value_all()
    print "某天资产总值"
    print value_all

    stock_report = test.pro_stock_all()
    print "《报告期末持仓市值前10的股票投资明细》"
    print stock_report
    
    fund_report = test.pro_fund_all()
    print "《报告期末持仓市前10的基金投资明细》"
    print fund_report
    
    bond_report = test.pro_bond_all()
    print "《 报告期末按公允价值占集合计划资产净值比例大小排名的前五名债券投资》"
    print bond_report
    
    goods_report = test.pro_goods_all()
    print "《报告期末按按合约价值占集合计划资产净值比例大小排名的前五名商品期货投资》"
    print goods_report
    
    stockHY_report = test.pro_stockHY_all()
    print "《报告期末按行业分类股票投资组合》"
    print stockHY_report
    
    fundHY_report = test.pro_fundHY_all()
    print "《报告期末基金投资组合》"
    print fundHY_report
    
    bondHY_report = test.pro_bondHY_all()
    print "《报告期末按债券品种分类投资组合》"
    print bondHY_report
    
    goodsHY_report = test.pro_goodsHY_all()
    print "《报告期末按商品板块分类投资组合》"
    print goodsHY_report

    fundHY_report = test.pro_fundHY_all()
    print "《报告期末基金投资组合》"
    print fundHY_report