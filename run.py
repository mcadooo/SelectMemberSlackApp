# -*- coding: utf-8 -*-
"""
Created on Sun May 29 17:16:04 2022

@author: kwsk0
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

# Addボタン押されたら
@app.action("button_click_add")
def action_button_click(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    # チャンネルにメッセージを投稿します
    say(f"<@{body['user']['id']}> 追加！")
    
# Delボタン押されたら
@app.action("button_click_del")
def action_button_click(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    # チャンネルにメッセージを投稿します
    say(f"<@{body['user']['id']}> 削除！")
    
# アプリを起動します
if __name__ == "__main__":
    # SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    SocketModeHandler(app, jsn["SLACK_APP_TOKEN"]["token"]).start()