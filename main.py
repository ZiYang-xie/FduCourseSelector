#coding=UTF-8
import json
import re
import base64
import time
from cookie_getter import CookieGetter
from captcha import read_captcha
from email_sender import sendEmail
from utils import *

_, URL_DICT = ReadNetWorkJson()

class CourseSearcher(CookieGetter):
    def __init__(self, profileId=ReadLessonJson()[1], CAPTCHA_TYPE='slide'): # This param will change with the semester
        super(CourseSearcher, self).__init__()
        self.profileId = profileId
        self.CAPTCHA_TYPE = CAPTCHA_TYPE
        self.mainUrl = URL_DICT['MAIN_PAGE']
        self.xkPageUrl = URL_DICT["XK_PAGE"]
        self.baseUrl = URL_DICT['BASE_URL']
        self.selCourseUrl = URL_DICT['SELECT_COURSE']
        self.captchaUrl = URL_DICT["CAPTCHA"]
        self.secondMajorUrl = URL_DICT["SECONDMAJOR_PAGE"]
        
        self.baseUrl = self.addProfParam(self.baseUrl)
        self.selCourseUrl = self.addProfParam(self.selCourseUrl)

        self.form_data = PayloadGetter('formData')
        self.main_page_data = PayloadGetter('mainPageData')
        self.captcha_ret_data = PayloadGetter('captcha_ret')
        self.main_page_data['electionProfile.id'] = profileId
        self.courseIdList = ReadLessonJson()[0]
        self.cookies = self.getCookies()
        
    def RunScript(self):
        for lessonNo in self.courseIdList:
            self.addCourse(lessonNo)

    def addProfParam(self, url):
        prof_param = {'profileId':self.profileId}
        url = AddParam(url, prof_param)
        return url
        
    def addCourse(self, lessonNo):
        res = self.searchCourse(lessonNo)
        course_no, course_id, course_name = findClassList(res.text, lessonNo)
        if isCourseAvailable(res.text, course_no):
            info = "课程 [" + course_name + " " + course_id +"], 可选, 正在选课中"
            print(info)
            #sendEmail(info)
            result = self.selCourse(course_no)
            return result
        else:
            info = "课程 [" + course_name + " " + course_id +"], 目前不可选"
            print(info)
            return False
        
    def searchCourse(self, lessonNo):
        form = self.form_data
        form['lessonNo'] = lessonNo
        
        self.direct_to_selCoursePage() # 验证步骤，必须执行，不然会被服务器反制
        
        res = self.Post(
            url=self.baseUrl,
            cookies=self.cookies,
            data = form,
            ErrMsg="Serch Course Error (getCourseNoAndId)"
        )
        return res
    
    def direct_to_selCoursePage(self):
        param = {'_':int(time.time())}
        xkPageUrl_t = AddParam(self.xkPageUrl, param)
        self.Get(
            url=xkPageUrl_t,
            cookies=self.cookies,
            ErrMsg="Get Main Page Error (getCourseNoAndId) Get"
        )

        if self.secondMajor == 1:
            self.Get(
                url=self.secondMajorUrl,
                cookies=self.cookies,
                ErrMsg="Get Second Major Page Error (getCourseNoAndId) Get"
            )

        self.Post(
            url=self.mainUrl,
            cookies=self.cookies,
            data = self.main_page_data,
            ErrMsg="Into Xk Page Error (getCourseNoAndId) Post"
        )

    def handleCAPTCHA(self):
        if self.CAPTCHA_TYPE == 'slide':
            moveEnd_X, wbili = self.getCaptcha()
            self.captcha_ret_data['moveEnd_X'] = moveEnd_X
            self.captcha_ret_data['wbili'] = wbili
            response = self.Post(
                url=self.captchaUrl,
                cookies=self.cookies,
                data=self.captcha_ret_data,
                ErrMsg="CAPTCHA Error (captchaUrl)"
            )
            captcha_response = 'captcha_response'
        elif self.CAPTCHA_TYPE == 'img':
            result = self.getCaptcha()
            captcha_response = result
        else:
            raise NotImplementedError
        return captcha_response
    

    # 抢课（捡漏）
    def selCourse(self, course_no):
        captcha_response = self.handleCAPTCHA()
        form_data = {
            'optype': 'true',
            'operator0': course_no + ':true:0',
            'captcha_response': captcha_response
        }
        response = self.Post(
            url=self.selCourseUrl,
            cookies=self.cookies,
            data=form_data,
            ErrMsg="selCourse Error (selCourse)"
        )
        result = response.content.decode(encoding='utf-8')
        cleaned_text = extract_output_text(result)
        print(cleaned_text)
        
    def getCaptcha(self):
        param = {'_':int(time.time())}
        captchaUrl = AddParam(self.captchaUrl, param)
        response = self.Get(
            url=captchaUrl,
            cookies=self.cookies,
            ErrMsg="Get Captcha Error (getCaptcha)"
        )
        captcha = read_captcha(response.content)
        return captcha
    

if __name__ == "__main__":
    launcher = CourseSearcher()
    launcher.RunScript()
            