#coding=UTF-8
import requests
import re
import json

""" 
Request 的异常处理封装 
"""
class Request:
    def __init__(self):
        requests.adapters.DEFAULT_RETRIES = 5
        pass
    
    def Post(self, url, cookies = None, data = None, params = None, allow_redirects = True, timeout = 20, ErrMsg = None):
        try:
            req = requests.post(
                url=url, 
                headers=ReadJson('./config/network.json')['Headers'],
                cookies=cookies,
                data=data,
                params=params,
                allow_redirects=allow_redirects,
                timeout=timeout)  
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            if ErrMsg:
                print(ErrMsg)
            raise SystemExit(e)
        
        return req

    def Get(self, url, cookies = None, params = None, allow_redirects = True, timeout = 20, ErrMsg = None):
        try:
            req = requests.get(
                url=url, 
                headers=ReadJson('./config/network.json')['Headers'],
                cookies=cookies,
                params=params,
                allow_redirects=allow_redirects,
                timeout=timeout)  
            req.raise_for_status()
        except requests.exceptions.RequestException as e:
            if ErrMsg:
                print(ErrMsg)
            raise SystemExit(e)
        
        return req
    
    
def ReadJson(filePath):
    with open(filePath, "r") as f: 
        return json.load(f)
    
def ReadNetWorkJson():
    json_data = ReadJson('./config/network.json')
    return (json_data['Headers'], json_data['Urls'])

def ReadAccountJson():
    json_data = ReadJson('./config/account.json')
    username, password = (json_data['UserName'], json_data['PassWord'])
    if(username == '' or password == ''):
        raise Exception('请在 data/account.json 中输入用户名和密码')
    return (username, password)

def ReadLessonJson():
    json_data = ReadJson('./config/lesson.json')
    lessonList = json_data['LessonID']
    if(len(lessonList) == 0):
        raise Exception('请在 data/lesson.json 中输入想要选择的课程ID')
    return lessonList

def ServiceGetter(service_field):
    json_data = ReadJson('./config/service.json')
    service_res = json_data[service_field]
    return service_res

def PayloadGetter(key):
    json_data = ReadJson('./config/payload.json')
    return json_data[key]

def MergeCookieJar(cookiejar_list):
    cookie_dict = {}
    for cookiejar in cookiejar_list:
        tmp_dict = requests.utils.dict_from_cookiejar(cookiejar)
        cookie_dict.update(tmp_dict)
        
    return requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True)

def findClassList(raw_str, lessonId):
    res = re.findall(r"\{id:(\d+),no:'(.*?)',name:'(.*?)'", raw_str)
    for class_tuple in res:
        if lessonId == class_tuple[1]:
            return class_tuple
    raise Exception("未搜索到课程结果，请检查LessonId")

def isCourseAvailable(raw_str, lessonNo):
    res = re.findall(r"'(\d+?)':{sc:(\d+?),lc:(\d+?)}", raw_str)
    for class_tuple in res:
        if lessonNo == class_tuple[0]:
            return int(class_tuple[1]) < int(class_tuple[2])

if __name__ == '__main__':
    ReadLessonJson()