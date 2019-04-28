from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, ElementNotVisibleException, \
ElementNotSelectableException
from selenium.webdriver import ActionChains
import time
import json
from func import params_encode, get_image
import logging


logging.basicConfig(level=logging.WARNING,
                    filename='D:/Work-warehouse/qichacha/log/log.txt',
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')


result_data = []
duplicate_entFddr = []  # 去重


class Sspider:

    _USERNAME = 'xxx'  # 第三方打码API账号
    _PASSWORD = 'xxx'  # 第三方打码API密码
    _FILE_NAME = None  # 需要识别的图片路径
    _MONGO_HOST = 'localhost'
    _MONGO_PORT = 27017
    _MONGO_DB = 'Qcc'
    _MONGO_COL = 'Data'
    _ITEM = {'entName': None,  # 企业名称
                        'entFddbr': None,  # 法定代表人
                        'cxDate': None,  # 查询时间
                        'entAddress': None,  # 地址
                        'qyxydm': None,  # 信用代码
                        'gsxxResultList': [{  # 工商信息
                            'entZczb': None,  # 企业注册资本
                            'entZczbIs': None,  # 实缴资本
                            'entzt': None,  # 企业状态
                            'entclsj': None,  # 企业成立时间
                            'entXydm': None,  # 信用代码
                            'entSbh': None,  # 纳税人识别号
                            'entZch': None,  # 注册号
                            'entJgdm': None,  # 组织机构代码
                            'entGsType': None,  # 公司类型
                            'entXy': None,  # 所属行业
                            'entclsjIs': None,  # 核准日期
                            'entRegister': None,  # 登记机关
                            'entRegion': None,  # 所属地区
                            'entEname': None,  # 英文名
                            'entOutName': None,  # 曾用名
                            'entPledgeCount': None,  # 参保人数
                            'entManMany': None,  # 人员规模
                            'entStopTime': None,  # 营业期限
                            'entAddress': None,  # 企业地址
                            'entScope': None  # 经营范围
                        }],
                        'bgjlResultList': [  # 变更记录
                            # 'bgNo': None,  # 变更序号
                            # 'bgDate': None,  # 变更日期
                            # 'bgpri': None,  # 变更项目
                            # 'bgBefore': None,  # 变更前
                            # 'bgLater': None  # 变更后
                        ]}

    def __init__(self, addr):
        self._user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        self._exe_path = r'C:\Users\CLay\AppData\Local\Google\Chrome\Application\chromedriver.exe'  # windows
        self._url_login = 'https://www.qichacha.com/user_login'
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        # chrome_options.add_argument('--headless')
        dcap = dict(DesiredCapabilities.CHROME)
        dcap['chrome.page.user.settings'] = self._user_agent
        self.driver = webdriver.Chrome(executable_path=self._exe_path, desired_capabilities=dcap, options=chrome_options)
        self.addr = addr

    def _move(self, driver, slider, xoffset=None):
        '''
        移动滑条
        :param driver:
        :param slider:
        :return:
        '''
        ActionChains(driver).click_and_hold(slider).perform()
        ActionChains(driver).move_by_offset(xoffset=xoffset, yoffset=0).perform()
        time.sleep(0.3)
        ActionChains(driver).release().perform()

    def _main(self):
        try:
            self.driver.get('https://www.qichacha.com/')  # 直接访问登录链接可能会被当成恶意访问
            self.driver.maximize_window()
            self.driver.find_element_by_xpath('/html/body/header/div/ul[2]/li[9]/a').click()

            try:
                WebDriverWait(self.driver, 2).until(EC.visibility_of_element_located((By.ID, 'normalLogin')))
            except (NoSuchElementException, TimeoutException, NoSuchElementException, WebDriverException,
                    ElementNotVisibleException, ElementNotSelectableException, BaseException) as e:
                logging.error(msg=e)
                self.driver.refresh()
            self.driver.find_element_by_xpath('//*[@id="normalLogin"]').click()  # 首页登录按钮
            time.sleep(1)
            self.driver.find_element_by_id('nameNormal').send_keys('13535045165')  # 账号
            self.driver.find_element_by_id('pwdNormal').send_keys('l1198659788')
            time.sleep(1)

            data = ''
            try:
                WebDriverWait(self.driver, 4).until(
                    EC.visibility_of_element_located((By.XPATH, ('//*[@id="nc_1__scale_text"]/span'))))
                self.driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span').click()  # 阿里验证码
                self._move(driver=self.driver, slider=self.driver.find_element_by_xpath('//*[@id="nc_1__scale_text"]/span'),
                           xoffset=308)
                WebDriverWait(self.driver, 4).until(EC.visibility_of_element_located((By.CLASS_NAME, 'imgCaptcha_img')))
                dr = self.driver.find_element_by_xpath('//*[@id="nc_1__imgCaptcha_img"]/img')
                data = dr.get_attribute('src')[22:]  # 获取图片base64后的数据
            except (NoSuchElementException, TimeoutException, NoSuchElementException, WebDriverException,
                    ElementNotVisibleException, ElementNotSelectableException, BaseException) as e:
                logging.error(msg=e)
                self.driver.refresh()

            # TODO(CLay): 此处可调用打码平台或者进行图片处理识别
            if get_image(data):
                self.FILE_NAME = get_image(data)  # 获取base64转本地图片之后的绝对路径
            # 手动打码
            captcha_key = input('''
                请手动输入验证码：
            ''').strip()
            time.sleep(6)

            self.driver.find_element_by_xpath('//*[@id="nc_1_captcha_input"]').send_keys(captcha_key)
            self.driver.find_element_by_xpath('//*[@id="nc_1_scale_submit"]/span').click()

            if self.driver.find_element_by_class_name('imgCaptcha_btn').get_attribute('style') == 'border-top-color: red;':
                self.driver.refresh()

            time.sleep(1)
            self.driver.find_element_by_xpath('//*[@id="user_login_normal"]/button').click()
            self.driver.maximize_window()

            try:
                WebDriverWait(self.driver, 3).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="bindwxModal"]/div/div/div/button')))
                self.driver.find_element_by_xpath('//*[@id="bindwxModal"]/div/div/div/button').click()
            except (NoSuchElementException, TimeoutException, NoSuchElementException, WebDriverException,
                    ElementNotVisibleException, ElementNotSelectableException, BaseException) as e:
                logging.error(msg=e)
                self.driver.refresh()  # TODO

            # 搜索框
            self.driver.find_element_by_xpath('//*[@id="searchkey"]').send_keys(self.addr)
            time.sleep(1.5)
            self.driver.find_element_by_xpath('//*[@id="V3_Search_bt"]').click()

            # 遍历第一页页面详细链接
            a_list = self.driver.find_elements_by_class_name('ma_h1')
            urls = [i.get_attribute('href') for i in a_list]
            for url in urls:
                js = "window.open('{}')".format(url)
                time.sleep(0.1)
                self.driver.execute_script(js)
            all_handles = self.driver.window_handles

            for handle1 in all_handles[1:]:
                self.driver.switch_to.window(handle1)
                item = self._ITEM
                try:
                    # 判断公司是否是需要爬取
                    WebDriverWait(self.driver, 1).until(EC.visibility_of_element_located((By.XPATH, ('//*[@class="ntable"][2]'))))
                    item['cxDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    item['entName'] = self.driver.find_element_by_xpath(
                        '//*[@id="company-top"]/div[2]/div[2]/div[1]/h1').text
                    item['entFddbr'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[1]/tbody/tr[2]/td[1]/div/div[1]/div[2]/a/h2').text
                    item['entAddress'] = self.driver.find_element_by_xpath(
                        '//*[@id="company-top"]/div[2]/div[2]/div[3]/div[2]/span[3]/a[1]').text
                    item['qyxydm'] = self.driver.find_element_by_xpath('//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[2]').text
                    item['gsxxResultList'][0]['entZczb'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[1]/td[2]').text
                    item['gsxxResultList'][0]['entZczbIs'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[1]/td[4]').text
                    item['gsxxResultList'][0]['entzt'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[2]/td[2]').text
                    item['gsxxResultList'][0]['entclsj'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[2]/td[4]').text
                    item['gsxxResultList'][0]['entXydm'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[2]').text
                    item['gsxxResultList'][0]['entSbh'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[4]').text
                    item['gsxxResultList'][0]['entZch'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[4]/td[2]').text
                    item['gsxxResultList'][0]['entJgdm'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[4]').text
                    item['gsxxResultList'][0]['entGsType'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[5]/td[2]').text
                    item['gsxxResultList'][0]['entXy'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[5]/td[4]').text
                    item['gsxxResultList'][0]['entclsjIs'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[6]/td[2]').text
                    item['gsxxResultList'][0]['entRegister'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[6]/td[4]').text
                    item['gsxxResultList'][0]['entRegion'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[7]/td[2]').text
                    item['gsxxResultList'][0]['entEname'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[7]/td[4]').text
                    item['gsxxResultList'][0]['entOutName'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[8]/td[2]/span').text
                    item['gsxxResultList'][0]['entPledgeCount'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[8]/td[4]').text
                    item['gsxxResultList'][0]['entManMany'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[9]/td[2]').text
                    item['gsxxResultList'][0]['entStopTime'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[9]/td[4]').text
                    item['gsxxResultList'][0]['entAddress'] = self.driver.find_element_by_xpath(
                        '//*[@id="company-top"]/div[2]/div[2]/div[3]/div[2]/span[3]/a[1]').text
                    item['gsxxResultList'][0]['entScope'] = self.driver.find_element_by_xpath(
                        '//*[@id="Cominfo"]/table[2]/tbody/tr[11]/td[2]').text

                    # 变更记录
                    tr_list = self.driver.find_element_by_id('Changelist').find_elements_by_tag_name('tr')[1:]
                    for tr in tr_list:
                        bg_dict = {}
                        bg_dict['bgNo'] = tr.find_element_by_xpath('td[1]').text
                        bg_dict['bgDate'] = tr.find_element_by_xpath('td[2]').text
                        bg_dict['bgpri'] = tr.find_element_by_xpath('td[3]').text
                        bg_dict['bgBefore'] = tr.find_element_by_xpath('td[4]').text
                        bg_dict['bgLater'] = tr.find_element_by_xpath('td[5]').text
                        item['bgjlResultList'].append(bg_dict)
                    if item['entFddbr'] not in duplicate_entFddr:
                        result_data.append(item)
                        duplicate_entFddr.append(item['entFddbr'])
                    self.driver.close()  # 关闭当前窗口
                except (NoSuchElementException, TimeoutException, NoSuchElementException, WebDriverException,
                        ElementNotVisibleException, ElementNotSelectableException, BaseException) as e:
                    # self.main(addr=addr)
                    logging.error(msg=e)
                    self.driver.close()
                    continue

            if len(urls) >= 20:
                # 切换到第一页
                self.driver.switch_to.window(all_handles[0])
                params_encode_list = params_encode(addr=self.addr)
                for next_url_key in params_encode_list:
                    next_url = 'https://www.qichacha.com/search?' + next_url_key
                    js = "window.open('{}', '_blank')".format(next_url)
                    self.driver.execute_script(js)  # 句柄停留在最后一个打开的页面
                    all_next_page_handles = self.driver.window_handles  # 获取前五个页面的句柄
                    if all_next_page_handles[1]:
                        self.driver.switch_to.window(all_next_page_handles[1])  # 切换到第二个窗口
                        a_detail_list = self.driver.find_elements_by_class_name('ma_h1')
                        urls_detail = [j.get_attribute('href') for j in a_detail_list]
                        for url_detail in urls_detail:
                            js_detail = "window.open('{}')".format(url_detail)
                            self.driver.execute_script(js_detail)
                        all_handles_detail = self.driver.window_handles  # 获取主页面下的子页面句柄

                        # 遍历详细页面链接
                        for handle_detail in all_handles_detail[1:]:
                            self.driver.switch_to.window(handle_detail)
                            item = self._ITEM
                            try:
                                # 判断公司是否是需要爬取
                                WebDriverWait(self.driver, 1).until(
                                    EC.visibility_of_element_located((By.XPATH, ('//*[@class="ntable"][2]'))))
                                item['cxDate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                                item['entName'] = self.driver.find_element_by_xpath(
                                    '//*[@id="company-top"]/div[2]/div[2]/div[1]/h1').text
                                item['entFddbr'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[1]/tbody/tr[2]/td[1]/div/div[1]/div[2]/a/h2').text
                                item['entAddress'] = self.driver.find_element_by_xpath(
                                    '//*[@id="company-top"]/div[2]/div[2]/div[3]/div[2]/span[3]/a[1]').text
                                item['qyxydm'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[2]').text
                                item['gsxxResultList'][0]['entZczb'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[1]/td[2]').text
                                item['gsxxResultList'][0]['entZczbIs'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[1]/td[4]').text
                                item['gsxxResultList'][0]['entzt'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[2]/td[2]').text
                                item['gsxxResultList'][0]['entclsj'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[2]/td[4]').text
                                item['gsxxResultList'][0]['entXydm'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[2]').text
                                item['gsxxResultList'][0]['entSbh'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[4]').text
                                item['gsxxResultList'][0]['entZch'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[4]/td[2]').text
                                item['gsxxResultList'][0]['entJgdm'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[3]/td[4]').text
                                item['gsxxResultList'][0]['entGsType'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[5]/td[2]').text
                                item['gsxxResultList'][0]['entXy'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[5]/td[4]').text
                                item['gsxxResultList'][0]['entclsjIs'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[6]/td[2]').text
                                item['gsxxResultList'][0]['entRegister'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[6]/td[4]').text
                                item['gsxxResultList'][0]['entRegion'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[7]/td[2]').text
                                item['gsxxResultList'][0]['entEname'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[7]/td[4]').text
                                item['gsxxResultList'][0]['entOutName'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[8]/td[2]/span').text
                                item['gsxxResultList'][0]['entPledgeCount'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[8]/td[4]').text
                                item['gsxxResultList'][0]['entManMany'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[9]/td[2]').text
                                item['gsxxResultList'][0]['entStopTime'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[9]/td[4]').text
                                item['gsxxResultList'][0]['entAddress'] = self.driver.find_element_by_xpath(
                                    '//*[@id="company-top"]/div[2]/div[2]/div[3]/div[2]/span[3]/a[1]').text
                                item['gsxxResultList'][0]['entScope'] = self.driver.find_element_by_xpath(
                                    '//*[@id="Cominfo"]/table[2]/tbody/tr[11]/td[2]').text

                                # 变更记录
                                tr_list = self.driver.find_element_by_id('Changelist').find_elements_by_tag_name('tr')[1:]
                                for tr in tr_list:
                                    bg_dict = {}
                                    bg_dict['bgNo'] = tr.find_element_by_xpath('td[1]').text
                                    bg_dict['bgDate'] = tr.find_element_by_xpath('td[2]').text
                                    bg_dict['bgpri'] = tr.find_element_by_xpath('td[3]').text
                                    bg_dict['bgBefore'] = tr.find_element_by_xpath('td[4]').text
                                    bg_dict['bgLater'] = tr.find_element_by_xpath('td[5]').text
                                    item['bgjlResultList'].append(bg_dict)
                                if item['entFddbr'] not in duplicate_entFddr:
                                    result_data.append(item)
                                    duplicate_entFddr.append(item['entFddbr'])
                                self.driver.close()  # 关闭当前窗口
                            except (
                            NoSuchElementException, TimeoutException, NoSuchElementException, WebDriverException,
                            ElementNotVisibleException, ElementNotSelectableException, BaseException) as e:
                                logging.error(msg=e)
                                self.driver.close()
                                continue
                            finally:
                                self.driver.switch_to.window(all_handles_detail[0])
                self.driver.quit()
                return json.dumps({'result': result_data})
            else:
                self.driver.quit()
                return json.dumps({'result': result_data})
        except (NoSuchElementException, TimeoutException, NoSuchElementException, WebDriverException,
                            ElementNotVisibleException, ElementNotSelectableException, BaseException) as e:
            logging.error(msg=e)
            self.driver.quit()
        finally:
            self.driver.quit()

    def run(self):
        return self._main()


if __name__ == '__main__':
    Sspider(addr='广州市天河区五山路').run()