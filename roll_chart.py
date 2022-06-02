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

# 'hello' を含むメッセージをリッスンします
# 指定可能なリスナーのメソッド引数の一覧は以下のモジュールドキュメントを参考にしてください：
# https://slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("そうじ")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"ヒトを追加"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"追加"},
                    "action_id": "button_click_add"
                }
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"ヒトを削除"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text":"削除"},
                    "action_id": "button_click_del"
                }
            }
        ],
        text=f"Hey there <@{message['user']}>!"  # 表示されなくなる
    )

# 仕事場所と担当者の二次元配列からメッセージを作成する関数
def makeComent(array):
    blocks=[]
    # 仕事一つ当たりのblockのテンプレート※うまくいかなかった
    template={
                "type": "section",
                "text": {
                "type": "plain_text",
                "text": None,
                "emoji": True}
            }
    
    text=""
    # 始めはBlockを生成して，それを送ろうとしたが，dictのリストがblocksの引数にとれない
    # 単一のblockとし，textに改行文字を入れて一つのtxtでメッセージを作成
    for a in array:
        # template["text"]=a[0]+" "+a[1]
        # blocks.append(template.copy())
        text+=a[0]+" "+a[1]+"\n"
    template["text"]=text
    blocks=template
    return blocks

# 分担表をSlackに送信する関数
@app.message("分担表")
def send_roll_chart(message,say):
    array=[["ゴミ捨て1","川崎"],["ゴミ捨て2","富濱"],["ゴミ捨て3","布野"],["教員室1","増尾"],["教員室2","松前"]]
    
    # 当初は単一のblockを渡そうとしたがblockの引数にとれなかった
    # 生成したblockの中から表示したいtxtのみ抽出し，それをblocksのtextのtextに代入
    block=makeComent(array)
    tex=block["text"]
    
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

# array=[["ゴミ捨て1","川崎"],["ゴミ捨て2","富濱"],["ゴミ捨て3","布野"],["教員室1","増尾"],["教員室2","松前"]]
# blocks=makeBlockComent(array)