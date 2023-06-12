# 1、获取学校信息
# 地址：
# https://1413383348518193.cn-heyuan.pai-eas.aliyuncs.com/api/predict/sfg_test_srd
# body：
# {
# "school_id":1004,
# "type":1
# }
# 2、请求地址
# https://gk-1259218859.cos.ap-beijing.myqcloud.com/d/special_list.json?r=1686409329771

# 3、根据专业查询学校列表
# https://1413383348518193.cn-heyuan.pai-eas.aliyuncs.com/api/predict/sfg_test_srd

# {
#     "modelVersion": 0,
#     "province_id": 31,
#     "special_id": 110101,
#     "type": 6
# }
# 4、专业详情
# https://1413383348518193.cn-heyuan.pai-eas.aliyuncs.com/api/predict/sfg_test_srd
# {
#     "special_id": 110102,
#     "type": 4
# }
# 5、获取学校列表
# https://1413383348518193.cn-heyuan.pai-eas.aliyuncs.com/api/predict/sfg_test_srd
# {
#     "modelVersion": 0,
#     "province_id": 31,
#     "type": 7,
#     "xuanke_id": 0
# }
# 6、获取学校专业
# https://1413383348518193.cn-heyuan.pai-eas.aliyuncs.com/api/predict/sfg_test_srd
# {
#     "school_id": 1270,
#     "type": 2
# }
# 7、专业录取分数线
# https://1413383348518193.cn-heyuan.pai-eas.aliyuncs.com/api/predict/sfg_test_srd
# {
#     "modelVersion": 0,
#     "province_id": 31,
#     "school_id": 1270,
#     "type": 3,
#     "xuanke_id": 0
# }


'''
@,@python version: ,: python3
@,@Author: ,: chaotianjiao
@,@Date: ,: 2021-04-05 18:08:32
@,@LastEditors: ,: chaotianjiao
@,@LastEditTime: ,: 2021-06-14 23:37:35
'''

import requests
import json
import pandas as pd 

headers ={
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/6945",
    "Authorization":"YWQ2ZWYyOWMwNGNkNDllZWE1YzZhOGRmNzYzYjhkMDQwZjI2NjhmZg==",
    "Connection":"keep-alive",
    "Accept-Encoding":"gzip, deflate, br",
        "Accept":"*/*",
        "Content-Type":"application/json"
}

def get_school_info():
    """
        获取学校相关数据
    """
    url ="https://1413383348518193.cn-heyuan.pai-eas.aliyuncs.com/api/predict/sfg_test_srd"
    def get_all_school():
        """
            获取所有的学校列表
        """
        res = []
        params = {
            "modelVersion": 0,
            "province_id": 31,
            "type": 7,
            "xuanke_id": 0
            }
        r =requests.post(url,data=json.dumps(params),headers=headers)
        schools = json.loads(r.text)['school_lines']
        # print(schools)
        tmp = schools
        cols = list(schools[0].keys())
        for i in tmp:
            tmp_res = []
            for index, j in enumerate(cols):
                if index != len(cols)-1:
                    tmp_res.extend([i[j]])
                else:
                    for k in i[j]:
                        try:
                            score = k['score']
                        except:
                            score = None
                        try:
                            year = k['year']
                        except:
                            year = None
                        try:
                            rank = k['rank']
                        except:
                            rank = 0
                        tmp_res.extend([score, year, rank])
            res.append(tmp_res)
        df = pd.DataFrame(res, columns=cols[:-1] + ['score1', 'year1', 'rank1', \
                            'score2', 'year2', 'rank2', 'score3', 'year3', 'rank3'])
        df.to_csv('./data/school_list_info.csv', index=False, sep='\t', header=None)
        return df 
    # df = get_all_school()

    # school_id_list = set(df['school_id'].tolist())

    def get_school_info(school_id):
        """
            获取学校的每个细节信息
        """
        cols = []
        res = []
        for index, id in enumerate(school_id):
            tmp_res = []
            params = {
                "school_id":id,
                "type":1
                }
            r = requests.post(url, data=json.dumps(params), headers=headers)
            schools_info = json.loads(r.text)
            if index == 0:
                cols = list(schools_info.keys())
            for names in cols:
                tmp_res.extend([schools_info[names]])
            res.append(tmp_res)
        df = pd.DataFrame(res, columns=cols)
        df.to_csv('./data/school_info.csv', index=False, sep='\t', header=None)
    # get_school_info(school_id_list)

    def get_special_info():
        """
            获取专业信息
        """
        res = []
        cols = ['subject', 'special_class_name', 'special_class_id']
        cols_other = ['special_name', 'special_id', 'special_code', 'limit_year']
        url = "https://gk-1259218859.cos.ap-beijing.myqcloud.com/d/special_list.json?r=1686409329771"
        r = requests.get(url)
        special_info = json.loads(r.text)
        # print(special_info[0])
        for info in special_info:
            for i in info['special_classes']:
                tmp_res = []
                tmp_res.extend([info['subject'], i['special_class_name'], i['special_class_id']])
                for j in i['specials']:
                    tmp_tmp_res = []
                    tmp_tmp_res.extend(tmp_res + [j['special_name'], j['special_id'], j['special_code'], j['limit_year']])
                    # print(tmp_tmp_res)
                    res.append(tmp_tmp_res)
        df = pd.DataFrame(res, columns=['subject', 'special_class_name', 'special_class_id',
                                         'special_name', 'special_id', 'special_code', 'limit_year'])
        df.to_csv('./special_info.csv', index=False, sep='\t')
        return df         
    # df = get_special_info()
    # special_id_list = set(df['special_id'].tolist())

    def get_special_info_all(special_id_list):
        """
            获取专业详情
        """
        cols = ['special_name', 'special_id', 'special_code', 'is_what', 'learn_what', 
                'do_what', 'limit_year', 'degree', 'direction']
        res = []
        for index, id in enumerate(list(special_id_list)[:3]):
            params = {
                "special_id": id,
                "type":4
                }
            r = requests.post(url, data=json.dumps(params), headers=headers)
            specail_info = json.loads(r.text)
            tmp = []
            for i in cols:
                tmp.extend([specail_info[i]])
            res.append(tmp)
        df = pd.DataFrame(res, columns=cols)
        df.to_csv('special_info_list.csv', index=False, sep='\t')
    # get_special_info_all(special_id_list=special_id_list)
    

    def get_school_by_specical(specical_list):
        """
            根据专业查询学校列表
        """
        res = []
        cols = ['batch_name', 'school_id', 'school', 'batch_id', 'wenlike_id', 'wenlike', 'special_name', 'lines']
        for id in specical_list:
            params = {
                    "modelVersion": 0,
                    "province_id": 31,
                    "special_id": id,
                    "type": 6
                    }
            r = requests.post(url, data=json.dumps(params), headers=headers)
            school_info = json.loads(r.text)['special_score_line'][:2]
            for info in school_info:
                tmp = []
                for names in cols:
                    tmp.extend([info[names]])
                res.append([id] + tmp)
        df = pd.DataFrame(res, columns=cols)
        print(df)
                

    get_school_by_specical()


if __name__ == "__main__":
    get_school_info()

