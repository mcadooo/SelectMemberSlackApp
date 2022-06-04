# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 23:50:07 2022

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

def makeOptions(array):
    template={"text": {
                "type": "plain_text",
                "text": "*this is plain_text text*",
                "emoji": True
                },
            "value": None
             }
    work=[]
    person=[]
    for i in range(len(array)):
        template["value"]="value-"+str(i)
        
        template["text"]["text"]=array[i][0]
        work.append(template.copy())
        
        template["text"]["text"]=array[i][1]
        work.append(template.copy())
        
    return work,person

# 分担表をSlackに送信する関数
@app.message("そうじ削除")
def send_roll_chart(message,say):
    # 掃除当番表の配列を返す関数に変更予定
    array=[["ゴミ捨て1","AA"],["ゴミ捨て2","AB"],["ゴミ捨て3","AC"],["教員室1","AD"],["教員室2","AE"]]
    
    work,person=makeOptions(array)
    
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(
        blocks=[
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Test block with multi static select"
			},
			"accessory": {
				"type": "multi_static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select options",
					"emoji": True
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "ゴミ捨て1",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "教員室1",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "教員室2",
							"emoji": True
						},
						"value": "value-2"
					}
				],
				"action_id": "multi_static_select-action"
			}
		}
	],
        text=f"Hey there <@{message['user']}>!"  # 表示されなくなる
        )

# Addボタン押されたら
@app.action("multi_static_select-action")
def action_button_click(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    # チャンネルにメッセージを投稿します
    say(f"<@{body['user']['id']}> 追加！")

# アプリを起動します
if __name__ == "__main__":
    # SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    SocketModeHandler(app, jsn["SLACK_APP_TOKEN"]["token"]).start()