import json
import os
import re
from utils import *

_, URL_DICT = ReadNetWorkJson()

class CookieGetter(Request):
    def __init__(self):
        super(CookieGetter, self).__init__()
        self.loginUrl = URL_DICT['LOGIN']
        self.xkUrl = URL_DICT['XK']
        self.defaultPage = URL_DICT['MAIN_PAGE']
        self.url = URL_DICT['BASE_URL']
        self.username, self.password = ReadAccountJson()
        self.selCourseParams = PayloadGetter('selCourseParams')
        self.selCourseParams['username'], self.selCourseParams['password']  = self.username, self.password
        
    def getCookies(self):
        req = self.Post(url=self.loginUrl, params=self.selCourseParams, allow_redirects=False)
        cookies = req.cookies
        redirect_url = "".join([self.xkUrl, req.headers['Location']])
        req = self.Get(url=redirect_url, cookies=cookies)
        redirect_url = re.search("(?<=href=\").*(?=\")", req.text).group(0)
        if(redirect_url):
            req = self.Get(
                url=redirect_url,
                cookies=cookies
            )
        return cookies
        
    
if __name__ == '__main__':
    cookieGetter = CookieGetter()
    cookieGetter.getCookies()