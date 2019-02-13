# encoding:utf-8
import requests
#import json

class Report_http:
    host = ''
    date = ''
    pro_name = ''
    
    def __init__(self,host,date,pro_id):
        self.host = 'http://stpro.qianyilc.com'
        self.date = date
        self.pro_id = pro_id
    
    #登录FOF标准化业务管理系统
    def login(self):
        url = self.host + '/Admin/Login/login'
        data = {'user_name':'admin',
            'passwd':123456,
            'authcode':4444}
        result = requests.post(url,params = data)
        return result
    
    #获取要查询的产品id，版本号
    def get_ver(self):
        url = self.host + '/Admin/Report/apidayreportrecord'
        data = {'day' : self.date}
        result = requests.post(url, json = data, cookies = self.login().cookies)
        if result.status_code == 200:
            if result.json()['data']['list']:
                result = result.json()['data']['list'][0]
                return result
            else:
                return "有效批次号不存在"
        else:
            return "请求失败"

    
    #获取接口单只产品某日的日报数据
    def get_single_report(self):
        url = self.host + '/Admin/ProAnalysis/singleOther'
        if type(self.get_ver()) is dict:            
            data = {'date':self.date,
                    'pro_id':self.pro_id,
                    'ver':self.get_ver()['ver']
                    }
            result = requests.post(url, json = data, cookies = self.login().cookies)
            result = result.json()['data']
            return result
        else:
            return "有效批次号不存在"
        
    #获取接口单只产品某日的组合报告
    def get_single_General(self):
        url = self.host + '/Admin/ProAnalysis/singleGeneralFxck'
        if type(self.get_ver()) is dict:
            data = {'date':self.date,
                    'pro_id':self.pro_id,
                    'ver':self.get_ver()['ver']
                    }
            result = requests.post(url,json = data, cookies = self.login().cookies)
            return result.json()['data']
        else:
            return "有效批次号不存在"
    
    #获取接口总产品某日的日报数据
    def get_all_report(self):
        url = self.host + '/Admin/ProAnalysis/otherSum'
        if type(self.get_ver()) is dict:
            data = {'date':self.date,
                    'ver':self.get_ver()['ver']
                    }
            result = requests.post(url, json = data, cookies = self.login().cookies)
            result = result.json()['data']
            return result
        else:
            return "有效批次号不存在"
        
    #获取接口总产品某日的组合报告
    def get_all_General(self):
        url = self.host + '/Admin/ProAnalysis/generalInvestreportFxck'
        if type(self.get_ver()) is dict:
            data = {'date':self.date,
                    'ver':self.get_ver()['ver']}
            result = requests.post(url,json = data, cookies = self.login().cookies)
            return result.json()['data']
        else:
            return "有效批次号不存在"
    
    
    """ 
    def sss(self):
        url = self.host + '/admin/upload'
        data = {"files":[{"size":18,"filename":"qqq.txt","relpath":"data:text/plain;base64,zfXG87bszt7Iusj0zt7Iusj0"}]}
        result = requests.post(url, data = data, cookies = self.login().cookies)
        print type(data)      
        return result
    """
    
if __name__ == "__main__":
    test = Report_http('host','2017-06-27',48)
    print test.login()
    print test.get_ver()
    print test.get_single_General()
    print test.get_all_General()
    #print test.get_ver()['pro_id']
    #print test.get_ver()
    #print test.get_single_report()['gp']['detail']['list']
    #print test.get_single_report()
    #print test.get_all_report()['gp']['detail']['list']
    #print test.get_all_report()
    
