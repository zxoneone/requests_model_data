import requests

HEADERS = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
    'Content-Type': 'application/json; charset=UTF-8',
    'Origin': 'https://kimi.moonshot.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
}


def get_token_key(key):
    #增加重试请求机制
    headers= {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
        'Content-Type': 'application/json; charset=UTF-8',
        'Origin': 'https://kimi.moonshot.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
         'Authorization':f'Bearer {key}',
        # 'Cookie':'Hm_lvt_358cae4815e85d48f7e8ab7f3680a74b=1710999788; _ga=GA1.1.1245915597.1710999788; Hm_lpvt_358cae4815e85d48f7e8ab7f3680a74b=1713255983; _ga_YXD8W70SZP=GS1.1.1713253123.71.1.1713257950.0.0.0'
    }

    res=requests.get('https://kimi.moonshot.cn/api/auth/token/refresh', headers=headers).json()

    # print('accsess_token',res['access_token'])
    return res['refresh_token'],res['access_token']




def create_new_chat_session(tokens):
    """
    发送POST请求以创建新的聊天会话。
    :return: 如果请求成功，返回会话ID；如果失败，返回None。
    """
    # 从全局tokens变量中获取access_token
    # auth_token ='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxNDExNDk2NCwiaWF0IjoxNzE0MTE0MDY0LCJqdGkiOiJjb2xrczQydG5uMHF0MzM4dW5tZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNubnNjNGlsbmw5M2JjcW9jNTlnIiwic3BhY2VfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU5MCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU4ZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.j8NOlViY2EPbEsMq7nlSU2SoNPYX14kYVTdBD8aZNYzKA_jyz9kUqxPYiK7GFq5X2BQKr_oGAUlsZ5Te96JJSw'
    # auth_token='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxNDExNDk2NCwiaWF0IjoxNzE0MTE0MDY0LCJqdGkiOiJjb2xrczQydG5uMHF0MzM4dW5tZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNubnNjNGlsbmw5M2JjcW9jNTlnIiwic3BhY2VfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU5MCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU4ZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.j8NOlViY2EPbEsMq7nlSU2SoNPYX14kYVTdBD8aZNYzKA_jyz9kUqxPYiK7GFq5X2BQKr_oGAUlsZ5Te96JJSw'
    auth_token=tokens
    # 复制请求头并添加Authorization字段
    headers = HEADERS.copy()
    headers['Authorization'] = f'Bearer {auth_token}'

    # 定义请求的载荷
    payload = {
        "name": "未命名会话",
        "is_example": False
    }

    # 发送POST请求
    response = requests.post('https://kimi.moonshot.cn/api/chat', json=payload, headers=headers)
    print(response.json())

    # 检查响应状态码并处理响应
    if response.status_code == 200:
        # logger.debug("[KimiChat] 新建会话ID操作成功！")
        print('ID:',response.json().get('id'))
        return response.json().get('id')  # 返回会话ID
    else:
        # logger.error(f"[KimiChat] 新建会话ID失败，状态码：{response.status_code}")
        return None
#
# chat_key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxNDExNDk2NCwiaWF0IjoxNzE0MTE0MDY0LCJqdGkiOiJjb2xrczQydG5uMHF0MzM4dW5tZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNubnNjNGlsbmw5M2JjcW9jNTlnIiwic3BhY2VfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU5MCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU4ZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.j8NOlViY2EPbEsMq7nlSU2SoNPYX14kYVTdBD8aZNYzKA_jyz9kUqxPYiK7GFq5X2BQKr_oGAUlsZ5Te96JJSw'
# key="eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyMTg4NjA3MywiaWF0IjoxNzE0MTEwMDczLCJqdGkiOiJjb2xqc3VhdWw3MjI3dHNiaDdwMCIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjbm9qcGI0dWR1NjZrYjFyMGszZyIsInNwYWNlX2lkIjoiY25vanBiNHVkdTY2a2IxcjBrMzAiLCJhYnN0cmFjdF91c2VyX2lkIjoiY25vanBiNHVkdTY2a2IxcjBrMmcifQ.LaUhg4e-ACxKx-UKXtT3zBnAafRkkMfP4aCp90U4q3fIiOrKF8dbfBBebzjmBzrlljcb7-s3ef5YwJP52hBDZQ"
# # access_key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxNDExMDEyNywiaWF0IjoxNzE0MTA5MjI3LCJqdGkiOiJjb2xqbWFxdWw3MjI3dHM2aG9oZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNubnNjNGlsbmw5M2JjcW9jNTlnIiwic3BhY2VfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU5MCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU4ZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.yV1X48H4vllc7Tm5yZXbQe_NHfJrK_QSf2F5APKeI2lk8iDwB_r-_X1IEFZYmMYLXoCGMaR1WbnzET5frZgB7A'
# # access_key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcxNDExMDEyNywiaWF0IjoxNzE0MTA5MjI3LCJqdGkiOiJjb2xqbWFxdWw3MjI3dHM2aG9oZyIsInR5cCI6ImFjY2VzcyIsInN1YiI6ImNubnNjNGlsbmw5M2JjcW9jNTlnIiwic3BhY2VfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU5MCIsImFic3RyYWN0X3VzZXJfaWQiOiJjbm5zYzRpbG5sOTNiY3FvYzU4ZyIsInJvbGVzIjpbImZsYXNoX2NhdGNoZXJfZ29vZF91c2VyIl19.yV1X48H4vllc7Tm5yZXbQe_NHfJrK_QSf2F5APKeI2lk8iDwB_r-_X1IEFZYmMYLXoCGMaR1WbnzET5frZgB7A'

# merge_word(access_key,'哈哈哈哈哈 谢谢你愿意陪我聊天')
