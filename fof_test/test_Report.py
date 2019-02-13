# encoding:utf-8
import unittest
import json
from single_pro_report import single_pro_report
from Report_http import Report_http
from all_pro_report import all_pro_report
#import pandas as pd
#import chardet
#import os,sys
"""
此脚本用于检查某日单产品日报
以及某日总产品日报
"""

class Report_test(unittest.TestCase):
    
    def setUp(self):
        self.host = 'http://stpro.qianyilc.com'
        self.date = '2017-08-15'
        self.pro_id = '1'
        self.Other = Report_http(self.host,self.date,self.pro_id)
        self.single_pro_report = single_pro_report(self.date,self.pro_id)
        self.all_pro_report = all_pro_report(self.date)
        
    def tearDown(self):
        print '执行完成'   
    
    #校验单只产品日报的股票数据
    def test_stock(self):
        if type(self.Other.get_single_report()) is dict:
            a = self.Other.get_single_report()['gp']['detail']['list']
            for i in range(len(a)):
                a[i]['market_value'] = float(a[i]['market_value'])
                a[i]['price'] = float(a[i]['price'])
                a[i]['percent'] = float(a[i]['percent'])
                a[i]['hold'] = float(a[i]['hold'])
        else:
            a = [self.Other.get_single_report()]
        if self.single_pro_report.check_ver():
            b = self.single_pro_report.pro_stock_single().to_dict(orient = 'records')#to_dict(orient = 'records')---将pd转换为dict
            bb = json.dumps(b).decode('unicode-escape')
            b = json.loads(bb)
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)
    
    #校验单只产品日报的基金数据    
    def test_fund(self):
        if type(self.Other.get_single_report())is dict:
            a = self.Other.get_single_report()['jj']['detail']['list']
            for i in range(len(a)):
                a[i]['market_value'] = float(a[i]['market_value'])
                a[i]['percent'] = float(a[i]['percent'])
                a[i]['current_value'] = float(a[i]['current_value'])
                a[i]['units'] = float(a[i]['units'])
                a[i]['start_value'] = float(a[i]['start_value'])
        else:
            a = [self.Other.get_single_report()]
        if self.single_pro_report.check_ver():
            b = self.single_pro_report.pro_fund_single().to_dict(orient = 'records')
            bb = json.dumps(b).decode('unicode-escape')
            b = json.loads(bb)
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)
    
    #校验单只产品日报的债券数据    
    def test_bond(self):
        if type(self.Other.get_single_report()) is dict:
            a = self.Other.get_single_report()['zq']['detail']['list']
            for i in range(len(a)):
                a[i]['market_value'] = float(a[i]['market_value'])
                a[i]['percent'] = float(a[i]['percent'])
                a[i]['fair_value'] = float(a[i]['fair_value'])
                a[i]['amount'] = float(a[i]['amount'])
        else:
            a = [self.Other.get_single_report()]
        if self.single_pro_report.check_ver():
            b = self.single_pro_report.pro_bond_single().to_dict(orient = 'records')
            bb = json.dumps(b).decode('unicode-escape')
            b = json.loads(bb)
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)
        
    #校验单只产品日报的商品期货数据
    def test_goods(self):
        if type(self.Other.get_single_report()) is dict:
            a = self.Other.get_single_report()['qh']['detail']['list']           
            for i in range(len(a)):
                a[i]['poor'] = float(a[i]['poor'])
                a[i]['percent'] = float(a[i]['percent'])
                a[i]['bear'] = float(a[i]['bear'])
                a[i]['tvalue'] = float(a[i]['tvalue'])
                a[i]['long'] = float(a[i]['long'])
        else:
            a = [self.Other.get_single_report()]
        if self.single_pro_report.check_ver():
            b = self.single_pro_report.pro_goods_single().to_dict(orient = 'records')
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)      
        
    #校验单只产品日报的股票组合数据
    def test_stockHY(self):
        if type(self.Other.get_single_report()) is dict:            
            a = self.Other.get_single_report()['gp']['pie']['list']        
            for i in range(len(a)):
                a[i]['circle_percent'] = float(a[i]['circle_percent'])
                a[i]['amount'] = float(a[i]['amount'])
                a[i]['percent'] = float(a[i]['percent'])
        else:
            a = [self.Other.get_single_report()]
        if self.single_pro_report.check_ver():
            b = self.single_pro_report.pro_stockHY_sigle().to_dict(orient = 'records')
            bb = json.dumps(b).decode('unicode-escape')
            b = json.loads(bb)
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)
   
    #校验单只产品日报的基金组合数据
    def test_fundHY(self):
        if type(self.Other.get_single_report()) is dict:            
            a = self.Other.get_single_report()['jj']['pie']['list']
            for i in range(len(a)):
                a[i]['circle_percent'] = float(a[i]['circle_percent'])
                a[i]['amount'] = float(a[i]['amount'])
                a[i]['percent'] = float(a[i]['percent'])
        else:
            a = [self.Other.get_single_report()]
        if self.single_pro_report.check_ver():
            b = self.single_pro_report.pro_fundHY_single().to_dict(orient = 'records')
            bb = json.dumps(b).decode('unicode-escape')
            b = json.loads(bb)
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)

    #校验单只产品日报的债券组合数据
    def test_bondHY(self):
        if type(self.Other.get_single_report()) is dict:
            a = self.Other.get_single_report()['zq']['pie']['list']
            for i in range(len(a)):
                a[i]['circle_percent'] = float(a[i]['circle_percent'])
                a[i]['amount'] = float(a[i]['amount'])
                a[i]['percent'] = float(a[i]['percent'])
        else:
            a = [self.Other.get_single_report()]
        if self.single_pro_report.check_ver():
            b = self.single_pro_report.pro_bondHY_single().to_dict(orient = 'records') 
            bb = json.dumps(b).decode('unicode-escape')
            b = json.loads(bb)
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)
        
    #校验单只产品日报的商品期货组合数据
    def test_goodsHY(self):
        if type(self.Other.get_single_report()) is dict:
            print json.dumps(self.Other.get_single_report()).decode('unicode-escape')
            a = self.Other.get_single_report()['qh']['pie']['list']
            for i in range(len(a)):
                a[i]['circle_percent'] = float(a[i]['circle_percent'])
                a[i]['amount'] = float(a[i]['amount'])
                a[i]['percent'] = float(a[i]['percent'])
        else:
            a = [self.Other.get_single_report()]
        if self.single_pro_report.check_ver():
            b = self.single_pro_report.pro_goodsHY_single().to_dict(orient = 'records')
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)
    
    
    #校验总产品日报的股票数据    
    def test_allstock(self):
        if type(self.Other.get_all_report()) is dict:
            a = self.Other.get_all_report()['gp']['detail']['list']
            for i in range(len(a)):
                a[i]['market_value'] = float(a[i]['market_value'])
                a[i]['price'] = float(a[i]['price'])
                a[i]['percent'] = float(a[i]['percent'])
                a[i]['hold'] = float(a[i]['hold'])
        else:
            a = [self.Other.get_all_report()]
        if self.single_pro_report.check_ver():
            b = self.all_pro_report.pro_stock_all().to_dict(orient = 'records')
            bb = json.dumps(b).decode('unicode-escape')
            b = json.loads(bb)
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)
        
    #校验总产品日报的基金数据
    def test_allfund(self):
        if type(self.Other.get_all_report()) is dict:
            a = self.Other.get_all_report()['jj']['detail']['list']
            for i in range(len(a)):
                a[i]['market_value'] = float(a[i]['market_value'])
                a[i]['current_value'] = float(a[i]['current_value'])
                a[i]['percent'] = float(a[i]['percent'])
                a[i]['units'] = float(a[i]['units'])
                a[i]['start_value'] = float(a[i]['start_value'])
        else:
            a = [self.Other.get_all_report()]
        if self.single_pro_report.check_ver():
            b = self.all_pro_report.pro_fund_all().to_dict(orient = 'records')
            bb = json.dumps(b).decode('unicode-escape')
            b = json.loads(bb)
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)        
    
    #校验总产品日报的债券数据
    def test_allbond(self):
        if type(self.Other.get_all_report()) is dict:
            a = self.Other.get_all_report()['zq']['detail']['list']
            for i in range(len(a)):
                a[i]['market_value'] = float(a[i]['market_value'])
                a[i]['percent'] = float(a[i]['percent'])
                a[i]['fair_value'] = float(a[i]['fair_value'])
                a[i]['amount'] = float(a[i]['amount'])
        else:
            a = [self.Other.get_all_report()]
        if self.single_pro_report.check_ver():
            b = self.all_pro_report.pro_bond_all().to_dict(orient = 'records')
            bb = json.dumps(b).decode('unicode-escape')
            b = json.loads(bb)
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a, b)
        
    #校验总产品日报的商品期货数据
    def test_allgoods(self):
        if type(self.Other.get_all_report()) is dict:
            a = self.Other.get_all_report()['qh']['detail']['list']
            for i in range(len(a)):
                a[i]['poor'] = float(a[i]['poor'])
                a[i]['percent'] = float(a[i]['percent'])
                a[i]['bear'] = float(a[i]['bear'])
                a[i]['tvalue'] = float(a[i]['tvalue'])
                a[i]['long'] = float(a[i]['long'])
        else:
            a = [self.Other.get_all_report()]
        if self.single_pro_report.check_ver():
            b = self.all_pro_report.pro_goods_all().to_dict(orient = 'records')
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')  
        self.assertListEqual(a,b)            
    
    #校验总产品日报的股票组合数据
    def test_allstockHY(self):
        if type(self.Other.get_all_report()) is dict:
            a = self.Other.get_all_report()['gp']['pie']['list']
            for i in range(len(a)):
                a[i]['circle_percent'] = float(a[i]['circle_percent'])
                a[i]['amount'] = float(a[i]['amount'])
                a[i]['percent'] = float(a[i]['percent'])
        else:
            a = [self.Other.get_all_report()]
        if self.single_pro_report.check_ver():
            b = self.all_pro_report.pro_stockHY_all().to_dict(orient = 'records')
            bb = json.dumps(b).decode('unicode-escape')
            b = json.loads(bb)
        else:
            b = ["有效批次号不存在"]                      
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)
    
    #校验总产品日报的基金组合数据
    def test_allfundHY(self):
        if type(self.Other.get_all_report()) is dict:
            a = self.Other.get_all_report()['jj']['pie']['list']
            for i in range(len(a)):
                a[i]['circle_percent'] = float(a[i]['circle_percent'])
                a[i]['amount'] = float(a[i]['amount'])
                a[i]['percent'] = float(a[i]['percent'])
        else:
            a = [self.Other.get_all_report()]
        if self.single_pro_report.check_ver():
            b = self.all_pro_report.pro_fundHY_all().to_dict(orient = 'records')
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')
        self.assertListEqual(a,b)
        
    #校验总产品日报的债券组合数据
    def test_allbondHY(self):
        if type(self.Other.get_all_report()) is dict:
            a = self.Other.get_all_report()['zq']['pie']['list']
            for i in range(len(a)):
                a[i]['circle_percent'] = float(a[i]['circle_percent'])
                a[i]['amount'] = float(a[i]['amount'])
                a[i]['percent'] = float(a[i]['percent'])
        else:
            a = [self.Other.get_all_report()]
        if self.single_pro_report.check_ver():            
            b = self.all_pro_report.pro_bondHY_all().to_dict(orient = 'records')
        else:
            b = ["有效批次号不存在"]
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape')                
        self.assertListEqual(a,b)
    
    #校验总产品日报的商品期货组合数据
    def test_allgoodsHY(self):
        if type(self.Other.get_all_report()) is dict:
            a = self.Other.get_all_report()['qh']['pie']['list']
            for i in range(len(a)):
                a[i]['circle_percent'] = float(a[i]['circle_percent'])
                a[i]['amount'] = float(a[i]['amount'])
                a[i]['percent'] = float(a[i]['percent'])
        else:
            a = [self.Other.get_all_report()]
        if self.single_pro_report.check_ver():
            b = self.all_pro_report.pro_goodsHY_all().to_dict(orient = 'records')
        else:
            b = ["有效批次号不存在"]     
        #print json.dumps(a).decode('unicode-escape')
        #print json.dumps(b).decode('unicode-escape') 
        self.assertListEqual(a,b)     
      
if __name__ =='__main__':
    unittest.main
    