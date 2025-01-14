from fastapi import FastAPI, HTTPException
import uvicorn
from fastapi import FastAPI
import requests
import textwrap

app = FastAPI()


@app.post("/ai/id_card")
async def id_card(url: str):
    try:
        prompt = """
            提取身份证中以下内容的文本信息,无法提取的内容默认为空：
            姓名
            性别
            民族
            出生日期
            住址
            身份证号
            """
        request_url = (
            "http://127.0.0.1:50010/ai/prompt?url=" + url + "&prompt=" + prompt
        )
        response = requests.post(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/ai/train_ticket")
async def train_ticket(url: str):
    return ocr_train_ticket(url)


def ocr_train_ticket(url: str):
    try:
        request_url = "http://127.0.0.1:50013/predict_kie?image_url=" + url
        response = requests.post(request_url)
        response.raise_for_status()
        json_result = response.json()
        return textwrap.dedent(
            f"""
            车票号：{json_result.get("ticketNum")}
            始发站：{json_result.get("startingStation")}
            车次号：{json_result.get("trainNum")}
            到达站：{json_result.get("destinationStation")}
            出发日期：{json_result.get("date")}
            座位号：{json_result.get("seatNum")}
            车票金额：{json_result.get("ticketRates")}
            席别：{json_result.get("seatCategory")}
            乘客姓名：{json_result.get("name")}
            身份证号：{json_result.get("id_num")}
            序列号：{json_result.get("serial_number")}
            时间：{json_result.get("time")}
            """
        ).strip()
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


def llm_train_ticket(url: str):
    try:
        prompt = """
            提取火车票中以下内容的文本信息,无法提取的内容默认为空：
            车票号
            始发站
            车次号
            到达站
            出发日期
            座位号
            车票金额
            席别 
            乘客姓名
            身份证号
            售站
            序列号
            时间
            """
        request_url = (
            "http://127.0.0.1:50010/ai/prompt?url=" + url + "&prompt=" + prompt
        )
        response = requests.post(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@app.post("/ai/invoice")
async def invoice(url: str):
    try:
        prompt = """
            提取发票中以下内容的文本信息,无法提取的内容默认为空：
            发票名称
            发票代码
            发票号码
            开票日期
            密码区
            收款人
            复核
            开票人
            购买方名称
            购买方纳税人识别号
            购买方地址、电话
            购买方开户行及账号
            销售方名称
            销售方纳税人识别号
            销售方地址、电话
            销售方开户行及账号
            货物或应税劳务、服务名称
            货物或应税劳务、服务金额
            货物或应税劳务、服务税率
            货物或应税劳务、服务税额
            金额合计
            税额合计
            价税合计(大写)
            价税合计(小写)
            """
        request_url = (
            "http://127.0.0.1:50010/ai/prompt?url=" + url + "&prompt=" + prompt
        )
        response = requests.post(request_url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=50011)
