import requests
from requests.exceptions import RequestException
import time


def get_new_token(key):
    url = 'https://chatglm.cn/chatglm/backend-api/v1/user/refresh'
    headers = {
        'Authorization': f'Bearer {key}',
        'Accept': 'application/json',

    }

    max_retries = 3
    retry_delay = 2  # 重试间隔时间，单位为秒

    for attempt in range(max_retries):
        try:
            response = requests.post(url=url, headers=headers)
            response.raise_for_status()  # 将触发HTTP错误
            return response.json()['result']['accessToken']
        except RequestException as e:
            print(f"请求失败，正在尝试第{attempt + 1}次重试: {e}")
            time.sleep(retry_delay)
        except KeyError:
            print("响应JSON中缺少预期的键")
            break

    print('重试次数已用完，请求token无效.')
    return None

