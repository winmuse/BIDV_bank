import io, os, time
import json
import pyautogui
# from google.cloud import vision
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from winreg import *

class AutoDownloadBIDVbank:
    def __init__(self, user_name, pass_word):
        self.user_name = user_name
        self.pass_word = pass_word

        # self.excel_file_name = "TPbank_Account_Statement.xlsx"
        # with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
        #     self.dir_download = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0] + "\\"
        # self.dir_sample_input = os.getcwd() + "\\sample input\\"

        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

        self.runDownload()

    def timeoutToken(self,):
        while True:
            element = '//*[@id="btn-step1"]/button[2]'
    def loadCompleted(self, locator, timeout):
        """ check website load complete """
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, locator))
            )
            return True
        except TimeoutException:
            return False

    def clickElement(self, xpath_element):
        """ find element on website then click """
        try:
            if self.loadCompleted(xpath_element, 50):
                element = self.driver.find_element(By.XPATH, xpath_element)
                element.click()

        except NoSuchElementException:
            print("can not find element:", xpath_element)
        except Exception:
            print("can not click try perform ")
            time.sleep(10)
            # ex_element = WebDriverWait(self.driver, 30).until(
            #     EC.visibility_of_element_located((By.XPATH, xpath_element)))
            ex_element = self.driver.find_element(By.XPATH, xpath_element)
            ActionChains(self.driver).click(ex_element).perform()

    def click_select_date(self, id_btn):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.ID, id_btn)))
            down_arrow_btn = self.driver.find_element(By.ID, id_btn)
            down_arrow_btn.click()
            print("click:" + id_btn)
        except Exception:
            print("can't find %s, try run javaScript" % id_btn)


    # Login to BIDVbank
    def loginBIDVbank(self):
        try:
            self.driver.get("https://smartbanking.bidv.com.vn/dang-nhap")
            # captcha = self.get_captcha()
            user_ele = "/html/body/div[1]/div[1]/div[2]/div/div[2]/app-dang-nhap/div/div/div/form/div[2]/div[1]/div/div[1]/input"
            self.clickElement(user_ele)
            user = self.driver.find_element(By.XPATH,user_ele)
            user.clear()
            password = self.driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div[2]/div/div[2]/app-dang-nhap/div/div/div/form/div[2]/div[2]/div/div[1]/app-password/input")
            password.clear()
            # captcha_input = self.driver.find_element(By.CSS_SELECTOR, "input[formControlName=captcha]")
            #button = self.driver.find_element(By.XPATH, "")

            user.send_keys(self.user_name)
            password.send_keys(self.pass_word)
            # captcha_input.send_keys(captcha)
            #button.click()

            #first login...
            
                
        except TimeoutException:
            print("Login TPbank timeout")
            time.sleep(5)
            return
        except:
            time.sleep(10)
            print("has been login TPbank - can't find element")

    def runDownload(self):
        """ start download TPbank Transaction """
        self.loginBIDVbank()
        
        first_login_element = '/html/body/div/div[1]/div[2]/div/div[1]/div[3]/div[1]/div/div/div[1]/div/div[2]/a/span'
        if self.loadCompleted(first_login_element,2000000):
            self.clickElement('/html/body/div[1]/div[1]/div[2]/div/div[1]/div[3]/div[1]/div/div/div[1]/div/div[2]/a/span')

        print("login success")

        xpath_element = '/html/body/div/div[1]/div[2]/div/app-tai-khoan/div/div[2]/div/div/div/div/div[2]/div/ul/li/div/a/div/div[2]/div[2]'
        # total_amount = WebDriverWait(self.driver, 20).until(
        #     EC.visibility_of_element_located((By.XPATH, xpath_element))).text
        with open('extract_data.txt', mode='w', encoding='utf-8') as log_file:
            log_file.write(' ' + '\n')
        if self.loadCompleted(xpath_element,2000000):
            total_amount = WebDriverWait(self.driver, 20).until(EC.visibility_of_element_located((By.XPATH, xpath_element))).text
            print("total amount", total_amount)
            with open('extract_data.txt', mode='a', encoding='utf-8') as log_file:
                log_file.write(total_amount + '\n')
            self.clickElement(xpath_element)
                    
        xpath_element = '/html/body/div/div[1]/div[2]/div/app-chi-tiet-tai-khoan/div[2]/div/div[2]/div/div[2]/div/div[1]/div[1]'
        if self.loadCompleted(xpath_element,2000000):
            all_transaction = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[2]/div/app-chi-tiet-tai-khoan/div[2]/div/div[2]/div/div[2]/div/div[1]/div[1]')
            html_content = all_transaction.get_attribute("innerHTML")

            # Print the HTML content
            print(html_content)
            each = all_transaction.find_elements(By.CLASS_NAME, 'list-line-item')
  
            table_data = []
            

            for row in each:
        #     ActionChains(self.driver).click(row).perform()
        #     time.sleep(4)
                col = row.find_element(By.CLASS_NAME, 'col')
                txt_sub = col.find_element(By.CLASS_NAME, 'txt-sub').text
                print("txt_sub ",txt_sub)
                time_data = col.find_element(By.CLASS_NAME, 'ml5').text
                print("ml5 ",time_data)
                txt_main = col.find_element(By.CLASS_NAME, 'txt-main').text
                print("txt_main ",txt_main)


                col_auto = row.find_element(By.CLASS_NAME, 'col-auto')
                txt_sub1 = col_auto.find_element(By.CLASS_NAME, 'txt-sub').text
                print("txt_sub1 ",txt_sub1)
                txt_main1 = col_auto.find_element(By.CLASS_NAME, 'txt-main').text
                print("txt_main1 ",txt_main1)
                
                with open('extract_data.txt', mode='a', encoding='utf-8') as log_file:
                    log_file.write(txt_sub+ ' ' + time_data + ' ' + txt_main + ' ' + txt_sub1 + ' ' + txt_main1 + '\n')

        #     modal_content = modal.find_element(By.CLASS_NAME, 'content')
        #     modal_transaction_info = modal_content.find_element(By.CLASS_NAME, 'transaction-info')
        #     info_tran = modal_transaction_info.find_elements(By.CLASS_NAME,'line-right')
        #     data = [tran_text.text for tran_text in info_tran]
        #     table_data.append(data)
            
        #     with open('extract_data.txt', mode='a', encoding='utf-8') as log_file:
        #         log_file.write(' '.join(data) + '\n')
        #     close_btn = '/html/body/app-root/main-component/div/div[2]/div/div/div[1]/div/app-account-transaction/div/div/div[2]/app-acc-trans-search/div[1]/app-modal[1]/div/div/div/div/div[1]/img'
        #     self.clickElement(close_btn)
        #     transaction_info = '/html/body/app-root/main-component/div/div[2]/div/div/div[1]/div/app-account-transaction/div/div/div[2]/app-acc-trans-search/div[1]/app-modal[1]/div/div/div/div/div[4]'
        #     print(data)
        #     print('----------------------------------')
        # log_file.close()
        time.sleep(30)
        self.runDownload()
        # self.driver.quit()

    def isLoginError(self):
        xpath_element = '//*[@id="maincontent"]/ng-component/div[1]/div/div[3]/div/div/div/app-login-form/div/div/div[4]/p'
        login_error = WebDriverWait(self.driver, 20).until(
            EC.visibility_of_element_located((By.XPATH, xpath_element))).text
        print("login_error", login_error)

        if login_error == 'Mã kiểm tra không chính xác. Quý khách vui lòng kiểm tra lại.':
            return True
        return False

if __name__ == "__main__":
    file_name = f'.\\setting.json'
    with open(file_name) as file:
        info = json.load(file)
    AutoDownloadBIDVbank(info['USER_NAME'],info['PASSWORD'])