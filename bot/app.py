#!/usr/bin/env python3
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import os
from dotenv import load_dotenv
from botbuilder.core import BotFrameworkAdapter, BotFrameworkAdapterSettings, TurnContext

# 加载环境变量
load_dotenv()

# 创建适配器
SETTINGS = BotFrameworkAdapterSettings(
    app_id=os.environ.get("MicrosoftAppId", ""),
    app_password=os.environ.get("MicrosoftAppPassword", "")
)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# 简单问答数据
QNA_DATA = {
    "砂纸用途是什么": "砂纸主要用于打磨和抛光各种表面，如木材、金属、塑料、涂料等。不同粒度的砂纸适用于不同的打磨阶段。",
    "如何选择砂纸粒度": "砂纸粒度选择取决于您的具体需求：\n- 粗粒度(P40-P80)：用于初步打磨和去除大量材料\n- 中粒度(P100-P180)：用于中等光滑度的打磨\n- 细粒度(P220-P400)：用于精细打磨和上漆前准备\n- 超细粒度(P600以上)：用于精细抛光和漆面处理",
    "天鹰砂纸有什么特点": "天鹰砂纸特点包括：\n- 高品质磨料，耐用性强\n- 均匀涂层，确保一致的打磨效果\n- 多种规格和粒度可选\n- 适用于各种专业和DIY应用场景",
    "如何购买产品": "您可以通过我们的网站在线购买，也可以通过电话(123-456-7890)或电子邮件(sales@flytiger.com)联系我们的销售团队进行订购。",
    "产品价格是多少": "我们的产品价格根据型号、粒度和购买数量而有所不同。您可以在产品页面查看详细价格，批量采购可享受折扣。",
    "如何支付": "我们支持多种支付方式，包括支付宝、微信支付和银行转账。所有在线订单处理都是安全加密的。",
    "发货时间和运费": "正常情况下，订单会在1-2个工作日内发货。标准快递免运费，加急快递需额外支付15元运费。",
    "如何退换货": "如果产品有质量问题，我们提供15天内退换货服务。请通过客服联系我们，并提供订单号和问题描述。",
    "批发合作": "我们欢迎批发合作，大量采购可享受特别折扣。请联系我们的销售团队(sales@flytiger.com)获取批发价格。",
    "公司地址": "我们的公司位于广东省广州市天河区某某路某某号。欢迎实地参观考察。"
}

# 错误处理
async def on_error(context: TurnContext, error: Exception):
    """错误处理器"""
    print(f"\n [on_turn_error]: {error}")
    
    # 向用户发送错误消息
    await context.send_activity("机器人遇到了错误，请稍后重试。")

# 设置错误处理器
ADAPTER.on_turn_error = on_error

# 处理消息
async def on_message_activity(turn_context: TurnContext):
    """处理消息活动"""
    # 获取用户消息
    user_message = turn_context.activity.text.strip().lower()
    
    # 查找最匹配的问题
    best_match = None
    best_score = 0
    
    for question in QNA_DATA.keys():
        if user_message in question.lower():
            score = len(user_message) / len(question.lower())
            if score > best_score:
                best_score = score
                best_match = question
    
    # 如果找到匹配的问题，返回答案
    if best_match and best_score > 0.5:
        await turn_context.send_activity(QNA_DATA[best_match])
    else:
        # 默认回复
        await turn_context.send_activity("感谢您的咨询。我是天鹰砂纸的智能助手，可以回答有关产品、订单和服务的问题。如果您需要人工服务，请拨打客服电话123-456-7890。")

# Bot处理函数
async def bot_main(req_body):
    """主处理函数"""
    activity = req_body
    
    # 检查活动类型
    if activity['type'] == 'message':
        # 创建上下文
        async def aux_func(turn_context):
            await on_message_activity(turn_context)
        
        await ADAPTER.process_activity(activity, "", aux_func)
    
    return {"status": 200}

# 简单的Flask应用
if __name__ == "__main__":
    from flask import Flask, request, jsonify
    
    app = Flask(__name__)
    
    @app.route("/api/messages", methods=["POST"])
    def messages():
        if request.headers.get("Content-Type") == "application/json":
            body = request.json
            result = bot_main(body)
            return jsonify(status=result["status"])
        else:
            return jsonify(status=415)
    
    app.run(host="0.0.0.0", port=3978) 