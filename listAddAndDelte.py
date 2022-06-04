# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 23:50:07 2022

@author: lonytom
"""
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json

#jsonからトークンを読み取る
with open('token.json') as f:
    jsn = json.load(f)

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=jsn["SLACK_BOT_TOKEN"]["token"])

# 与えられた配列から選択肢を作成する関数
# num:0=仕事，1＝メンバ
def makeOptions(array,num):
    options=[]
    for i in range(len(array)):
        template={"text": {
					"type": "plain_text",
					"text": "*this is plain_text text*",
					"emoji": True
					},
				"value": None}
        template["value"]="value-"+str(i)
        template["text"]["text"]=array[i][num]
        options.append(template.copy())
    
    return options

def makeWorkWeightOptions(minimum,maxim):
    options=[]
    for i in range(minimum,maxim+1):
        template={"text": {
					"type": "plain_text",
					"text": "*this is plain_text text*",
					"emoji": True
					},
				"value": None}
        template["value"]="value-"+str(i)
        template["text"]["text"]=str(i)
        options.append(template.copy())
        
    return options

# 追加したい仕事の選択肢をSlackに送信する関数
@app.message("しごと追加")
def selectAddWork(message,say):
    # 辞書型の選択肢一覧（options）を作成
    weight=makeWorkWeightOptions(1, 5)
	
    # イベントがトリガーされたチャンネルへ say() で複数選択肢を送信します
    say(
        blocks=[
            {
 			"dispatch_action": True,
 			"type": "input",
 			"element": {
				"type": "plain_text_input",
				"dispatch_action_config": {
 					"trigger_actions_on": [
						"on_character_entered"
 					]
				},
				"action_id": "work_name_input-action"
 			},
 			"label": {
				"type": "plain_text",
				"text": "仕事名",
				"emoji": True}
            }
 			],
        text=f"Hey there <@{message['user']}>!"  # 表示されなくなる
        )
	
    say(
            blocks=[
    		{
    			"type": "actions",
    			"elements": [
    				{
    					"type": "static_select",
    					"placeholder": {
    						"type": "plain_text",
    						"text": "Select an weight",
    						"emoji": True
    					},
    					"options": weight,
    					"action_id": "select_weight"
    				}]
            }],
            text=f"Hey there <@{message['user']}>!"  # 表示されなくなる
            )
    
    work=""
    weight=0
    
    @app.action("work_name_input-action")
    def checkInputData(body,ack,say):
        ack()
        input_item=body["actions"][0]["value"]
        print(input_item)
        work=input_item
        
    @app.action("select_weight")
    def checkWeightData(body, ack, say):
        ack()
        select_items=body["actions"][0]["selected_option"]["text"]["text"]
        print(select_items)
        weight=select_items
    print(work,weight)

# 欠席者の選択肢をSlackに送信する関数
@app.message("欠席者")
def selectDeletePerson(message,say):
    # 掃除当番表の配列を返す関数に変更予定
    array=[["ゴミ捨て1","AA"],["ゴミ捨て2","AB"],["ゴミ捨て3","AC"],["教員室1","AD"],["教員室2","AE"]]
    
    # 辞書型の選択肢一覧（options）を作成
    person=makeOptions(array, 1)
	
    # イベントがトリガーされたチャンネルへ say() で複数選択肢を送信します
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
				"options": person,
				"action_id": "multi_person_select-action"
 			}
		}
 	],
        text=f"Hey there <@{message['user']}>!"  # 表示されなくなる
        )

# 削除する仕事の選択しをSlackに送信する関数
@app.message("そうじ削除")
def selectDeleteWork(message,say):
    # 掃除当番表の配列を返す関数に変更予定
    array=[["ゴミ捨て1","AA"],["ゴミ捨て2","AB"],["ゴミ捨て3","AC"],["教員室1","AD"],["教員室2","AE"]]
    
    # 辞書型の選択肢一覧（options）を作成
    work=makeOptions(array, 0)
	
    # イベントがトリガーされたチャンネルへ say() で複数選択肢を送信します
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
				"options": work,
				"action_id": "multi_work_select-action"
 			}
		}
 	],
        text=f"Hey there <@{message['user']}>!"  # 表示されなくなる
        )

def makeResultMessage(array):
    text=""
    for i in range(len(array)):
        text+=array[i]
        if i<len(array)-1:
            text+=","
	
    return text

# マルチ選択のそうじ項目で何か選択されたら
@app.action("multi_work_select-action")
def actionWorkButtonClick(body, ack, say):
    # アクションを確認したことを即時で応答します
	ack()
	select_items=body["actions"][0]["selected_options"]
	work=[s["text"]["text"] for s in select_items] # 選択したしごと名の一次元配列
	text=makeResultMessage(work)

    # チャンネルに選択したそうじを投稿(確認用)
	say(
		blocks=[
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": text,
				"emoji": True
			}
		}
	]
	)

	return work

# マルチ選択の欠席者項目で何か選択されたら
@app.action("multi_person_select-action")
def actionPersonButtonClick(body, ack, say):
    # アクションを確認したことを即時で応答します
	ack()
	select_items=body["actions"][0]["selected_options"]
	person=[s["text"]["text"] for s in select_items] # 選択したメンバ名の一次元配列
	text=makeResultMessage(person)

    # チャンネルに選択したメンバ名を投稿(確認用)
	say(
		blocks=[
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"text": text,
				"emoji": True
			}
		}
	]
	)

	return person

# アプリを起動します
if __name__ == "__main__":
    sm=SocketModeHandler(app, jsn["SLACK_APP_TOKEN"]["token"]).start()