# -*- coding: utf-8 -*-
'''
    selenium 登录猪八戒，定时刷新cookie，更新存入redis
'''

import redis
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.common.exceptions import TimeoutException
from zbjCookie.log import Logger
from PIL import Image
from io import BytesIO
import time
import json


logger = Logger(filename='./log/cookie.log')


class LoginAndGetCookies:

    def __init__(self):
        self._BORDER = 6
        self._redis_conn = redis.Redis(host='xxx.xxx.xxx.xxx', port=6379, db=0)
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }
        self._chrome_driver_path = 'xxxxxxxxxxxxxxxxxxxxxxxxx'
        self._options = webdriver.ChromeOptions()
        self._options.add_argument('--headless')
        self._options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36')
        self._options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self._options.add_argument("--start-maximized")
        self._browser = webdriver.Chrome(options=self._options)
        self._wait = WebDriverWait(self._browser, 10)
        self._captcha_wait = WebDriverWait(self._browser, 4)

    def _open(self):
        """
        打开网页
        :param url:
        :return:
        """
        self._browser.get('https://account.zbj.com/login')

    def _open_js(self):
        js_open_window = 'window.open("https://account.zbj.com/login");'
        self._browser.execute_script(js_open_window)

    def _close(self):
        """
        关闭网页
        :return:
        """
        self._browser.close()
        self._browser.quit()

    def _is_the_picture_loaded(self):
        """
        验证码图片是否加载完成
        :return:
        """
        self._captcha_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.geetest_ant')))

    def _get_slider_button(self):
        """
        获取滑块
        :return: 滑块对象
        """
        button = self._captcha_wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'geetest_slider_button')))
        return button

    def _get_position(self):
        """
        获取验证码位置
        :return: 位置元组
        """
        img = self._captcha_wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.geetest_canvas_img.geetest_absolute')))
        time.sleep(0.5)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size['width']
        return top, bottom, left, right

    def _get_screenshots(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshots = self._browser.get_screenshot_as_png()
        self._browser.save_screenshot("./images/overall_page.png")
        screenshots = Image.open(BytesIO(screenshots))
        return screenshots

    def _get_geetest_image(self, name='captcha.png'):
        """
        获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self._get_position()
        screenshots = self._get_screenshots()
        captcha = screenshots.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def delete_style(self):
        """
        执行js脚本，获取无滑块图
        :return None
        """
        js = 'document.querySelectorAll("canvas")[2].style=""'
        self._browser.execute_script(js)

    def _is_pixel_equal(self, img1, img2, x, y):
        """
        判断两个像素是否相同
        :param img1: 不带缺口图片
        :param img2: 带缺口图
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同
        """
        # 取两个图片的像素点
        pix1 = img1.load()[x, y]
        pix2 = img2.load()[x, y]
        threshold = 60
        if abs(pix1[0] - pix2[0]) < threshold and abs(pix1[1] - pix2[1]) < threshold and abs(
                pix1[2] - pix2[2]) < threshold:
            return True
        else:
            return False

    def _get_gap(self, img1, img2):
        """
        获取缺口偏移量
        :param img1: 不带缺口图片
        :param img2: 带缺口图
        :return 缺口位置
        """
        left = 70
        for i in range(left, img1.size[0]):
            for j in range(img1.size[1]):
                if not self._is_pixel_equal(img1, img2, i, j):
                    left = i
                    return left
        return left

    def _get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 3 / 5
        # 计算间隔
        t = 0.2
        # 初速度
        v = 0
        # 滑超过过一段距离
        distance += 10
        while current < distance:
            if current < mid:
                # 加速度为正
                a = 1
            else:
                # 加速度为负
                a = -0.5
            # 初速度 v0
            v0 = v
            # 当前速度 v
            v = v0 + a * t
            # 移动距离 move-->x
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def _shake_mouse(self):
        """
        模拟人手释放鼠标时的抖动
        :return: None
        """
        ActionChains(self._browser).move_by_offset(xoffset=-2, yoffset=0).perform()
        ActionChains(self._browser).move_by_offset(xoffset=2, yoffset=0).perform()

    def _move_to_gap(self, slider, tracks):
        """
        拖动滑块到缺口处
        :param slider: 滑块
        :param tracks: 轨迹
        :return
        """
        back_tracks = [-1, -1, -2, -2, -1, -2, -1]
        ActionChains(self._browser).click_and_hold(slider).perform()
        # 正向
        for x in tracks:
            ActionChains(self._browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.3)
        # 逆向
        for x in back_tracks:
            ActionChains(self._browser).move_by_offset(xoffset=x, yoffset=0).perform()
        # 模拟抖动
        self._shake_mouse()
        time.sleep(0.5)
        ActionChains(self._browser).release().perform()

    def _get_cookies_and_hset_redis(self, username):
        # print('[get_cookie] 正在获取Cookie :(')
        cookies = self._browser.get_cookies()
        new_cookies_dict = dict()
        for cookie in cookies:
            new_cookies_dict[cookie['name']] = cookie['value']
        # print('[get_cookie] 已获取 :)')
        new_cookies_json = json.dumps(new_cookies_dict)
        # print('[hset_redis] 正在更新redis :(')
        self._redis_conn.hset(username, 'cookie', new_cookies_json)
        self._redis_conn.hset(username, 'updateTimestamp', int(time.time()))  # 更新时间
        self._redis_conn.hset(username, 'usedStatus', '0')  # 使用状态
        self._redis_conn.hset(username, 'isUsingStatus', '0')  # 正在使用状态
        # print('[hset_redis] 完成更新 :)')
        logger.info('[redis] updated cookie.')

    def _refresh(self):
        """
        刷新验证码/页面
        :return:
        """
        # 因刷新太多次验证码图片
        time.sleep(0.2)
        text = self._browser.find_element_by_xpath('//*[@class="geetest_radar_tip"][1]').get_attribute('aria-label')
        if text == '网络不给力':  # 点击重试
            self._browser.find_element_by_xpath('//*[@id="password-captcha-box"]/div[2]/div[2]/div[1]/div[3]/span[2]').click()
            logger.warning('[refresh] refresh page.')
            return True

    def _crack(self, reset=False):
        """
        滑动
        :param reset: 重置
        :return:
        """
        try:
            if not reset:
                self._browser.find_element_by_xpath('//*[@class="geetest_wait"]').click()
                try:  # 不出现滑动验证码的情况下
                    success = self._captcha_wait.until(
                        EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功')
                    )
                    if success:
                        return True
                except TimeoutException as e:
                    pass
            else:
                if not self._refresh():  # 已点击重试，可以继续验证
                    self._browser.find_element_by_class_name('geetest_refresh_1').click()  # 若重新调用，刷新滑块图片
                else:time.sleep(2)
            slider = self._get_slider_button()
            # 获取带缺口的验证码图片
            image1 = self._get_geetest_image('./images/captcha1.png')
            self.delete_style()
            image2 = self._get_geetest_image('./images/captcha2.png')
            gap = self._get_gap(image1, image2)
            gap -= self._BORDER
            track = self._get_track(gap)
            self._move_to_gap(slider, track)
            time.sleep(2)
            try:
                success = self._captcha_wait.until(
                    EC.text_to_be_present_in_element((By.CLASS_NAME, 'geetest_success_radar_tip_content'), '验证成功')
                )
            except TimeoutException as e:
                return False
            if success:
                # print('[crack] 滑动成功 :)')
                return True
            else:return False
        except BaseException as e:
            pass

    def _login(self, username):
        """
        首页登录
        :return:
        """
        logger.info("[updating {}'s cookie]".format(username))
        time.sleep(2)
        try:
            self._captcha_wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, 'geetest_logo')))  # 判断登录页面是否完全加载
        except:
            logger.error('[login] css not loaded and refresh page now.')
            self._browser.refresh()
        self._browser.find_element_by_xpath('//*[@id="username"]').clear()
        self._browser.find_element_by_xpath('//*[@id="password"]').clear()
        self._browser.find_element_by_xpath('//*[@id="username"]').send_keys(username)
        self._browser.find_element_by_xpath('//*[@id="password"]').send_keys('wr1234')
        time.sleep(2)
        success = self._crack()
        crack_number = 1
        while not success:
            if success:
                logger.warning('[crack] sliding success and get cookie now.')
                # print('[crack] 滑动成功，开始获取Cookie :)')
                break
            else:
                logger.warning('[crack] sliding fail and reboot.')
                # print('[crack] 滑动失败，重新滑动 :(')
                crack_number += 1
                success = self._crack(reset=True)
            if crack_number > 9:
                # 验证大于8次，重调
                logger.warning('[crack] over-validation and page refresh')
                self._login(username)
                break
        self._browser.find_element_by_css_selector('.zbj-btn.zbj-btn-primary.j-login-btn.linear-gradient-btn').click()
        time.sleep(1)
        self._get_cookies_and_hset_redis(username=str(username))  # 以手机号为键
        logger.info('------------:)------------')
        time.sleep(1)

    def run(self, username):
        try:
            if len(self._browser.window_handles) > 1:
                self._open_js()
                self._login(username)
            else:
                self._open()
                self._login(username)
        except BaseException as e:
            pass
        finally:
            self._browser.close()
            self._browser.quit()


def all_cookie(u_data):
    """
    更新全部cookie
    :param u_data:
    :return:
    """
    instance = LoginAndGetCookies
    for u in u_data:
        instance().run(u)


def single_cookie(u):
    """
    更新单个cookie
    :param u:
    :return:
    """
    instance = LoginAndGetCookies
    instance().run(u)


if __name__ == '__main__':
    pass