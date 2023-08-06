import sys
import time
from qrunner.utils.log import logger
from qrunner.core.android.driver import AndroidDriver
from qrunner.core.android.element import AndroidElement
from qrunner.core.ios.driver import IosDriver
from qrunner.core.ios.element import IosElement
from qrunner.core.web.driver import WebDriver
from qrunner.core.web.element import WebElement
from qrunner.core.h5.driver import H5Driver
from typing import Union


class Page(object):
    """页面基类，用于pom模式封装"""

    url = None

    def __init__(self, driver: Union[AndroidDriver, IosDriver,
                                     WebDriver, H5Driver]):
        self.driver = driver

    @staticmethod
    def sleep(n):
        """休眠"""
        logger.info(f'休眠 {n} 秒')
        time.sleep(n)

    def open(self):
        """打开页面"""
        try:
            self.driver.open_url(self.url)
        except Exception as e:
            logger.error(f'请设置页面url: {str(e)}')
            sys.exit()

    def elem(self, **kwargs):
        """页面元素封装"""
        if isinstance(self.driver, AndroidDriver):
            return AndroidElement(**kwargs)
        elif isinstance(self.driver, WebDriver):
            return WebElement(**kwargs)
        elif isinstance(self.driver, IosDriver):
            return IosElement(**kwargs)

    def assertText(self, expect_value, timeout=5):
        """断言页面包含文本"""
        for _ in range(timeout + 1):
            try:
                page_source = self.driver.get_page_content()
                logger.info(f'断言: {page_source}\n包含 {expect_value}')
                assert expect_value in page_source, f'页面内容不包含 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            page_source = self.driver.get_page_content()
            logger.info(f'断言: {page_source}\n包含 {expect_value}')
            assert expect_value in page_source, f'页面内容不包含 {expect_value}'

    def assertNotText(self, expect_value, timeout=5):
        """断言页面不包含文本"""
        for _ in range(timeout + 1):
            try:
                page_source = self.driver.get_page_content()
                logger.info(f'断言: {page_source}\n不包含 {expect_value}')
                assert expect_value not in page_source, f'页面内容不包含 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            page_source = self.driver.get_page_content()
            logger.info(f'断言: {page_source}\n不包含 {expect_value}')
            assert expect_value not in page_source, f'页面内容仍然包含 {expect_value}'

    def assertElement(self, timeout=5, **kwargs):
        """断言元素存在"""
        for _ in range(timeout + 1):
            try:
                flag = self.elem(**kwargs).exists()
                logger.info(f'断言: 元素 {kwargs} 存在结果为 {flag}')
                assert flag, f'元素 {kwargs} 不存在'
                break
            except AssertionError:
                time.sleep(1)
        else:
            flag = self.elem(**kwargs).exists()
            logger.info(f'断言: 元素 {kwargs} 存在结果为 {flag}')
            assert flag, f'元素 {kwargs} 不存在'

    def assertNotElement(self, timeout=5, **kwargs):
        """断言元素不存在"""
        for _ in range(timeout + 1):
            try:
                flag = self.elem(**kwargs).exists()
                logger.info(f'断言: 元素 {kwargs} 存在结果为 {flag}')
                assert not flag, f'元素 {kwargs} 仍然存在'
                break
            except AssertionError:
                time.sleep(1)
        else:
            flag = self.elem(**kwargs).exists()
            logger.info(f'断言: 元素 {kwargs} 存在结果为 {flag}')
            assert not flag, f'元素 {kwargs} 仍然存在'

    def assertTitle(self, expect_value=None, timeout=5):
        """断言页面标题等于"""
        for _ in range(timeout + 1):
            try:
                title = self.driver.get_title()
                logger.info(f'断言: 页面标题 {title} 等于 {expect_value}')
                assert expect_value == title, f'页面标题 {title} 不等于 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            title = self.driver.get_title()
            logger.info(f'断言: 页面标题 {title} 等于 {expect_value}')
            assert expect_value == title, f'页面标题 {title} 不等于 {expect_value}'

    def assertInTitle(self, expect_value=None, timeout=5):
        """断言页面标题包含"""
        for _ in range(timeout + 1):
            try:
                title = self.driver.get_title()
                logger.info(f'断言: 页面标题 {title} 包含 {expect_value}')
                assert expect_value in title, f'页面标题 {title} 不包含 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            title = self.driver.get_title()
            logger.info(f'断言: 页面标题 {title} 包含 {expect_value}')
            assert expect_value in title, f'页面标题 {title} 不包含 {expect_value}'

    def assertUrl(self, expect_value=None, timeout=5):
        """断言页面url等于"""
        for _ in range(timeout + 1):
            try:
                url = self.driver.get_url()
                logger.info(f'断言: 页面url {url} 等于 {expect_value}')
                assert expect_value == url, f'页面url {url} 不等于 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            url = self.driver.get_url()
            logger.info(f'断言: 页面url {url} 等于 {expect_value}')
            assert expect_value == url, f'页面url {url} 不等于 {expect_value}'

    def assertInUrl(self, expect_value=None, timeout=5):
        """断言页面url包含"""
        for _ in range(timeout + 1):
            try:
                url = self.driver.get_url()
                logger.info(f'断言: 页面url {url} 包含 {expect_value}')
                assert expect_value in url, f'页面url {url} 不包含 {expect_value}'
                break
            except AssertionError:
                time.sleep(1)
        else:
            url = self.driver.get_url()
            logger.info(f'断言: 页面url {url} 包含 {expect_value}')
            assert expect_value in url, f'页面url {url} 不包含 {expect_value}'

    def assertAlertText(self, expect_value):
        """断言弹窗文本"""
        alert_text = self.driver.get_alert_text()
        logger.info(f'断言: 弹窗文本 {alert_text} 等于 {expect_value}')
        assert expect_value == alert_text, f'弹窗文本 {alert_text} 等于 {expect_value}'

