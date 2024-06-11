# -*- coding: utf-8 -*-

#以xlsx文件为请求示例
import pandas as pd
import requests

filepath=r'C:\Users\51976\Desktop\work_task\6月\prompt_test.xlsx'
outfilepath='prompt_test(alone).xlsx'
MODEL='KIMI'
CHAT_ID=''
chat_params = {'model': MODEL}
# CHAT_ID = requests.get(f"http://127.0.0.1:8000/model/id", params=chat_params).json()['chat_id']



df=pd.read_excel(filepath)

#单轮请求
def process_item(prompt,model,chat_id):
    '''

    :param prompt: 需要请求的问题
    :param model: 所选模型
    :param chat_id: 会话ID为空则为单轮，此外为多轮请求
    :return:
    '''
    params = {'model': model,
              "prompt": prompt,
              'chat_id': chat_id}
    res=requests.get(f"http://127.0.0.1:8000/hello", params=params).json()

    return res



data_list=[]

for index,row in list(df.iterrows())[1:]:

    prompt=row['A']
    print(prompt)


    #单轮请求

    output=process_item(prompt,MODEL,CHAT_ID)
    print(output)
    data_list.append((prompt,output))
    filtered_df = pd.DataFrame(data_list, columns=['input', 'output'])
    filtered_df.to_excel(outfilepath,index=False)



#问题query,model，model_key，单多轮请求，
#单论chat_id每轮更新，多单轮chat_id不变

