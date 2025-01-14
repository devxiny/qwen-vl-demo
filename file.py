from fastapi import FastAPI
import uvicorn
from datetime import datetime
import os
import shutil
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

# 配置静态文件服务
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    # 确保images目录存在
    os.makedirs("images", exist_ok=True)

    # 生成唯一的文件名
    file_name = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
    file_path = f"images/{file_name}"

    # 保存上传的文件
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 构建并返回图片URL
    image_url = f"http://10.18.5.116:50012/images/{file_name}"
    return {"url": image_url}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=50012)
