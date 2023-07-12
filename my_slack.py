# 파이썬에서 슬랙으로 텍스트 메시지 보내기 입니다.
import requests
import json
from config import get_secret


class Slack_Msg():
    def __init__(self, msg):
        self.msg = msg
        self.sendmsg()

    def sendmsg(self):
        web_hook_url = get_secret("web_hook_url")
        sendmsg = self.msg
        slack_msg = {'text': sendmsg}
        requests.post(web_hook_url, data=json.dumps(slack_msg))


if __name__ == "__main__":
    
    my_msg = '''
    안녕하세요.
    2023년 7월 12일(수) 테스트 문자를 발송합니다.
    ----------------------------------
    안전지수 : 20점 (전사 평균대비 +3점)
    주요 키워드 : 샤클(5), 하부(2)
    ==================================
    감사합니다.    
    '''
    
    Slack_Msg(my_msg)