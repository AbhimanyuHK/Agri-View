from datetime import datetime, timedelta

import requests


class HttpClient:

    def __init__(self):
        self.yesterday_dt = datetime.now() - timedelta(days=1)
        self.yesterday = self.__dt_to_str__(self.yesterday_dt)

    def __update_date_to_day_back__(self, days=1):
        self.yesterday_dt = self.yesterday_dt - timedelta(days=days)
        self.yesterday = self.__dt_to_str__(self.yesterday_dt)

    @classmethod
    def __dt_to_str__(cls, yesterday_dt):
        return yesterday_dt.strftime("%Y-%m-%d")

    def data_list(self, state_name=None, ):
        cookies = {
            'SERVERID': 'node1',
            '_ga': 'GA1.3.268957160.1709265770',
            '_gid': 'GA1.3.1119279184.1709265770',
            'uniqueCode': '20240615498',
            'privacyPolicyAccepted': 'true',
            'ci_session': 'ps266jbhlsq21tk8ebf3n3idd4h9msqn',
            '_gat_gtag_UA_128172535_1': '1',
        }

        headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'Cookie': 'SERVERID=node1; _ga=GA1.3.268957160.1709265770; _gid=GA1.3.1119279184.1709265770; uniqueCode=20240615498; privacyPolicyAccepted=true; ci_session=ps266jbhlsq21tk8ebf3n3idd4h9msqn; _gat_gtag_UA_128172535_1=1',
            'Origin': 'https://enam.gov.in',
            'Referer': 'https://enam.gov.in/web/dashboard/trade-data',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
            'X-Requested-With': 'XMLHttpRequest',
            'dnt': '1',
        }

        data = {
            'language': 'en',
            'stateName': state_name or '-- All --',
            'apmcName': '-- Select APMCs --',
            'commodityName': '-- Select Commodity --',
            'fromDate': self.yesterday,
            'toDate': self.yesterday,
        }

        for x in range(7):
            try:
                response = requests.post(
                    'https://enam.gov.in/web/Ajax_ctrl/trade_data_list', cookies=cookies, headers=headers, data=data
                )
                data = response.json()["data"]

                return data
            except Exception as exception:
                print(exception)
                if x == 6:
                    raise exception
