from fastapi import FastAPI,HTTPException
from kimichat_model.gne_kimi_res import merge_word
from kimichat_model.refresh_kimi import get_token_key,create_new_chat_session
from glm_model.glm4_api import get_glm_response
from functools import wraps
import time
from fastapi import FastAPI, File, UploadFile, Response
from fastapi.responses import HTMLResponse
import shutil
import logging
import uvicorn

# 配置日志记录器
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)




app = FastAPI()


RETRY_LIMIT=3
RETRY_DELAY=2
refresh_key='eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJ1c2VyLWNlbnRlciIsImV4cCI6MTcyNDU3ODUxNSwiaWF0IjoxNzE2ODAyNTE1LCJqdGkiOiJjcGE1N2twcDJrMTIycjVoNW5tZyIsInR5cCI6InJlZnJlc2giLCJzdWIiOiJjb2FmNmkxa3FxNHY0dWt2cXNpZyIsInNwYWNlX2lkIjoiY29hZjZpMWtxcTR2NHVrdnFzaTAiLCJhYnN0cmFjdF91c2VyX2lkIjoiY29hZjZpMWtxcTR2NHVrdnFzaGcifQ.pYrUd_bXQyp25G_Yx2QA3EU_ehPF96aGGEgpFhLZUBOtTrsYLVZlc7kW6vgTQ6_Yshko4HMWB8zzyybp1122Gg'

from logging.handlers import RotatingFileHandler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(funcName)s - %(lineno)d - %(message)s')
# 创建一个日志文件handler，用于写入日志文件，并设置最大文件大小和备份文件数量
log_file_path = r"model_log\app.log"
max_log_size = 1000 * 1024 * 1024  # 1000MB
backup_count = 5  # 保留5个备份文件
rotating_file_handler = RotatingFileHandler(log_file_path, maxBytes=max_log_size, backupCount=backup_count)
rotating_file_handler.setLevel(logging.INFO)
rotating_file_handler.setFormatter(formatter)

# 添加handler到logger
logger.addHandler(rotating_file_handler)

def retry_if_empty(retry_limit: int = 3, delay: int = 2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < retry_limit:
                result = func(*args, **kwargs)
                if result["message"]:  # 假设函数返回的结果是output
                    return result
                attempts += 1
                logger.warning("操作失败，正在重试... 尝试次数：{}".format(attempts))  # 重试警告
                time.sleep(delay)  # 等待一段时间后重试
            logger.error("达到最大重试次数，操作失败。")
            # 如果重试次数达到限制，结果仍然为空，则返回空结果
            return None
        return wrapper
    return decorator

@app.get("/")
async def root():

    return {"message": "OK"}


@app.get("/hello")
@retry_if_empty()
def get_model_res(model:str,prompt: str,chat_id:str):
    global refresh_key
    try:
        if model.lower()=='kimi':
            print('Okk')
            refresh_key, key = get_token_key(refresh_key)
            if not chat_id:
                chat_id = create_new_chat_session(key)
                print(chat_id)


            output = merge_word(key, prompt, chat_id)
            # return {"message": f"Hello {output}  nice too meet you ","model":'kimi'}
        elif model.lower()=='glm-4':
            print('GLM4')
            output = get_glm_response(prompt,
                                      'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTcxNTA2NjQyMywianRpIjoiNTc2MWVmYzEtMDNkNC00NzRmLTg3ZWItMzlkYmZiYWExZGEyIiwidHlwZSI6InJlZnJlc2giLCJzdWIiOiI3MDZlODc2NTEwMzI0Y2QwODlhM2JlZTkwNmY1N2E2ZiIsIm5iZiI6MTcxNTA2NjQyMywiZXhwIjoxNzMwNjE4NDIzLCJ1aWQiOiI2NGVmZTc0NDM3MGVjMWM4NzgwNDI3NjUiLCJ1cGxhdGZvcm0iOiIiLCJyb2xlcyI6WyJ1bmF1dGhlZF91c2VyIl19.IEMvBxl8iQGv7RjHTMdorQOKXY9faUyGqVPafH6-7NA	')
            print('output:', output)
        logger.info(f"模型 {model} 响应生成成功，当前input:{prompt},'输出output：{output}")
        return {"message":output,"model":model,'chat_id':chat_id}
    except Exception as e:
        logger.exception("请求处理异常：")
        return {"message":"","model":"error"}

@app.get("/model/id")
def get_model_chat_id(model:str)->dict:
    global refresh_key
    if model.lower()=='kimi':
        refresh_key, key = get_token_key(refresh_key)
        chat_id = create_new_chat_session(key)
        return {'chat_id':chat_id}

    elif model.lower()=='glm-4':
        pass


if __name__ == "__main__":
    # uvicorn.run(app, host="127.0.0.1", port=8000)
    pass