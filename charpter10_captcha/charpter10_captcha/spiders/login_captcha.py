# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest
import json
from PIL import Image
from io import BytesIO
import pytesseract
from scrapy.log import logger


class CaptchaLoginSpider(scrapy.Spider):
    name = 'login_captcha'
    start_urls = ['http://XXX.com/']

    def parse(self, response):
        pass

    # X 网站登录页面的 url
    login_url = 'http://XXX.com/login'
    user = 'liushuo@XXX.com'
    password = '12345678'

    def start_requests(self):
        yield Request(self.login_url, callback=self.login, dont_filter=True)

    def login(self, response):
        # 该方法既是登录页面的解析函数，又是下载验证码图片的响应处理函数
        # 如果 response.mete['login_response'] 存在，当前 response 为验证码图片的响应
        # 否则当前 response 为登录页面的响应
        login_response = response.meta.get('login_response')

        if not login_response:
            # Step 1:
            # 此时 response 为登录页面的响应，从中提取验证码图片的 url，下载验证码图片
            captchaUrl = response.css('label.field.prepend-icon img::attr(src)').extract_first()

            captchaUrl = response.urljoin(captchaUrl)
            # 构造 Request 时，将当前 response 保存到 meta 字典中
            yield Request(captchaUrl, callback=self.login, meta={'login_response': response}, dont_filter=True)

        else:
            # Step 2
            # 此时，response 为验证码图片的响应，response.body 是图片二进制数据
            # login_response 为登录页面的响应，用其构造表单请求并发送
            formdata = {
                'email': self.user,
                'pass': self.password,
                # 使用 OCR 识别
                'code': self.get_captcha_by_OCR(response.body),
            }
            yield FormRequest.from_response(login_response, callback=self.parse_login, formdata=formdata, dont_filter=True)

    def parse_login(self, response):
        # 根据响应结果判断是否登录成功
        info = json.loads(response.text)
        if info['error'] == '0':
            logger.info('登录成功')
            return super().start_requests()

        logger.info('登录失败')
        return self.start_requests()

    def get_captcha_by_OCR(self, data):
        # OCR 识别
        img = Image.open(BytesIO(data))
        img = img.convert('L')
        captcha = pytesseract.image_to_string(img)
        img.close()

        return captcha

    def get_captcha_by_network(self, data):
        # 平台识别
        import requests
        import base64


        url = 'http://ali-checkcode.showapi.com/checkcode'
        appcode = 'f23cca37f287418a90e2f922649273c4'

        form = {}
        form['convert_to_jpg'] = '0'
        form['img_base64'] = base64.b64encode(data)
        form['typeId'] = '3040'

        headers = {'Authorization': 'APPCODE' + appcode}
        response = requests.post(url, headers=headers, data=form)
        res = response.json()

        if res['showapi_res_code'] == 0:
            return res['showapi_res_body']['Result']

        return ''

    def get_captcha_by_user(self, data):
        # 人工识别
        img = Image.open(BytesIO(data))
        img.show()
        captcha = input('输入验证码：')
        img.close()
        return captcha