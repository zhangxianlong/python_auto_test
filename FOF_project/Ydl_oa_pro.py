# encoding:utf-8
import requests
from config import userconfig
from FOF_project import Base

#源动力审核OA流
class Ydl_oa_pro:
    
    def __init__(self,host_fof,host_ydl):
        self.host_fof = host_fof #'http://stpro.qianyilc.com' FOF的host
        self.host_ydl = host_ydl #'http://bch.ydl.lczq.com'  源动力的host
        
    #获取流程的task_id    
    def get_task_id(self,oa_sn):
        url = self.host_ydl + '/task/apiOaTaskList?page=1&limit=10&type=1'
        user = Base.Base(self.host_fof,self.host_ydl)
        result = requests.get(url,cookies = user.Login_ydl(userconfig.userPT_mobile).cookies)
        #print result.json()  
        task_id = []
        for i in range(len(result.json()['data'])):
            if result.json()['data'][i]['oa_sn'] == oa_sn:
                task_id.append(result.json()['data'][i]['id'])
        #print 'task_id为:',task_id               
        return task_id
    
    #获取流程详情
    def get_oa_detail(self,oa_sn):
        url = self.host_ydl + '/log/getLogsBySn'
        data = {'oa_sn':oa_sn}
        user = Base.Base(self.host_fof,self.host_ydl)
        result = requests.get(url,params = data,cookies = user.Login_ydl(userconfig.userPT_mobile).cookies)
        #print json.dumps(result.json()).decode('unicode-escape')
        return result.json()
    
    #审核OA流程
    def audit_oa(self,oa_sn):
        task_id = self.get_task_id(oa_sn)
        oa_detail = self.get_oa_detail(oa_sn)
        url = self.host_ydl + '/oa/oaCheck'
        result = []
        for i in range(len(task_id)):
            data = {'achievement':oa_detail['data'][0]['data']['achievement'],
                    'back_task_id':0,
                    'broker_man':oa_detail['data'][0]['data']['broker_man'],
                    'business_type':oa_detail['data'][0]['data']['business_type'],
                    'check_childstatus':oa_detail['data'][0]['data']['check_childstatus'],
                    'check_status':1,
                    'closed_date':oa_detail['data'][0]['data']['closed_date'],
                    'countersign_users':[],
                    'dep_id':oa_detail['data'][0]['data']['dep_id'],
                    'entrust_man':oa_detail['data'][0]['data']['entrust_man'],
                    'excess_ach_reward':oa_detail['data'][0]['data']['excess_ach_reward'],
                    'fee_broker':oa_detail['data'][0]['data']['fee_broker'],
                    'fee_manage':oa_detail['data'][0]['data']['fee_manage'],
                    'fee_other':oa_detail['data'][0]['data']['fee_other'],
                    'fee_redeem':oa_detail['data'][0]['data']['fee_redeem'],
                    'fee_sale':oa_detail['data'][0]['data']['fee_sale'],
                    'fee_subscription':oa_detail['data'][0]['data']['fee_subscription'],
                    'fee_trustee':oa_detail['data'][0]['data']['fee_trustee'],
                    'form_data_id':0,
                    'form_id':"612",
                    'income_scheme':oa_detail['data'][0]['data']['income_scheme'],
                    'intro':oa_detail['data'][0]['data']['intro'],
                    'invest_scope':oa_detail['data'][0]['data']['invest_scope'],
                    'invest_sponsor':oa_detail['data'][0]['data']['invest_sponsor'],
                    'invest_strategy':oa_detail['data'][0]['data']['invest_strategy'],
                    'is_open':oa_detail['data'][0]['data']['is_open'],
                    'is_own_cpl':oa_detail['data'][0]['data']['is_own_cpl'],
                    'is_structured':oa_detail['data'][0]['data']['is_structured'],
                    'lever_ratio':oa_detail['data'][0]['data']['lever_ratio'],
                    'manage_deadline':oa_detail['data'][0]['data']['manage_deadline'],
                    'manage_man':oa_detail['data'][0]['data']['manage_man'],
                    'name':oa_detail['data'][0]['data']['name'],
                    'oa_sn':oa_detail['data'][0]['data']['oa_sn'],
                    'open_date':oa_detail['data'][0]['data']['open_date'],
                    'other_man':oa_detail['data'][0]['data']['other_man'],
                    'own_cpl_comp_act':oa_detail['data'][0]['data']['own_cpl_comp_act'],
                    'own_cpl_scale':oa_detail['data'][0]['data']['own_cpl_scale'],
                    'pass_halfway_task':task_id[i],
                    'pro_leade':oa_detail['data'][0]['data']['pro_leade'],
                    'pro_members':oa_detail['data'][0]['data']['pro_members'],
                    'risk_level':oa_detail['data'][0]['data']['risk_level'],
                    'spread_mechanism':oa_detail['data'][0]['data']['spread_mechanism'],
                    'stop_act':oa_detail['data'][0]['data']['stop_act'],
                    'stop_line':oa_detail['data'][0]['data']['stop_line'],
                    'target_scale':oa_detail['data'][0]['data']['target_scale'],
                    'task_id':task_id[i],
                    'title':oa_detail['data'][0]['data']['title'],
                    'trustee_man':oa_detail['data'][0]['data']['trustee_man'],
                    'type':oa_detail['data'][0]['data']['type'],
                    'warning_line':oa_detail['data'][0]['data']['warning_line']
                    }
            user = Base.Base(self.host_fof,self.host_ydl)
            re = requests.post(url,data = data,cookies = user.Login_ydl(userconfig.userPT_mobile).cookies)
            result.append(re.json())
        return result
    
        
if __name__ == '__main__':
    test = Ydl_oa_pro('http://stpro.qianyilc.com','http://bch.ydl.lczq.com')
    test.get_task_id('270')
    test.get_oa_detail('270')
    test.audit_oa()
