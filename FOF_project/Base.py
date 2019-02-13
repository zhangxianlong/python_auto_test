# encoding:utf-8
import requests
from config import userconfig
from util import db_mysql
from config import dbconfig
import time
import json

#公用类
class Base():
    
    def __init__(self,host_fof,host_ydl):
        self.host_fof = host_fof #FOF的host
        self.host_ydl = host_ydl  #源动力的host
    
    #登录源动力系统
    def Login_ydl(self,user_name):
        url = self.host_ydl + '/staff/login'
        data = {'mobile':user_name,
                'password':'111111',
                'verify_code':''}
        result = requests.post(url,data = data)
        return result
    
    #登录源动力跳转到FOF系统，并返回请求头
    def Login_fof(self,user_name):
        url_ydl = self.host_ydl + '/staff/login'
        data_ydl = {'mobile':user_name,
                'password':'111111',
                'verify_code':''}
        result_ydl = requests.post(url_ydl,data = data_ydl)
        url_fof = self.host_ydl + '/qianyiaction/goFof'
        result_fof = requests.get(url_fof,cookies = result_ydl.cookies)
        return result_fof
    
    #提交OA后，获取流程号oa_sn
    def get_oa_sn(self,project_id):
        db = db_mysql.db_mysql(dbconfig.host_177,
                               dbconfig.user_177,
                               dbconfig.passwd_177,
                               dbconfig.db_177,
                               dbconfig.port_177)
        db.connentDB()
        project_name = db.querySQL("SELECT NAME FROM lc_project WHERE id = "+ project_id +";")
        param = db.querySQL("SELECT param FROM lc_ydl_api_log ORDER BY id DESC LIMIT 1;")
        #print project_name[0][0]
        oa_sn = []
        for i in range(len(param)):
            param_json = eval(eval(param[i][0])) #evl()将str转换为dict
            if param_json.has_key('name'):
                #print '项目名称为：',
                #print param_json['name'].decode('unicode_escape')
                if project_name[0][0] == param_json['name'].decode('unicode_escape'):
                    if param_json.has_key('oa_sn'):
                        oa_sn.append(param_json['oa_sn'])
        if type(oa_sn) is list:
            return oa_sn[0]
        else:
            return 'oa_sn获取失败'
    
    
    #确认获取回调结果后，执行cron    
    def Cron(self,oa_sn):
        cron = 'http://stpro.qianyilc.com/Cron/Ydl/resultHandle'
        db = db_mysql.db_mysql(dbconfig.host_177,
                               dbconfig.user_177,
                               dbconfig.passwd_177,
                               dbconfig.db_177,
                               dbconfig.port_177)
        #需要在循环内重新连接数据库查询
        st_code = []
        while True:
            db.connentDB()
            back_notify = db.querySQL("SELECT * FROM lc_ydl_notify WHERE notify_id = "+ oa_sn +";")
            print '回调结果为：', back_notify
            if back_notify != None:
                result = requests.get(url = cron)
                st_code.append(result.status_code)
                return st_code
                break
            else:
                time.sleep(5)
            db.connClose()
            
    #获取议题id
    def get_topic_id(self,project_id):
        db = db_mysql.db_mysql(dbconfig.host_177,
                       dbconfig.user_177,
                       dbconfig.passwd_177,
                       dbconfig.db_177,
                       dbconfig.port_177)
        db.connentDB()
        result = db.querySQL("SELECT * FROM lc_ydl_api_log ORDER BY id DESC LIMIT 5;")
        #print result[0][7]
        for i in range(len(result)):
            param_json = eval(eval(result[i][4]))
            if param_json.has_key('form_id'):
                if param_json['form_id'] == project_id:
                    print '议题id为：',
                    print result[i][7][17:20]
                    return result[i][7][17:20]
            else:
                print "该项目的议题未提交成功，请重新提交"
    
    #获取议题详情        
    def get_topic_detail(self,topic_id,user_name):
        url = self.host_ydl + '/MeetingTopic/getTopicList'
        data = {'page':1,
                'limit':5,
                'type':1
                }
        result = requests.get(url,data,cookies = self.Login_ydl(user_name).cookies)
        for i in range(len(result.json()['data'])):
            if result.json()['data'][i]['id'] == topic_id:
                #print '议题详情为：',
                #print result.json()['data'][i]
                return result.json()['data'][i]
            else:
                return '获取议题详情，议题不存在'
    
    #开启议题
    def open_topic(self,topic_id,user_name):
        if type(self.get_topic_detail(topic_id,user_name)) is dict:
            url = self.host_ydl + '/MeetingTopic/addTopic'
            data = {"id":topic_id,
                    "name":self.get_topic_detail(topic_id,user_name)['name'],
                    "content_type":"text",
                    "content_value":self.get_topic_detail(topic_id,user_name)['name'],
                    "start_time":1508912280000,
                    "end_time":1509085080000,
                    "form":"fof",
                    "form_type":"1",
                    "execute_uids":"2770",
                    "look_uids":"2770",
                    "is_vote":"0",
                    "message":0,
                    "execute_uids_arr":["2770"],
                    "look_uids_arr":["2770"],
                    "attachment_ids":[]
                    }
            result = requests.get(url,json = data,cookies = self.Login_ydl(user_name).cookies)
            print '开启议题结果为：',
            print json.dumps(result.json()).decode('unicode-escape')
            return result.json()
        else:
            return '开启议题，议题不存在'
    
    #关闭议题    
    def close_topic(self,topic_id,user_name):
        url = self.host_ydl + '/MeetingTopic/colseTopic'
        data = {'result':1,
                'topic_id':topic_id
                }
        result = requests.post(url, data, cookies = self.Login_ydl(user_name).cookies)
        print '关闭议题结果为：',
        print json.dumps(result.json()).decode('unicode-escape')
        return result.json()
    
    #上传附件
    #注意：文件路径和文件名不能包含中文
    def attach(self,user_name,att_path):
        url = self.host_fof + '/admin/upload/webUploader'
        #files = {'file':('test1.xls',open(att_path,'rb'))}
        files = {'file':(open(att_path,'rb'))}
        result = requests.post(url,headers = self.Login_fof(user_name).request.headers,files = files)
        return result.json()
    
    #获取附件列表
    def get_atta_list(self,project_id):
        #项目全景接口
        url_detail = self.host_fof + '/ProjectLxh/apiCheck'
        data_detail = {'id':project_id}
        result_atta = requests.post(url_detail,json = data_detail,headers = self.Login_fof(userconfig.user2_mobile).request.headers)
        #项目中的附件为atta
        detail_atta = result_atta.json()['data']['base']['file']
        #print detail_atta
        atta_list = []                
        for i in range(len(detail_atta)):
            atta_dic = {}
            atta_dic['ext'] = detail_atta[i]['file_ext']
            atta_dic['file_size'] = detail_atta[i]['file_size']
            atta_dic['filename'] = detail_atta[i]['file_name']
            atta_dic['id'] = detail_atta[i]['id']
            atta_dic['url'] = detail_atta[i]['check']
            atta_list.append(atta_dic)
        print '附件列表为：',
        print atta_list
        return atta_list
    
    
    
      

if __name__ == '__main__':
    test = Base('http://stpro.qianyilc.com','http://bch.ydl.lczq.com')
    #print test.Login_ydl(userconfig.user0_mobile).json()
    #print test.Login_fof(userconfig.user0_mobile).request.headers
    #print test.get_oa_sn('539')
    #print test.Cron('1111')
    #print test.attach(userconfig.user0_mobile,'C:\\Users\\USER\\Desktop\\aaa\\faqiren\\test1.xls')
    print test.get_atta_list(842)