#encoding=utf-8
from util import db_mysql
from config import dbconfig
import pandas as pd
from util import logger


pd.set_option('display.height',1000)
pd.set_option('display.width',1000)
#pd.set_option('display.max_rows',500)
#pd.set_option('display.max_columns',500)

#此脚本用于查询单产品股票、基金、债券的日报数据
class single_pro_report:
    date = ''
    pro_id = ''
    
    def __init__(self,date,pro_id):
        self.date = date
        self.pro_id = pro_id
    
    #连接数据库
    def conn(self):
        db = db_mysql.db_mysql(dbconfig.host_177,
                               dbconfig.user_177,
                               dbconfig.passwd_177,
                               dbconfig.db_177,
                               dbconfig.port_177)
        conn = db.connentDB()
        return conn
    
    #先检查这天是否存在有效版本号
    def check_ver(self):
        ver_sql = "select ver from lc_cron_job where date = '"+ self.date +"' and new_status = 1;"
        logger.info("即将执行的sql语句：" + ver_sql)
        ver = pd.read_sql(ver_sql,con = self.conn())
        ver = ver.to_dict(orient = 'records')
        return ver
        
    
    #《报告期末持仓市值前10的股票投资明细》
    def pro_stock_single(self):
        stock_sql = "SELECT RIGHT(i.item_code,6) AS code,st.stockname AS name,i.amount AS hold,i.unit_market_value \
        AS price,ROUND((i.total_market_value)/(s.total_market_value)*100,4) AS percent,\
        TRUNCATE((i.amount)*(i.unit_market_value),3) AS market_value FROM lc_valuation_item i LEFT JOIN \
        lc_valuation_file f ON f.valuation_id = i.valuation_id LEFT JOIN lc_valuation_stats s ON \
        f.valuation_id = s.valuation_id LEFT JOIN lc_wd_stock st ON RIGHT(i.item_code,6) = st.stocknum \
        WHERE i.item_code LIKE '1102%' AND i.pro_id="+ self.pro_id +" AND LENGTH(i.item_code)>8 AND \
        i.date='"+ self.date +"' AND f.is_valid = 1 AND f.status = 1 AND s.item_code ='asset_net_value' \
        ORDER BY i.total_market_value DESC;"
        logger.info("即将执行的sql语句：" + stock_sql)
        stock_report = pd.read_sql(stock_sql,con = self.conn())
        for i in range(len(stock_report)):
            stock_report.loc[i,'percent'] = int(stock_report.loc[i,'percent']*100)
            stock_report.loc[i,'percent'] = stock_report.loc[i,'percent']/100
        return stock_report
    
    #《报告期末持仓市前10的基金投资明细》
    def pro_fund_single(self):
        fund_sql = "SELECT (i.amount*i.unit_market_value) AS market_value,RIGHT(i.item_code,6) AS code,i.item_name \
        AS name,i.amount AS units,i.unit_cost AS start_value,i.unit_market_value AS current_value,\
        TRUNCATE((i.amount*i.unit_market_value)/(s.total_market_value)*100,2) AS percent FROM lc_valuation_item i \
        LEFT JOIN lc_valuation_file f ON f.valuation_id = i.valuation_id LEFT JOIN lc_valuation_stats s \
        ON f.valuation_id = s.valuation_id WHERE (i.item_code LIKE '1105%' OR i.item_code LIKE '1116%') \
        AND i.pro_id="+ self.pro_id +" AND LENGTH(i.item_code)>8 AND i.DATE='"+ self.date +"' AND \
        f.is_valid = 1 AND f.status = 1 AND s.item_code ='asset_net_value' AND i.pro_code IN \
        (SELECT CODE FROM lc_pro WHERE TYPE < 4);"
        logger.info("即将执行的sql语句：" + fund_sql)
        fund_report = pd.read_sql(fund_sql,con = self.conn())
        return fund_report
    
    #《报告期末按公允价值占集合计划资产净值比例大小排名的前五名债券投资》
    def pro_bond_single(self):
        bond_sql = "SELECT b.bond_code as code,i.item_name as name,i.total_market_value as market_value,\
        i.total_market_value AS fair_value,b.wd_hy_cate1 as cate,b.zx_zxpj as credit,i.amount,\
        TRUNCATE((i.total_market_value)/(s.total_market_value)*100,2) AS percent FROM lc_wd_bond b LEFT JOIN \
        lc_valuation_item i ON b.bond_intro = i.item_name LEFT JOIN lc_valuation_file f ON \
        i.valuation_id = f.valuation_id LEFT JOIN lc_valuation_stats s ON f.valuation_id = \
        s.valuation_id WHERE i.item_code LIKE '1103%' AND (LENGTH(i.item_code)=14 OR \
        LENGTH(i.item_code)=17) AND i.pro_id = "+ self.pro_id +" AND i.date ='"+ self.date +"' \
        AND f.is_valid = 1 AND f.status = 1 AND s.item_code ='asset_net_value' GROUP BY \
        b.bond_code;"
        logger.info("即将执行的sql语句：" + bond_sql)
        bond_report = pd.read_sql(bond_sql, con = self.conn())
        return bond_report
    
    #《报告期末按按合约价值占集合计划资产净值比例大小排名的前五名商品期货投资》
    def pro_goods_single(self):
        goods_sql = "select i.total_market_value,c.name,ABS(i.total_market_value) AS ABS,\
        ABS(i.market_value_proportion) AS percent from lc_valuation_item \
        i left join lc_valuation_file f on i.valuation_id = f.valuation_id left join lc_wd_goods_cate c \
        on SUBSTR(i.item_code,9,2) = c.code where i.item_code like '3102%' and length(i.item_code)>8 and \
        SUBSTring(i.item_code,7,2)='01' AND i.pro_code IN (SELECT CODE FROM lc_pro WHERE TYPE < 4) and \
        f.status=1 AND f.is_valid=1 and i.date = '"+ self.date +"' and i.pro_id = "+ self.pro_id +";"
        logger.info("即将执行的sql语句：" + goods_sql)
        result = pd.read_sql(goods_sql,con = self.conn())
        if len(result) > 0:
            result_poor = result.groupby('name',as_index = False)['total_market_value'].sum()#轧差数据
            result_tvalue = result.groupby('name',as_index = False)['ABS'].sum()#合约价值数据
            result_percent = result.groupby('name',as_index = False)['percent'].sum()#占比数据
            for i in range(len(result)):
                if result.loc[i,'total_market_value'] > 0:
                    result.loc[i,'long'] = result.loc[i,'total_market_value']
                    result.loc[i,'bear'] = 0
                else:
                    result.loc[i,'long'] = 0
                    result.loc[i,'bear'] = result.loc[i,'total_market_value']
            result_long = result.groupby('name',as_index = False)['long'].sum()#多头数据
            result_bear = result.groupby('name',as_index = False)['bear'].sum()#空头数据
            result_bear['long'] = result_long['long']
            result_bear['tvalue'] = result_tvalue['ABS']
            result_bear['poor'] = result_poor['total_market_value']
            result_bear['percent'] = result_percent['percent']
            for i in range(len(result_bear)):
                result_bear.loc[i,'percent'] = round(result_bear.loc[i,'percent'],2)
                #result_bear.loc[i,'percent'] = result_bear.loc[i,'percent']/100
            return result_bear
        else:
            return result
    
    #《报告期末按行业分类股票投资组合》
    def pro_stockHY_sigle(self):
        stockHY_sql = "select s.wd_trade_pname as name,i.total_market_value as amount,\
        truncate(i.total_market_value/ss.total_market_value*100,2) as percent from lc_wd_stock s \
        left join lc_valuation_item i on s.stocknum = right(i.item_code,6) left join lc_valuation_file f \
        on i.valuation_id = f.valuation_id left join lc_valuation_stats ss on f.valuation_id = \
        ss.valuation_id WHERE i.date = '"+ self.date +"' AND LENGTH(i.item_code)>8 AND \
        i.item_code LIKE '1102%' and i.pro_id = "+ self.pro_id +" and f.is_valid = 1 and \
        f.status = 1 and ss.item_code = 'asset_net_value';"
        logger.info("即将执行的sql语句：" + stockHY_sql)
        result = pd.read_sql(stockHY_sql, con = self.conn())
        stockHY_report_a = result.groupby('name',as_index = False)['amount'].sum()
        stockHY_report_p = result.groupby('name',as_index = False)['percent'].sum()
        stockHY_report_a['percent'] = stockHY_report_p['percent']
        stockHY_report = stockHY_report_a.sort_values('amount',0, ascending=False)
        circle = sum(stockHY_report['amount'])
        stockHY_report['circle_percent'] = stockHY_report['amount']/circle * 100 * 100
        for i in range(len(stockHY_report)):
            stockHY_report.loc[i,'circle_percent'] = int(stockHY_report.loc[i,'circle_percent'])
        stockHY_report['circle_percent'] = stockHY_report['circle_percent']/100
        stockHY_report['percent'] = stockHY_report['percent'] * 100
        for i in range(len(stockHY_report)):
            stockHY_report.loc[i,'percent'] = int(stockHY_report.loc[i,'percent'])
        stockHY_report['percent'] = stockHY_report['percent']/100
        return stockHY_report
    
    #《报告期末基金投资组合》
    def pro_fundHY_single(self):
        fundHY_sql = "select fu.invest_ptype as name,i.total_market_value as amount,\
        truncate(i.total_market_value/s.total_market_value*100,2) as percent from lc_valuation_item i \
        left join lc_wd_fund fu on right(i.item_code,6) = fu.fund_num left join \
        lc_valuation_file f on i.valuation_id = f.valuation_id left join lc_valuation_stats s \
        on f.valuation_id = s.valuation_id where (i.item_code LIKE '1105%' OR i.item_code LIKE '1116%') \
        AND i.pro_id = "+ self.pro_id +" AND LENGTH(i.item_code)>8 AND i.DATE='"+ self.date +"' AND \
        f.is_valid = 1 AND f.status = 1 AND i.pro_code IN (SELECT CODE FROM lc_pro WHERE TYPE < 4) and \
        s.item_code = 'asset_net_value';"
        logger.info("即将执行的sql语句：" + fundHY_sql)
        result = pd.read_sql(fundHY_sql, con = self.conn())
        fundHY_report_a = result.groupby('name',as_index = False)['amount'].sum()
        fundHY_report_p = result.groupby('name',as_index = False)['percent'].sum()
        fundHY_report_a['percent'] = fundHY_report_p['percent']
        fundHY_report = fundHY_report_a.sort_values('amount',0, ascending=False)
        circle = sum(fundHY_report['amount'])
        fundHY_report['circle_percent'] = fundHY_report['amount']/circle * 100 * 100
        for i in range(len(fundHY_report)):
            fundHY_report.loc[i,'circle_percent'] = int(fundHY_report.loc[i,'circle_percent'])
        fundHY_report['circle_percent'] = fundHY_report['circle_percent']/100   
        return fundHY_report
    
    #《报告期末按债券品种分类投资组合》
    def pro_bondHY_single(self):
        bondHY_sql = "SELECT b.wd_bond_pcate AS name,i.total_market_value AS amount,\
        TRUNCATE(i.total_market_value/s.total_market_value*100,2) as percent FROM lc_wd_bond b \
        LEFT JOIN lc_valuation_item i ON b.bond_intro = i.item_name LEFT JOIN lc_valuation_file \
        f ON i.valuation_id = f.valuation_id LEFT JOIN lc_valuation_stats s ON f.valuation_id = \
        s.valuation_id WHERE LENGTH(i.item_code)>8 AND i.item_code LIKE '1103%' AND i.date = \
        '" + self.date +"' AND i.pro_id = "+ self.pro_id +" AND f.is_valid = 1 AND f.status \
        = 1 AND s.item_code = 'asset_net_value';"
        logger.info("即将执行的sql语句：" + bondHY_sql)
        result = pd.read_sql(bondHY_sql, con = self.conn())
        result1 = result.groupby('name',as_index = False)['amount'].sum()
        result2 = result.groupby('name',as_index = False)['percent'].sum()
        result1['percent'] = result2['percent']
        circle = sum(result1['amount'])
        result1['circle_percent'] = result1['amount']/circle * 100 * 100
        for i in range(len(result1)):
            result1.loc[i,'circle_percent'] = int(result1.loc[i,'circle_percent'])
        result1['circle_percent'] = result1['circle_percent']/100
        bondHY_report = result1      
        return bondHY_report
    
    #《报告期末按商品板块分类投资组合》
    def pro_goodsHY_single(self):
        goods_sql = "SELECT c.board,ABS(i.total_market_value) AS amount,ABS(i.market_value_proportion) \
        AS percent FROM lc_valuation_item i LEFT JOIN lc_valuation_file f ON i.valuation_id = \
        f.valuation_id LEFT JOIN lc_wd_goods_cate c ON SUBSTR(i.item_code,9,2) = c.code WHERE \
        i.item_code LIKE '3102%' AND LENGTH(i.item_code)>8 AND SUBSTRING(i.item_code,7,2)='01' \
        AND i.pro_code IN (SELECT CODE FROM lc_pro WHERE TYPE < 4) AND f.status=1 AND f.is_valid=1 \
        AND i.date = '"+ self.date +"' AND i.pro_id = "+ self.pro_id +";"
        logger.info("即将执行的sql语句：" + goods_sql)
        result = pd.read_sql(goods_sql,con = self.conn())
        result_amount = result.groupby('board',as_index = False)['amount'].sum()
        result_percent = result.groupby('board',as_index = False)['percent'].sum()
        result_percent['amount'] = result_amount['amount']
        for i in range(len(result_percent)):
            result_percent.loc[i,'percent'] = int(result_percent.loc[i,'percent']*100)
            result_percent.loc[i,'percent'] =result_percent.loc[i,'percent']/100
        circle = sum(result_percent['amount'])
        for i in range(len(result_percent)):
            result_percent.loc[i,'circle_percent'] = int(result_percent.loc[i,'amount']/circle*10000)
            result_percent.loc[i,'circle_percent'] = result_percent.loc[i,'circle_percent']/100
        goodsHY_report = result_percent.sort_values('amount',0, ascending=False)
        goodsHY_report.rename(columns = {'board':'name'},inplace = True)
        return goodsHY_report

if __name__ == "__main__":

    test = single_pro_report('2017-11-01','235')
    ver = test.check_ver()
    print "有效版本号是："
    print ver   
    stock_report = test.pro_stock_single()
    print "《报告期末持仓市值前10的股票投资明细》"
    print stock_report
  
    fund_report = test.pro_fund_single()
    print "《报告期末持仓市前10的基金投资明细》"
    print fund_report
    
    bond_report = test.pro_bond_single()
    print "《报告期末按公允价值占集合计划资产净值比例大小排名的前五名债券投资》"
    print bond_report

    goods_report = test.pro_goods_single()
    print "《报告期末按按合约价值占集合计划资产净值比例大小排名的前五名商品期货投资》"
    print goods_report
     
    stockHY_report = test.pro_stockHY_sigle()
    print "《报告期末按行业分类股票投资组合》"
    print stockHY_report
   
    fundHY_report = test.pro_fundHY_single()
    print "《报告期末基金投资组合》"
    print fundHY_report
    
    bondHY_report = test.pro_bondHY_single()
    print "《报告期末按债券品种分类投资组合》"
    print bondHY_report
    
    goodsHY_report = test.pro_goodsHY_single()
    print "《报告期末按商品板块分类投资组合》"
    print goodsHY_report

    goodsHY_report = test.pro_goodsHY_single()
    print "《报告期末按商品板块分类投资组合》"
    print goodsHY_report
