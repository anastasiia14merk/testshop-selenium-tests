class BasePage:
    base_url = 'http://testshop.qa-practice.com/'
    page_url = None
    def __init__(self, driver):
        self.driver = driver

    def open(self):
        if self.page_url:
            self.driver.get(f'{self.base_url}{self.page_url}')
        else:
            raise NotImplementedError('Page can not be opened for this page class')