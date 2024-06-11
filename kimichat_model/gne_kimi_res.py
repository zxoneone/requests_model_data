# -*- coding: utf-8 -*-
import requests
import json
# from .kimi_token import ensure_access_token, tokens, refresh_access_token,HEADERS

import time
from functools import wraps

def retry(max_attempts=5, delay_seconds=1, exceptions=(Exception,), retry_on_empty=True):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < max_attempts:
                try:
                    result = func(*args, **kwargs)
                    if retry_on_empty and not result:
                        raise ValueError("Empty result, retrying...")
                    return result
                except exceptions as e:
                    print(f"Attempt {attempts + 1}/{max_attempts} failed: {e}")
                except ValueError as ve:
                    print(ve)

                if attempts < max_attempts - 1:
                    time.sleep(delay_seconds)
                else:
                    print("All attempts failed.")
                attempts += 1

        return wrapper

    return decorator




def get_kimi_response(key,content,chat_id):
    # chat_id='coljlu4udu6fjld0lrg0'
    # chat_id=create_new_chat_session()
    print('当前chat_id',chat_id)
    api_url = f"https://kimi.moonshot.cn/api/chat/{chat_id}/completion/stream"

    data={
        "messages": [
            {
                "role": "user",
                "content": ""
            }
        ],
        "refs": [],
        "use_search": False
    }
    # 请求载荷
    messages=[
            {
                "role": "user",
                "content": content
            }
        ]
    payload = {
        "messages": messages,
        "refs": [],
        "use_search": False,
        "temperature": 0.3
    }

    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://kimi.moonshot.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 '
                      'Safari/537.36',
        'Authorization':f'Bearer {key}'
    }
    # post流失请求
    with requests.post(api_url, json=payload, headers=headers, stream=True) as response:
        try:
            # 迭代处理每行响应数据
            n = 1
            for line in response.iter_lines():
                if line:
                    # print(line)
                    decoded_line = line.decode('utf-8')
                    # print(decoded_line)
                    # 检查行是否包含有效的数据
                    if decoded_line.startswith('data: '):
                        json_str = decoded_line.split('data: ', 1)[1]
                        try:
                            json_obj = json.loads(json_str)
                            if 'text' in json_obj and json_obj.get('event') == 'cmpl':  # 检查 'event' 字段的值是否为 'cmpl'
                                # 构造 JSON 对象
                                response_json = {
                                    "choices": [
                                        {
                                            "index": 0,
                                            "delta": {
                                                "content": json_obj['text'],
                                                "role": "assistant"
                                            }
                                        }
                                    ],

                                }
                                yield response_json
                                # print(new_chat)
                            # elif 'text' in json_obj and json_obj.get('event') == 'rename':
                            #     # 检查 'event' 字段的值是否为 'rename'
                            #     # print("标记")
                            #
                            #     # print(json_obj['text'])
                            #

                            elif json_obj.get('event') == 'search_plus':  # 检查 'event' 字段的值是否为 'search_plus'
                                msg = json_obj.get('msg', {})
                                title = msg.get('title')
                                url = msg.get('url')

                                if title and url:  # 如果 'msg' 字段包含 'title' 和 'url'
                                    link = f'[{title}]({url})'
                                    content = f"找到了第{n}篇资料：{link}\n"
                                    n += 1
                                    response_json = {
                                        "choices": [
                                            {
                                                "index": 0,
                                                "delta": {
                                                    "content": content,
                                                    "role": "assistant"
                                                }
                                            }
                                        ],
                                    }
                                    yield response_json
                                response_json = {
                                    "choices": [
                                        {
                                            "index": 0,
                                            "delta": {
                                                "content": "\n",
                                                "role": "assistant"
                                            }
                                        }
                                    ],
                                }
                                yield response_json

                        except json.JSONDecodeError:
                            pass

                    # 检查数据流是否结束
                if '"event":"all_done"' in decoded_line:
                    break

        except requests.exceptions.ChunkedEncodingError as e:
            pass

# '''
# def get_token_key(key):
#     headers = {
#         'Accept': '*/*',
#         'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
#         'Content-Type': 'application/json; charset=UTF-8',
#         'Origin': 'https://kimi.moonshot.cn',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
#          'Authorization':f'Bearer {key}'
#     }
#
#     res=requests.get('https://kimi.moonshot.cn/api/auth/token/refresh', headers=headers).json()
#     return res['refresh_token']
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzI1ODgzMywiaWF0IjoxNzEzMjU3OTMzLCJqdGkiOiJjb2Yzcmo5a3FxNHR0cm4wZTJsZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNubnNjNGlsbmw5M2JjcW9jNTlnIiwic3BhY2VfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU5MCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU4ZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.z-5Qr7AkZ55KNGAD_OWGae-xCxvANJ8zan6SCl-d__Uo-klwECspWdz3oi89_d3Y0rSFYkvTasVFSdX3rytyGQ'

# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzI2MzU0NSwiaWF0IjoxNzEzMjYyNjQ1LCJqdGkiOiJjb2Y1MGQ5a3FxNG44aWo3bTQ2MCIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNubnNjNGlsbmw5M2JjcW9jNTlnIiwic3BhY2VfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU5MCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU4ZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.c9z64hGxLvohjwGt6cvKfUDelMy7ioqeUe2-QekTmkFTKW96v0gGbtGBBNUZTrSlAsnrTrcLlfsOzX2DkXhC1Q'
# key=  'eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzI2Mzk4NCwiaWF0IjoxNzEzMjYzMDg0LCJqdGkiOiJjb2Y1M3Ixa3FxNHR0cmhjdTNrMCIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNubnNjNGlsbmw5M2JjcW9jNTlnIiwic3BhY2VfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU5MCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU4ZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.uWS21sy2OoiY2HhV_SYmKcpMwN9WL2EkTK59fsRBXazuTWM20Wi2CkC6T_3PGbQ0bEvSfXnEpQkkUXsFzcGo4A'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzI2NTE4MCwiaWF0IjoxNzEzMjY0MjgwLCJqdGkiOiJjb2Y1ZDYxa3FxNG44aWpvdmI4ZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNubnNjNGlsbmw5M2JjcW9jNTlnIiwic3BhY2VfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU5MCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU4ZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.hnLz2s8vXjan_HqQAke1dsQE-LBcSRZyJLPameaPj5-kUIPLbzb-rLRTs2PAMsKCP-Y-FnKYxff-bRxX9Zms4Q'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzgzOTM1NCwiaWF0IjoxNzEzODM4NDU0LCJqdGkiOiJjb2poaXRoa3FxNHUwNDBjbDRzMCIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.0PHgslhN9_ZDIHWjL0fMPzIN_N-uJBFAx5oFOYN9vCSGu5X3fHQVJjuPc8EfoTds41QH1BSH5j_orXQ85ZT3dg'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzg0MjQ3OSwiaWF0IjoxNzEzODQxNTc5LCJqdGkiOiJjb2ppYmFwa3FxNGhhdTAzYjBoZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.YhtXNorRzlS8V9PkEuVlurNyH654kzIrHjfCGWn4HEr2s4OrCWcJ-L-HLH_ra0Y0aql-wTdaDtleIxnInAsCUgeyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzg0MjU4NSwiaWF0IjoxNzEzODQxNjg1LCJqdGkiOiJjb2ppYzU5a3FxNHUwNDJlNnVyMCIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.DLV-8qONsR3kmb8auh8JxeI_mHZ4qfRcH3nmnd8BfKNQrIlUF9NP1zzE6kK30Sqv9pF4y3ifwEuCAGH1rZNxhg'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzg0MjcwNywiaWF0IjoxNzEzODQxODA3LCJqdGkiOiJjb2ppZDNwa3FxNGhhdTA3czZxZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.wx7h86emkEDhRgX8V8W1Teo4_IuTDLYM11m0BUumrbl855dQCwJ9Dc4Sj-9fiMRSMeZJ_c6CSpMiwUbrMjT-RQ'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzg0Mzk3OCwiaWF0IjoxNzEzODQzMDc4LCJqdGkiOiJjb2ppbjFoa3FxNHUwNDM5bTFwMCIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.jivsjd4eft1voL_Nh35WG6X7nTmK5gCwtjXAC-8Ky1hUEZmOoA3AtidECqr-RY2leSvFtGxqdYQvk3orZscM5Q'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzg1MTcyNSwiaWF0IjoxNzEzODUwODI1LCJqdGkiOiJjb2pramk5a3FxNHUwNDV2NDBxMCIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.lHGDLR_s44-N7IuwH5s-YLXxU3dqhjwPdtOCIumIXWHuT238GPMk_bTqKMnfcZF6kdFjcNQxC9ZdsF3rAgKeaweyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzg1MTgxMSwiaWF0IjoxNzEzODUwOTExLCJqdGkiOiJjb2prazdwa3FxNGhhdTNuNGFkZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.1QHwG_QURdjloxDIZ6HPN3IPZHI2z8E59rIGQ6gBmgYVVf2Know75bjDEF43WjkHE3A-JuBGGs-3AiNXXCo7VQ'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzg1MTk4NiwiaWF0IjoxNzEzODUxMDg2LCJqdGkiOiJjb2prbGpoa3FxNHUwNDYyb2xoZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.NJM_FGZm52tFKqlaNKeT2XYdunJtObYdsfLrm2Te_HfiDVI0ZvFc33EqtP2aYTF4l8Akixd3mjGgvOgycTidJA'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzg2MjYzMywiaWF0IjoxNzEzODYxNzMzLCJqdGkiOiJjb2puOHA5a3FxNGhhdTJvcG1uMCIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.35HyF5se5qYedJAtGRsmh7mMQGtQ4H0XepaVdYeegQcVyw95AQy73KrHKYdOxmt1lTHEhBkYdj8jZJpPfErPiA'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyMTYzODA5NiwiaWF0IjoxNzEzODYyMDk2LCJqdGkiOiJjb2puYmsxa3FxNHUwNDVhYzhqZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjbm9qcGI0dWR1NjZrYjFyMGszZyIsInNwYWNlX2lkIjoiY25vanBiNHVkdTY2a2IxcjBrMzAiLCJhYnN0cmFjdF91c2VyX2lkIjoiY25vanBiNHVkdTY2a2IxcjBrMmcifQ.8C5UZMYIXRgq3F1Rq1nzSZrvBd_AoMqOHylcZ9OeX6W__feQhCFdxbMdEeGliLaRP_28nEWvPAQgdCHfvuO_sw'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzg2Mjk5NiwiaWF0IjoxNzEzODYyMDk2LCJqdGkiOiJjb2puYmsxa3FxNHUwNDVhY2g5MCIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.-gevttyX5tNXInLOSRtiYBs41ed0mwoiVCZk14ydIgB1pfqfhe3fecicFrw6dlf2Rl-GDGh_o3bUu3ZdT4Mbtg'
# key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxMzg2NDA5NCwiaWF0IjoxNzEzODYzMTk0LCJqdGkiOiJjb2puazZoa3FxNGhhdTNvMzUyZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNub2pwYjR1ZHU2NmtiMXIwazNnIiwic3BhY2VfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGszMCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm9qcGI0dWR1NjZrYjFyMGsyZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.VjNXDJIszN387bT9l9ahLbzlqgxBOnMlKslYIHe6UXVya5azfR2Mlxa7DXoRSiNIypbeIEHM1XnOyNiciDu5kw'
# @retry(max_attempts=5, delay_seconds=2, exceptions=(Exception, ValueError))
def merge_word(key,content,chat_id):
    '''

    :param key: access_token
    :param content: prompt
    :param chat_id: 当前会话ID
    :return: model返回的流失输出拼接的最终output
    '''


    try:


        res=get_kimi_response(key,content,chat_id)
        print(res)
        words=''
        for i in res:
            print(i,type(i))
            if 'choices' in i:
                words+=i['choices'][0]['delta']['content']


        print('words',words)

        return words
    except Exception as e :
        print('accesstoken 无效，请重新获取')

# print(merge_word(key,content))
