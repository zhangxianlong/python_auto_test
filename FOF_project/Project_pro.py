# encoding:utf-8
import requests
import json
import time
from FOF_project import Base
from test.config import userconfig
from FOF_project import Ydl_oa_pro
from util import db_mysql
from test.config import dbconfig

#创建项目，并返回项目id
class Project():
    
    def __init__(self,host_fof,host_ydl):
        self.host_fof = host_fof #FOF的host
        self.host_ydl = host_ydl  #源动力的host

    #创建项目        
    def creat_pro(self,att_path = []):
        user = Base.Base(self.host_fof,self.host_ydl)
        atta = []
        for i in range(len(att_path)):
            r = user.attach(userconfig.user0_mobile, att_path[i])
            r_atta = {'file_ext':r['data']['ext'],
                      'file_name':r['data']['name'],
                      'file_path':r['data']['url'],
                      'file_size':r['data']['size'],
                      'name':r['data']['name']
                      }
            atta.append(r_atta)   
        url = self.host_fof + "/admin/Project/add"
        data = {"pro":{
                    "id":"",
                    "sn":"",
                    "name":"FOF项目-zxl：" + str(time.time()),
                    "type":1,
                    "dep_id":1,#项目所属部门 1/资产管理总部,2/财富管理总部
                    "business_type":1,#项目业务归属 1/权益投资类,2/固定收投资类,3/大类资产配置类（FOF类）,4/量化投资类,5/创新投资类
                    "pro_leader":"xxx",
                    "invest_sponsor":"xxx",
                    "pro_members":"xxx",
                    "is_structured":1,
                    "lever_ratio":"1",
                    "risk_level":1,
                    "target_scale":"111",
                    "is_own_cpl":1,#自有资金是否参与 1/自有资金参与,2/自有资金不参与
                    "own_cpl_scale":"1",
                    "manage_deadline":"111",
                    "closed_date":"1",
                    "is_open":1,
                    "open_date":"1",
                    "warning_line":"1",
                    "stop_line":"1",
                    "entrust_man":"xxx",
                    "manage_man":"xxx",
                    "trustee_man":"xxx",
                    "broker_man":"",
                    "spread_mechanism":"",
                    "other_man":"",
                    "fee_manage":"1",
                    "fee_trustee":"1",
                    "fee_broker":"",
                    "fee_sale":"",
                    "fee_subscription":"",
                    "fee_redeem":"",
                    "fee_other":"",
                    "achievement":"xxx",
                    "excess_ach_reward":"xxx",
                    "income_scheme":"xxx",
                    "invest_strategy":"1",
                    "invest_scope":"1",
                    "stop_act":"",
                    "own_cpl_comp_act":"",
                    "intro":"",
                    "st1":"20",
                    "st2":"10",
                    "st3":"2010",
                    "st":"",
                    "st20_detail":"",
                    "st30_detail":"",
                    "yn_lxh":"",
                    "yn_bwh":"",
                    "yn_fkh":"",
                    "yn_zyh":"",
                    "is_fkh":"",
                    "update_user":"",
                    "update_time":"",
                    "create_user":"",
                    "create_time":"",
                    "type_arr":[
                        {   "text":"主动管理型",
                            "value":1
                        },
                        {   "text":"投顾型",
                            "value":2
                        },
                        {   "text":"通道型",
                            "value":3
                        },
                        {   "text":"其他",
                            "value":4
                        }
                    ],
                    "dep_id_arr":[
                        {   "text":"资产管理总部",
                            "value":1
                        },
                        {   "text":"财富管理总部",
                            "value":2
                        }
                    ],
                    "business_type_arr":[
                        {   "text":"权益投资类",
                            "value":1
                        },
                        {   "text":"固定收投资类",
                            "value":2
                        },
                        {   "text":"大类资产配置类",
                            "value":3
                        },
                        {   "text":"量化投资类",
                            "value":4
                        },
                        {   "text":"创新投资类",
                            "value":5
                        }
                    ],
                    "is_structured_arr":[
                        {   "text":"非结构化",
                            "value":1
                        },
                        {   "text":"结构化",
                            "value":2
                        }
                    ],
                    "risk_level_arr":[
                        {   "text":"低分险",
                            "value":1
                        },
                        {   "text":"中低风险",
                            "value":2
                        },
                        {   "text":"中等风险",
                            "value":3
                        },
                        {   "text":"中高风险",
                            "value":4
                        },
                        {   "text":"高风险",
                            "value":5
                        }
                    ],
                    "is_own_cpl_arr":[
                        {   "text":"自有资金参与",
                            "value":1
                        },
                        {   "text":"自有资金不参与",
                            "value":2
                        }
                    ],
                    "is_open_arr":[
                        {   "text":"是",
                            "value":1

                        },
                        {   "text":"否",
                            "value":2
                        }
                    ]
                },
                "atta":atta
            }
        result = requests.post(url,json = data,headers = user.Login_fof(userconfig.user0_mobile).request.headers)
        user.Login_fof(userconfig.user0_mobile).cookies.clear() #清除cookies
        #print '项目id:',result.json()['msg'][20:]
        print result.json()['msg']
        #return result
        if result.json()['res'] == 1:
            print '项目id为：',result.json()['msg'][20:]
            return result.json()['msg'][20:]
        else:
            return '项目创建失败'
    
    #立项会节点审核    
    def lxh_sub(self):
        #如果不需要附件，则传空列表self.creat_pro([])
        project_id = self.creat_pro(['C:\\Users\\USER\\Desktop\\aaa\\faqiren\\test1.xls','C:\\Users\\USER\\Desktop\\aaa\\faqiren\\test2.xls'])
        #project_id = '819'
        user = Base.Base(self.host_fof,self.host_ydl)
        Ydl_oa = Ydl_oa_pro.Ydl_oa_pro(self.host_fof,self.host_ydl)
        atta_list = user.get_atta_list(project_id)
        if int(project_id):
            url_tj = self.host_fof + '/ProjectLxh/apiSub2Lxh'
            data_tj = {'id':project_id,
                       'memo':'提交立项会',
                       'file':atta_list
                       }
            user = Base.Base(self.host_fof,self.host_ydl)
            result_tj = requests.post(url_tj,json = data_tj,headers = user.Login_fof(userconfig.user2_mobile).request.headers)
            user.Login_fof(userconfig.user2_mobile).cookies.clear() #清除cookies
            print '立项会处理结果为：',
            print json.dumps(result_tj.json()).decode('unicode-escape')
            oa_sn = user.get_oa_sn(project_id)
            print '流程编号为：',
            print oa_sn
            task_id = Ydl_oa.get_task_id(oa_sn)
            oa_detail = Ydl_oa.get_oa_detail(oa_sn)
            audit_oa = Ydl_oa.audit_oa(oa_sn)
            print '流程处理结果为：',
            print audit_oa
            cron_res = user.Cron(oa_sn)
            print '立项会节点执行cron：',
            print cron_res
            #确认立项会决议
            url_qr = self.host_fof + '/ProjectLxh/apiConfirm'     
            data_qr = {"pro":{"id":project_id,"is_pass":1},
                       "atta":[]
                       }
            result_qr = requests.post(url_qr,json = data_qr,headers = user.Login_fof(userconfig.user2_mobile).request.headers)
            if result_qr.text[7:11] == 'true':
                print '立项会决议确认成功',
                print json.dumps(result_qr.json()).decode('unicode-escape') 
                return project_id
            else:
                print result_qr.json()
                return '立项会决议确认失败'            
        else:
            return '没有可以提交立项会OA的项目'
        
    #标委会节点审核
    def bwh_sub(self):
        Ydl_oa = Ydl_oa_pro.Ydl_oa_pro(self.host_fof,self.host_ydl)
        project_id = self.lxh_sub()
        #project_id = '233'
        url_rep = self.host_fof + '/ProjectBwh/fkbgsubmit'
        data_rep = {'id':project_id,
                'memo':'获取风控报告'}
        user = Base.Base(self.host_fof,self.host_ydl)
        result_rep = requests.post(url_rep,json = data_rep,headers = user.Login_fof(userconfig.user4_mobile).request.headers)        
        if result_rep.text[7:11] == 'true':
            print '获取风控与合规报告提交成功：',
            print result_rep.json()['msg']
            oa_sn = user.get_oa_sn(project_id)
            print '流程编号为：',
            print oa_sn
            task_id = Ydl_oa.get_task_id(oa_sn)
            oa_detail = Ydl_oa.get_oa_detail(oa_sn)
            audit_oa = Ydl_oa.audit_oa(oa_sn)
            print '流程处理结果为：',
            print audit_oa
            cron_res = user.Cron(oa_sn)
            print '标委会节点--获取风控与合规报告执行cron：',
            print cron_res
            #发起标委会上会=================================================================================
            url_yt = self.host_fof + '/ProjectBwh/bwhsubmit'
            data_yt = {'id':project_id,
                    'memo':'提交标委会上会'
                    }
            result_yt = requests.post(url_yt,json = data_yt,headers = user.Login_fof(userconfig.user4_mobile).request.headers)
            if result_yt.text[7:11] == 'true':
                print '标委会上会提交成功:',
                print result_yt.json()['msg']
                topic_id = user.get_topic_id(project_id)
                topic_detail = user.get_topic_detail(topic_id, userconfig.user4_mobile)
                open_topic = user.open_topic(topic_id, userconfig.user4_mobile)
                close_topic = user.close_topic(topic_id, userconfig.user4_mobile)
                cron_yt = user.Cron(topic_id)
                print '标委会节点完成上会执行cron：',
                print cron_res
                #确认标委会上会决议
                url_qr = self.host_fof + '/ProjectBwh/isfkh'
                data_qr = {"pro":{"id":project_id,
                               "is_fkh":1
                               },
                        "atta":[]
                        }
                result_qr = requests.post(url_qr,json = data_qr,headers = user.Login_fof(userconfig.user4_mobile).request.headers)
                if result_qr.text[7:11] == 'true':
                    print '标委会上会决议确认成功'
                    print result_qr.json()
                    return project_id 
                else:
                    print result_qr.json()
                    return '标委会上会决议确认失败'
            else:
                print '标委会上会提交失败',
                print result_yt.json()['msg'] 
            #等号之间注释掉，流程可以走到标委会待上会状态====================================================================================
        else:
            print '获取风控与合规报告提交失败：',
            return result_rep.json()['msg']
    
    #风控会节点审核
    def fkh_sub(self):
        project_id = self.bwh_sub()
        url = self.host_fof + '/ProjectOS/fkhConfirm'
        data = {"pro":{"id":project_id,
                       "is_pass":1
                       },
                "atta":[]
                }
        user = Base.Base(self.host_fof,self.host_ydl)
        result = requests.post(url,json = data,headers = user.Login_fof(userconfig.user6_mobile).request.headers)
        if result.json()['res'] == 1:
            print '风控会决议确认成功'
            return project_id
        else:
            print '风控会决议确认失败'
            return result.json()
    
    #自营投决会节点审核
    def zytj_sub(self):
        project_id = self.fkh_sub()
        url = self.host_fof + '/ProjectOS/zyhConfirm'
        data = {"pro":{"id":project_id,
                       "is_pass":1
                       },
                "atta":[]
                }
        user = Base.Base(self.host_fof,self.host_ydl)
        result = requests.post(url,json = data,headers = user.Login_fof(userconfig.user6_mobile).request.headers )
        if result.json()['res'] == 1:
            print '自营投决会决议确认成功'
            return result.json()
        else:
            print '自营投决会确认失败'
            return result.json()
        
    

    
if __name__ == "__main__":
    test = Project('http://stpro.qianyilc.com','http://bch.ydl.lczq.com')
    #项目创建,列表为空时，项目没有附件
    print test.creat_pro(['C:\\Users\\USER\\Desktop\\aaa\\faqiren\\test1.xls','C:\\Users\\USER\\Desktop\\aaa\\faqiren\\test2.xls']) 
    #print test.lxh_sub() #立项会节点
    #print test.bwh_sub() #标委会节点 
    #print test.fkh_sub() #风控会节点
    #print test.zytj_sub() #自营投决会节点