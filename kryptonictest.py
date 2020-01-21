import os
from subprocess import Popen, PIPE
import unittest
from selenium.webdriver import Firefox, FirefoxProfile
from selenium.webdriver.firefox.options import Options
# from config import Config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import logging as log
from pymongo import MongoClient

MONGO_URI = 'localhost:27017' # TODO: A centralized place for the mongouri, modifiable by config and options.py
MONGO_DB = 'untapt_krypton'

#TODO: Refactor method extentions to a new KryptonMethods class and use multiple inheritance to Krypton<driver> classes
class KryptonicFirefox(Firefox):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def wait_for_element(self, id=None, css_selector=None, class_name=None, xpath=None, link_text=None, timeout=20 ):
        if id:
            by = By.ID
            selector = id
        elif css_selector:
            by = By.CSS_SELECTOR
            selector = css_selector
        elif class_name:
            by = class_name
            selector = class_name
        elif xpath:
            by = By.XPATH
            selector = xpath
        elif link_text:
            by = By.LINK_TEXT
            selector = link_text
        else:
            raise ValueError("wait_for_element must use one kwarg of: css_selector, class_name, xpath, link_text")

        try:
            return WebDriverWait(self, timeout).until(EC.presence_of_element_located((by, selector)))
        except TimeoutException as ex:
            log.error(f'wait_for_element: Timeout while waiting for element {selector}')
            raise TimeoutException(f'wait_for_element: Timeout while waiting for element {selector}', ex.screen, ex.stacktrace)


class KryptonicTestCase(unittest.TestCase):

    config_options = Config().options

    @classmethod
    def setUpClass(cls):
        print(cls.__module__)

        for path, dirs, files in os.walk(f'./scenarios/{cls.__module__}'):
            if path[-8:] == '__data__':
                cls._runNodeWithDbAccess(path, 'preTest.js')


            print(path, dirs, files)

    @classmethod
    def _runNodeWithDbAccess(cls, path, file):
        pass

    def _buildFirefoxDriver(self, headless=False):
        profile = FirefoxProfile()
        profile.accept_untrusted_certs = True
        profile.headless = headless
        profile.set_preference('security.fileuri.strict_origin_policy', False)
        o = Options()
        o.set_headless(self.config_options['headless'])
        return KryptonFirefox(firefox_profile=profile, options=o)

    def _cleanupDbWrites(self):
        client = MongoClient(MONGO_URI)
        db = getattr(client, MONGO_DB)
        log.debug('Removing all documents with _kryptonData')
        for collection_name in db.collection_names():
            db[collection_name].remove({'_kryptonData': {'$exists': True}}, multi=True)



    def setUp(self):
        if os.path.exists(f'./scenarios/{self.__module__}/__data__/setUp.js'):
            log.debug('setUp.js hook detected')
            js = Popen(['node', f'./scenarios/{self.__module__}/__data__/setUp.js'])
            stdout, stderr = js.communicate()
            log.debug(f'{self.__module__}/__data__/setUp.js:{stdout}')


        self.url = self.config_options['url']
        self.cleanup = self.config_options['cleanup']
        self.driver = self._buildFirefoxDriver(headless=self.config_options['headless'])
        # print(self.__module__) TODO: this is the name that should be used with errors



    def tearDown(self):
        if self.config_options.get('cleanup_db_writes', 'always') == 'always':
            self._cleanupDbWrites()

        if self.config_options['cleanup'] == 'onfailure':
            # logic for test case
            pass
        elif self.config_options['cleanup'] == 'always':
            self.driver.quit()
