# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 23:25:52 2022

@author: lonytom
"""

import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json

#jsonからトークンを読み取る
with open('token.json') as f:
    jsn = json.load(f)


# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
# app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
app = App(token=jsn["SLACK_BOT_TOKEN"]["token"])

# 仕事場所と担当者の二次元配列からメッセージを作成する関数
def makeComent(array):
    # 配列の要素毎に改行を加えて，一つのテキストに変換
    text=""
    for a in array:
        text+=a[0]+"   "+a[1]+"\n"
    
    return text

# 分担表をSlackに送信する関数
@app.message("分担表")
def send_roll_chart(message,say):
    # 掃除当番表の配列を返す関数に変更予定
    array=[["ゴミ捨て1","AA"],["ゴミ捨て2","AB"],["ゴミ捨て3","AC"],["教員室1","AD"],["教員室2","AE"]]
    
    # 生成された分担の二次元配列を単一テキストに変換
    tex=makeComent(array)
    
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
            {
                "type": "section",
                "text": {
                    "type":"plain_text",
                    "text":tex,
                    "emoji":True
                    }
            }
            ],
        text=f"Hey there <@{message['user']}>!"  # 表示されなくなる
        )


# アプリを起動します
if __name__ == "__main__":
    # SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    SocketModeHandler(app, jsn["SLACK_APP_TOKEN"]["token"]).start()