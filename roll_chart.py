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

@app.message("分担表")
def send_roll_chart(message,say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
            {
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "New request",
				"emoji": True
            }
            }
            ],        
            text=f"Hey there <@{message['user']}>!"  # 表示されなくなる
                )
# アプリを起動します
if __name__ == "__main__":
    # SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    SocketModeHandler(app, jsn["SLACK_APP_TOKEN"]["token"]).start()