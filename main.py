from datetime import datetime
import pickle
import time
import requests
import cart
import sys
import cookiemaker


class ABC:
    def __init__(self):
        sys.stdout.write(f"\rA-RT ver 0.0.4\n")
        sys.stdout.flush()
        data = '''                       @@@@@@@@@
                       @@@@@@@@@
                       @@@@@@@@@                   @@@@@@@@@@@     @@@@@@@@@@@@@
                       @@@@@@@@@                   @@@@@@@@@@@@    @@@@@@@@@@@@@
                       @@@@@@@@@                   @@@@@@@@@@@@@   @@@@@@@@@@@@@
                       @@@@@@@@@                     @@@@  @@@@@   @@@ @@@@@ @@@
                       @@@$@@@@@                     @@@@   @@@@   @@  @@@@@  @@
                      @@@@ @@@@@@                    @@@@   @@@@   @@  @@@@@  @@
                      @@@* *@@@@@      -@@@@@@!      @@@@  @@@@        @@@@@
                      @@@; ;@@@@@      -@@@@@@!      @@@@@@@@@         @@@@@
                      @@@@@@@@@@@      ,@@@@@@!      @@@@@@@@          @@@@@
                     @@@@@@@@@@@@@                   @@@@#@@@@         @@@@@
                     @@@@@@@@@@@@@                   @@@@  @@@@        @@@@@
                     @@@:   ;@@@@@                   @@@@  @@@@        @@@@@
                    @@@@.   ,@@@@@@                  @@@@   @@@@       @@@@@
                    @@@@-, .-@@@@@@                @@@@@@@  @@@@@     @@@@@@@
                  @@@@@@@; ;#@@@@@@@               @@@@@@@  @@@@@     @@@@@@@
                  @@@@@@@; ;@@@@@@@@               @@@@@@@  @@@@@     @@@@@@@
                  @@@@@@@; :@@@@@@@@                                     
                  @@@@@@@; ;@@@@@@@@                          AIO by Peaches                                    
                                                                     '''
        for i in data.split("\n"):
            print(i)
            time.sleep(0.1)


        sys.stdout.write(f"\r네이버 계정 검증 시작\n")
        sys.stdout.flush()
        self.navercookie = self.cookie()
        sys.stdout.write(f"\r네이버 계정 검증 완료\n")
        sys.stdout.flush()

    def cookie(self):
        return cookiemaker.Cookiemake().naver_cookie()

    def job_start(self, data):
        cart.ABCCART().run(data, self.navercookie)

    def save(self, data):
        pickle.dump(data, open(f'_internal/dclp.dll', 'wb'), pickle.HIGHEST_PROTOCOL)

    def load(self):
        return pickle.load(open(f'_internal/dclp.dll', 'rb'))


    def mypage(self, data):
        header, cookie = cart.ABCCART().login(data, "https://m.grandstage.a-rt.com/")
        req = requests.get('https://m.grandstage.a-rt.com/member/member-barcode-info', headers=header)
        event = requests.get("https://m.grandstage.a-rt.com/promotion/event/list?statusType=ing")
        for i in event.json()["eventList"]:
            if "출석체크" in i["eventName"]:
                eventNo = i["eventNo"]
                break
        data = f"eventNo={eventNo}&memberNo={req.json()['memberInfo']['memberNo']}&eventTypeCode=10002&mktUseAgreeYn=N&chkSaveID=&smsRecvYn=N&emailRecvYn=N&nightSmsRecvYn=N&quizAnswer=&surveyNo="
        requests.post('https://m.grandstage.a-rt.com/promotion/event/attend/check/member/save', headers=header, data=data)

        return req.json()["memberInfo"]['memberName']


    def run(self):
        while True:
            while True:
                id = input("A-RT ID:")
                pw = input("A-RT PW:")
                try:
                    name = self.mypage({"ID": id, "PW": pw})
                    sys.stdout.write(f"\r{name}님 A-RT AIO에 오신것을 환영합니다.\n")
                    sys.stdout.flush()
                    break
                except:
                    print("\n계정을 다시 확인해주세요.")
            while True:
                session = input("원하는 작업을 입력해주세요.\n1 온라인 선착순 구매:")
                if session == "1":
                    product_code = input("URL:")
                    size = input("SIZE:")
                    Pay = input("NaverPay Password:")
                    Point = input("A-RT포인트 사용 유무(사용시 1 미사용시 0):")
                    while True:
                        timer = input("실행 예약(ex:20240131 095800\n.입력시 바로 시작):")
                        if timer == ".":
                            break

                        try:
                            inputtime = datetime.strptime(timer, '%Y%m%d %H%M%S')
                            while True:
                                sys.stdout.write(f"\r{datetime.now().strftime('%Y%m%d %H%M%S')}")
                                sys.stdout.flush()
                                if datetime.now() >= inputtime:
                                    break
                            break
                        except:
                            print("\n시간 양식을 맞춰 다시 입력해주세요.")

                    data = {
                        "ID": id,
                        "PW": pw,
                        "product_code": product_code,
                        "size": size,
                        "Pay": Pay,
                        "Point": Point
                    }
                    self.job_start(data)


ABC().run()
