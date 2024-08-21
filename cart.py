import time
import cv2
import numpy as np
import pytesseract
from PIL import Image
from bs4 import BeautifulSoup
import requests
import json
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


class ABCCART:
    def __init__(self):
        self.driver = None

    def url_setting(self, url):
        return url.split("prdtNo=")[-1]

    def login(self, data, urls):
        req = requests.get(urls+"login")
        JSESSIONID = str(req.cookies).split("JSESSIONID=")[-1].split(" for")[0]
        WMONID = str(req.cookies).split("WMONID=")[-1].split(" for")[0]
        header = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) ApplewebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148APP_IOS_F",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Cookie": f"JSESSIONID={JSESSIONID}; " f"WMONID={WMONID}; fappVerTextArt=1.0.12",
        }
        url = f"{urls}login/login-processing"
        try:
            checkSrAd = BeautifulSoup(req.text, "html.parser").find("input", {"name":"checkSrAd"})["value"]
            data = f'loginType=member&returnUrl=%2F&checkSrAd={checkSrAd}&username={data["ID"]}&password={data["PW"]}&refUrl=%2F'
        except:
            data = f'loginType=member&username={data["ID"]}&password={data["PW"]}'
        req = requests.post(url, data=data, headers=header)
        UID = str(req.cookies).split("UID=")[-1].split(" for")[0]
        header = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) ApplewebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148APP_IOS_F",
            "Accept-Language": "ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Connection": "keep-alive",
            "Cookie": f"JSESSIONID={JSESSIONID}; " f"WMONID={WMONID}; " f"UID={UID}; fappVerTextArt=1.0.12",
        }
        cookie = [
            {
                "name": "JSESSIONID",
                "value": JSESSIONID
             },
            {
                "name": "WMONID",
                "value": WMONID
             },
            {
                "name": "UID",
                "value": UID
             },

        ]
        return header, cookie

    def cart(self, product_info, header, data, urls):
        header["Content-Type"] = "application/json"
        url = f"{urls}cart/cart-add"
        data = json.dumps(
            {
                "cartType": "B",
                "prdtList": [
                    {
                        "prdtNo": int(product_info["prdtNo"]),
                        "prdtTypeCode": int(product_info["prdtTypeCode"]),
                        "prdtOptnNo": int(data["size"]),
                        "optnName": int(data["size"]),
                        "orderQty": "1",
                        "vndrNo": product_info["vndrNo"],
                        "chnnlNo": product_info["chnnlNo"],
                        "ctgrNo": product_info["stdrCtgrNo"],
                        "plndpNo": "",
                        "eventNo": "",
                        "cartType": "B",
                    }
                ],
                "dailyDlvyYn": "N",
            }
        )
        req = requests.post(url, data=data, headers=header)
        return req.json()

    def info(self, product_code, header, urls):
        url = f"{urls}product/info?prdtNo=" + product_code
        # print(product_code)
        req = requests.get(url, headers=header)
        return req.json()

    def wait_for(self, el_type, element):
        while True:
            try:
                if el_type == "ID":
                    self.driver.find_element(By.ID, element)
                elif el_type == "XPATH":
                    self.driver.find_element(By.XPATH, element)
                elif el_type == "NAME":
                    self.driver.find_element(By.NAME, element)
                elif el_type == "CLASS_NAME":
                    self.driver.find_element(By.CLASS_NAME, element)
                time.sleep(0.1)
            except:
                break

    def wait_for_second(self, el_type, element):
        num = 0
        while True:
            try:
                if el_type == "ID":
                    self.driver.find_element(By.ID, element)
                elif el_type == "XPATH":
                    self.driver.find_element(By.XPATH, element)
                elif el_type == "NAME":
                    self.driver.find_element(By.NAME, element)
                elif el_type == "CLASS_NAME":
                    self.driver.find_element(By.CLASS_NAME, element)
                return False
            except:
                if num == 100:
                    return True
                else:
                    num = num + 1
                    time.sleep(0.1)
                    pass

    def driver_setting(self):
        chrome_options = Options()
        chrome_options.add_argument("User-Agent=Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) ApplewebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148APP_IOS_F")
        # chrome_options.add_argument("headless")
        chrome_options.add_argument('log-level=3')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=chrome_options)
        driver.maximize_window()
        return driver


    def popup_close(self):
        handles = self.driver.window_handles
        size = len(handles)
        main_handle = self.driver.current_window_handle
        for x in range(size):
            if handles[x] != main_handle:
                self.driver.switch_to.window(handles[x])
                self.driver.close()
        self.driver.switch_to.window(main_handle)

    def automatic(self, urls, cart_url, cookie, naver_cookie, data, product_code, header):

        sys.stdout.write(f"\r네이버 계정 검증\n")
        sys.stdout.flush()
        self.driver = self.driver_setting()
        self.driver.get("https://new-m.pay.naver.com/historybenefit/home")
        self.driver.delete_all_cookies()
        for i in naver_cookie:
            self.driver.add_cookie(i)
        self.driver.get('https://new-m.pay.naver.com/historybenefit/home')
        self.driver.get(urls)
        self.driver.delete_all_cookies()
        for i in cookie:
            self.driver.add_cookie(i)
        sys.stdout.write(f"\r네이버페이 파워적립 활성화\n")
        sys.stdout.flush()
        self.driver.get('https://ad.search.naver.com/search.naver?where=ad&query=ABC%EB%A7%88%ED%8A%B8&bucketTest=AD-PWL-SITURL&bucket=1&x=0&y=0')
        self.driver.find_element(By.CLASS_NAME, "tit_wrap").click()

        while True:
            if len(self.driver.window_handles) != 1:
                self.popup_close()
                break

        sys.stdout.write(f"\r결제창 진입\n")
        sys.stdout.flush()
        self.driver.get(cart_url)
        action = ActionChains(self.driver)
        self.wait_for_second('XPATH', '//label[@for="applyAllpoint"]')
        while True:
            try:
                action.move_to_element(self.driver.find_element(By.ID, 'giftCardCertNum')).perform()
                break
            except:
                # print("안됨?")
                pass
        if str(data["Point"]) == "1":
            while True:
                try:
                    if '<input id="applyAllpoint" type="checkbox" disabled' in str(self.driver.page_source):
                        break
                    self.driver.find_element(By.XPATH, '//label[@for="applyAllpoint"]').click()
                    break
                except:
                    pass
        action.move_to_element(self.driver.find_element(By.ID, 'saveMainPayment')).perform()
        while True:
            try:
                self.driver.find_element(By.XPATH, '//label[@for="payment10004"]').click()
                break
            except:
                pass
        try:
            action.move_to_element(self.driver.find_element(By.CLASS_NAME, 'footer-notice')).perform()
        except:
            action.move_to_element(self.driver.find_element(By.CLASS_NAME, 'footer-company')).perform()
            pass
        self.driver.find_element(By.XPATH, '//label[@for="term1"]').click()
        self.driver.find_element(By.ID, "btnPayment").click()

        sys.stdout.write(f"\r네이버페이 결제 진행\n")
        sys.stdout.flush()
        self.naver_pay(urls, product_code, header, data)
        # "https://grandstage.a-rt.com/order/complete?orderNo=2024040844145"

        for i in range(5):
            try:
                if "complete" in self.driver.current_url:
                    sys.stdout.flush()
                    sys.stdout.write(f"\r구매 완료\n")
                    break
                else:
                    pass
            except:
                time.sleep(1)
        self.driver.close()
        self.driver.quit()


    def naver_pay(self, urls, product_code, header, data):
        while True:
            handles = self.driver.window_handles
            if 1 != len(handles):
                break
        main_handle = self.driver.current_window_handle
        self.driver.switch_to.window(self.driver.window_handles[-1])
        # time.sleep(1000)
        self.wait_for_second('XPATH', '//label[@for="card"]')
        action = ActionChains(self.driver)
        action.move_to_element(self.driver.find_element(By.CLASS_NAME, 'point_h')).perform()
        self.driver.find_element(By.XPATH, '//label[@for="card"]').click()
        try:
            self.driver.find_element(By.ID, 'f_s2').click()
            self.driver.find_element(By.XPATH, '//option[@value="03"]').click()
        except:
            pass
        action.move_to_element(self.driver.find_element(By.CLASS_NAME, 'footer')).perform()
        self.driver.find_element(By.CLASS_NAME, 'button_bottom').click()
        while True:
            if "authentication" in self.driver.current_url:
                break
            else:
                pass
        # self.driver.switch_to.window(self.driver.window_handles[-1])

        sys.stdout.write(f"\r결제 OCR 진행\n")
        sys.stdout.flush()
        imgname = str(time.time_ns()).split(".")[0]
        self.driver.save_screenshot(f'{imgname}.png')
        self.pay_key_orc(urls, product_code, header, data, imgname)
        self.driver.switch_to.window(main_handle)

    def pay_key_orc(self, urls, product_code, header, data, imgname):
        pytesseract.pytesseract.tesseract_cmd = r'_internal\Tesseract\tesseract.exe'
        image = cv2.imread(f'{imgname}.png')

        height, width = image.shape[:2]
        midpoint = height // 2

        mask_color = (255, 255, 255)  # Assuming white background
        upper_half_mask = np.full((midpoint, width, 3), mask_color, dtype=np.uint8)

        image[0:midpoint, :] = upper_half_mask

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
        invert = 255 - thresh
        custom_config = r'--oem 3 --psm 6'
        text_data = pytesseract.image_to_data(invert, config=custom_config, lang='eng+kor', output_type=pytesseract.Output.DICT)
        screenshot_image = Image.open(f'{imgname}.png')
        screenshot_size = screenshot_image.size
        viewport_size = self.driver.execute_script("return [window.innerWidth, window.innerHeight];")
        scale = screenshot_size[0] / viewport_size[0]
        for i in range(len(data["Pay"])):
            x, y = self.get_ocr_pos(text_data, data["Pay"][i])
            script = """
                var element = document.elementFromPoint(arguments[0], arguments[1]);
                if (element) {
                    element.click();
                }
            """
            if i == 5:
                self.check_stock(urls, product_code, header, data)
            self.driver.execute_script(script, x, y)

    def get_ocr_pos(self, text_data, num):
        target_number = str(num)
        for i, text in enumerate(text_data['text']):
            if text == target_number:
                x = text_data['left'][i] + text_data['width'][i] / 2
                y = text_data['top'][i] + text_data['height'][i] / 2
        return x, y

    def check_stock(self, urls, product_code, header, data):
        if "onthespot" in urls:
            url = "https://www.onthespot.co.kr/"
        elif "grandstage" in urls:
            url = "https://grandstage.a-rt.com/"
        else:
            url = "https://abcmart.a-rt.com/"
        url = f"{url}product/info?prdtNo=" + product_code
        stock = 0
        num = 0
        while True:
            req = requests.get(url, headers=header)
            for i in req.json()["productOption"]:
                if str(i["optnName"]) == data['size']:
                    stock = i["totalStockQty"]-i["totalOrderQty"]
                    break
            if num == 4:
                num = 1
            sys.stdout.write(f"\r재고 대기중{'.'*num}")
            sys.stdout.flush()
            num = num+1
            if stock>0:
                print(json.dumps(req.json(), ensure_ascii=False, indent=4))
                break
            else:
                time.sleep(0.2)

    def run(self, data, naver_cookie):
        sys.stdout.write(f"\r구매 시작\n")
        sys.stdout.flush()
        product_code = data["product_code"]
        if "onthespot" in product_code:
            product_code = self.url_setting(product_code)
            url = "https://m.onthespot.co.kr/"
        elif "grandstage" in product_code:
            product_code = self.url_setting(product_code)
            url = "https://m.grandstage.a-rt.com/"
        else:
            product_code = self.url_setting(product_code)
            url = "https://m.abcmart.a-rt.com/"

        sys.stdout.write(f"\rA-RT Login\n")
        sys.stdout.flush()
        header, cookie = self.login(data, url)
        sys.stdout.write(f"\r제품 정보 취득\n")
        sys.stdout.flush()
        product_info = self.info(product_code, header, url)
        sys.stdout.write(f"\r{product_info['prdtName']} {product_info['styleInfo']}\n")
        sys.stdout.flush()
        sys.stdout.write(f"\r장바구니 담기 시작\n")
        sys.stdout.flush()
        try:
            cart_info = self.cart(product_info, header, data, url)

            cart_url = f'{url}order?cartDeliveryType=D&cartSeq={cart_info["cartSeqs"][0]}&dailyDlvyYn=N'

            sys.stdout.write(f"\r장바구니 담기 완료\n")
            sys.stdout.flush()
        except:
            sys.stdout.write(f"\r장바구니를 비우고 다시 시작해주세요\n")
            sys.stdout.flush()
            return
        try:

            sys.stdout.write(f"\r구매 시작\n")
            sys.stdout.flush()
            self.automatic(url, cart_url, cookie, naver_cookie, data, product_code, header)

            sys.stdout.write(f"\r결제 완료\n")
            sys.stdout.flush()

        except Exception as E:
            sys.stdout.write(f"\r결제중 에러 발생\n"+str(E))
            sys.stdout.flush()
            self.driver.close()
            self.driver.quit()
