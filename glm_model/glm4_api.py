from glm_model.refresh_glm import get_new_token
import requests
import json


chat_id = 'col1n6alnl9bclnu9d4g'
# chat_id=create_new_chat_session()
print('chat_id', chat_id)
# api_url = f"https://kimi.moonshot.cn/api/chat/{chat_id}/completion/stream"
api_url='https://chatglm.cn/chatglm/backend-api/assistant/stream'




#     "assistant_id": "65940acff94777010aa6b796",
#     "conversation_id": "662e0702b1dd07b80843d2e3",
#     "meta_data": {
#         "mention_conversation_id": "",
#         "is_test": false,
#         "input_question_type": "xxxx",
#         "channel": "",
#         "draft_id": ""
#     },
#     "messages": [
#         {
#             "role": "user",
#             "content": [
#                 {
#                     "type": "text",
#                     "text": "哈哈哈哈哈 是嘛"
#                 }
#             ]
#         }
#     ]
# }









# key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDAzMzI2NSwianRpIjoiZWYxNWJjZjEtNmNjNS00NjUzLWI4NTItOTdmM2VlYTMzMjg3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImE5NTY3MDZmN2JhZjRmYWE4YjcyNmVmMGRkODY0ZDAzIiwibmJmIjoxNzE0MDMzMjY1LCJleHAiOjE3MTQxMTk2NjUsInVpZCI6IjY0ZjdmYTNjZGQ0N2VkOTAwYWU5NGUyMiIsInVwbGF0Zm9ybSI6IiIsInJvbGVzIjpbInVuYXV0aGVkX3VzZXIiXX0.7emZJe8pGCQu6IpYsoOO59HPr_OrADoea601EsKkAC4'

# key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDI5MjQ1MiwianRpIjoiMGI4NGI0N2YtYzRjZS00YzA3LWFlNDgtM2FhOTMwMzE5OGU3IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImE5NTY3MDZmN2JhZjRmYWE4YjcyNmVmMGRkODY0ZDAzIiwibmJmIjoxNzE0MjkyNDUyLCJleHAiOjE3MTQzNzg4NTIsInVpZCI6IjY0ZjdmYTNjZGQ0N2VkOTAwYWU5NGUyMiIsInVwbGF0Zm9ybSI6IiIsInJvbGVzIjpbInVuYXV0aGVkX3VzZXIiXX0.LCKZarblMJTqJvcV3N0zrgrWceYwdUqRDd7Ohcr8VCw'
# key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDM4MTE1MywianRpIjoiMjZhZWRmODktMzk0ZS00OGM0LWIxZGMtN2Q0OGRkYjcxODY5IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImE5NTY3MDZmN2JhZjRmYWE4YjcyNmVmMGRkODY0ZDAzIiwibmJmIjoxNzE0MzgxMTUzLCJleHAiOjE3MTQ0Njc1NTMsInVpZCI6IjY0ZjdmYTNjZGQ0N2VkOTAwYWU5NGUyMiIsInVwbGF0Zm9ybSI6IiIsInJvbGVzIjpbInVuYXV0aGVkX3VzZXIiXX0.7NIDeZFi9BIFJekF6pP2vq9-MgStTIKmEj9m-OTX2ho'
# key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDQ2Nzc5MiwianRpIjoiN2U1ZjZiNzMtOGY3Mi00YzU5LThhYTAtMjQ1MWVlNjY4NjQ2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImE5NTY3MDZmN2JhZjRmYWE4YjcyNmVmMGRkODY0ZDAzIiwibmJmIjoxNzE0NDY3NzkyLCJleHAiOjE3MTQ1NTQxOTIsInVpZCI6IjY0ZjdmYTNjZGQ0N2VkOTAwYWU5NGUyMiIsInVwbGF0Zm9ybSI6IiIsInJvbGVzIjpbInVuYXV0aGVkX3VzZXIiXX0.uActTIQIdzUtWYtJXtCbf9jm1xsgMw6mnQNOl5GqxBQ'
key='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDgxOTk0NywianRpIjoiNjZhZmE3YmEtMjgxZi00NGVlLTlkMWYtNDlmOGE5NTViNzNhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImE5NTY3MDZmN2JhZjRmYWE4YjcyNmVmMGRkODY0ZDAzIiwibmJmIjoxNzE0ODE5OTQ3LCJleHAiOjE3MTQ5MDYzNDcsInVpZCI6IjY0ZjdmYTNjZGQ0N2VkOTAwYWU5NGUyMiIsInVwbGF0Zm9ybSI6IiIsInJvbGVzIjpbInVuYXV0aGVkX3VzZXIiXX0.SahqBeJZuSZPFo6IuPsOt23RKtXgSPgSydf1mYzvEQM'

def get_glm_response(prompt,key):
    try:
    # global key
        key=get_new_token(key)
        headers = {
            'Accept': '*/*',
            'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
            'Content-Type': 'application/json; charset=UTF-8',

            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 '
                          'Safari/537.36',
            'Authorization': f'Bearer {key}'
        }

        data = {
            "assistant_id": "65940acff94777010aa6b796",
            "conversation_id": "",
            "meta_data": {
                "mention_conversation_id": "",
                "is_test": 'False',
                "input_question_type": "xxxx",
                "channel": "",
                "draft_id": ""
            },
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        }
        # 以流的方式发起POST请求
        # res=requests.post(api_url,json=data,headers=headers,stream=False,).text
        # res.encode('utf-8')
        # print(res)
        with requests.post(api_url, json=data, headers=headers, stream=True) as response:

                # 迭代处理每行响应数据
                n = 1
                for line in response.iter_lines():
                    if line:


                        decoded_line = line.decode('utf-8')
                        # print(decoded_line)
                        if decoded_line.startswith('data: '):
                            json_str = decoded_line.split('data: ', 1)[1]
                            print('json_str:',json_str)
                            try:
                                json_obj = json.loads(json_str)
                                if 'parts' in json_obj and json_obj.get('status') == 'finish':  # 检查 'event' 字段的值是否为 'cmpl'
                                    # 构造 JSON 对象
                                    print('已进入',json_obj['parts'])
                                    print(json_obj,type(json_obj))
                                    print('为',json_obj['parts'][0]['content'][0]['text'])
                                    return json_obj['parts'][0]['content'][0]['text']

                            except Exception as e:
                                return ''

    except Exception as e:
        return ''
    # return res
def get_new_token3():

    url='https://chatglm.cn/chatglm/backend-api/v1/user/refresh'
    headers={'Authorization':'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNDQ3MjY1MywianRpIjoiZGFjZmYzMjYtYTQwNS00OWE1LWFhODgtYzBhZTM2N2VjZjgwIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiIzZTZlZjEzMGNiYTQ0YWQ2YWZjYTBhYjRkMTVkMDRiYSIsIm5iZiI6MTcxNDQ3MjY1MywiZXhwIjoxNzMwMDI0NjUzLCJ1aWQiOiI2NjMwYzZjYzgwOGYwMGZjMmQ5ZjE1N2UiLCJ1cGxhdGZvcm0iOiJwYyIsInJvbGVzIjpbInVuYXV0aGVkX3VzZXIiXX0.vM1YuGePIN3xEyz-nFUH1KR-GJDUtb4lJ-cjW_TMZjY'
    }



    data={}
    res=requests.post(url=url,headers=headers).json()
    print(res)
    return res['result']['accessToken']

def get_glm_response3(prompt):

    key=get_new_token3()
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh-HK;q=0.9,zh;q=0.8',
        'Content-Type': 'application/json; charset=UTF-8',

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 '
                      'Safari/537.36',
        'Authorization': f'Bearer {key}'
    }

    data = {
        "assistant_id": "65940acff94777010aa6b796",
        "conversation_id": "",
        "meta_data": {
            "mention_conversation_id": "",
            "is_test": 'False',
            "input_question_type": "xxxx",
            "channel": "",
            "draft_id": ""
        },
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ]
    }
    # 以流的方式发起POST请求
    # res=requests.post(api_url,json=data,headers=headers,stream=False,).text
    # res.encode('utf-8')
    # print(res)
    with requests.post(api_url, json=data, headers=headers, stream=True) as response:

            # 迭代处理每行响应数据
            n = 1
            for line in response.iter_lines():
                if line:


                    decoded_line = line.decode('utf-8')
                    # print(decoded_line)
                    if decoded_line.startswith('data: '):
                        json_str = decoded_line.split('data: ', 1)[1]
                        print('json_str:',json_str)
                        try:
                            json_obj = json.loads(json_str)
                            if 'parts' in json_obj and json_obj.get('status') == 'finish':
                                # 构造 JSON 对象
                                print('已进入',json_obj['parts'])
                                print(json_obj,type(json_obj))
                                print('为',json_obj['parts'][0]['content'][0]['text'])
                                return json_obj['parts'][0]['content'][0]['text']
                                # response_json = {
                                #     "choices": [
                                #         {
                                #             "index": 0,
                                #             "delta": {
                                #                 "content": json_obj['parts'][0]['content'][0]['text'],
                                #                 "role": "assistant"
                                #             }
                                #
                                #         }
                                #     ],
                                #
                                # }
                                # print('content是',response_json['choices'][0]['content'])
                                # # yield response_json
                                # yield response_json
                        except Exception as e:
                            return ''

def extract_text_from_stream(stream_output):
    def extract_text_from_stream(stream_output):
        last_text = None
        for line in stream_output.split('\n'):
            if line.strip().startswith('data:'):
                data = line.strip()[5:]
                try:
                    event = json.loads(data)
                    if event.get('status') == 'finish' and event.get('data'):
                        parts = event['data'].get('parts')
                        if parts:
                            last_part = parts[-1]
                            if last_part.get('content'):
                                text = last_part['content'][0].get('text')
                                if text:
                                    last_text = text
                except json.decoder.JSONDecodeError:
                    continue
        return last_text


# cnt=0
# while cnt<=0:
#     t=get_kimi_response(key)
#     print('结果为',t)
#     cnt+=1
    # data=extract_text_from_stream(t)
    # for i in t:
    #     print('i',i['choices'][0]['content'])
    # print('cnt',cnt)
    # print('data',t)
    # cnt+=1
