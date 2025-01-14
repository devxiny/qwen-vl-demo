import gradio as gr
import requests
from io import BytesIO

# 更新后的上传图片函数


def upload_image(image):
    # 将Gradio上传的图片转换为文件对象
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="png")
    img_byte_arr = img_byte_arr.getvalue()

    # 准备上传的文件
    files = {"file": ("image.png", img_byte_arr, "image/png")}

    try:
        # 发送POST请求到上传API
        response = requests.post("http://127.0.0.1:50012/upload", files=files)
        response.raise_for_status()  # 如果请求失败，这将抛出一个异常

        # 从响应中获取图片URL
        image_url = response.json()["url"]
        return image_url
    except Exception as e:
        print(f"上传图片时发生错误: {e}")
        return None


# 模拟识别文档的函数


def recognize_document(doc_type, image_url):
    url = ""
    if doc_type == "身份证":
        url = "http://127.0.0.1:50011/ai/id_card?url=" + image_url
    elif doc_type == "火车票":
        url = "http://127.0.0.1:50011/ai/train_ticket?url=" + image_url
    elif doc_type == "增值税发票":
        url = "http://127.0.0.1:50011/ai/invoice?url=" + image_url
    try:
        # 发送POST请求到上传API
        response = requests.post(url)
        response.raise_for_status()  # 如果请求失败，这将抛出一个异常
        return response.json()
    except Exception as e:
        print(f"识别图片时发生错误: {e}")
        return None


# 创建Gradio接口


def gradio_interface(doc_type, image):
    if doc_type is None:
        return "请先选择类型"

    if image is None:
        return "请先上传图片"

    # 上传图片并获取URL
    image_url = upload_image(image)
    if image_url is None:
        return "图片上传失败，请重试"

    # 识别文档
    result = recognize_document(doc_type, image_url)

    return result


# 创建Gradio应用
iface = gr.Interface(
    fn=gradio_interface,
    inputs=[
        gr.Dropdown(["身份证", "火车票", "增值税发票"], label="类型"),
        gr.Image(type="pil", label="上传图片", format="png"),
    ],
    outputs=gr.Textbox(label="识别结果"),
    title="身份证、火车票、增值税发票识别系统",
    description="上传图片并选择类型，然后点击提交按钮进行识别。",
    theme="default",
    allow_flagging="never",
    submit_btn="提交",
    clear_btn="重置",
)

# 运行应用
iface.launch(server_name="0.0.0.0")
