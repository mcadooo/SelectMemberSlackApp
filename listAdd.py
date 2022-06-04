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
    need=makeWorkWeightOptions(1, 20)
	
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
    
    say(
            blocks=[
    		{
    			"type": "actions",
    			"elements": [
    				{
    					"type": "static_select",
    					"placeholder": {
    						"type": "plain_text",
    						"text": "Select an need",
    						"emoji": True
    					},
    					"options": need,
    					"action_id": "select_need"
    				}]
            }],
            text=f"Hey there <@{message['user']}>!"  # 表示されなくなる
            )
    
    path="./log/temp_work.json"
    work_list=dict()
    
    # jsonファイルへの書き出しに差し替え
    with open(path, mode='w') as file:
        json.dump(work_list, file, ensure_ascii=False, indent=2)
    
    # jsonファイルへの読み込みに差し替え
    with open(path, mode='r') as file:
        work_list = json.load(file)
        
    work_num=0 #work_listの長さの最大値を取得
    
    template={"name":"","weight":0,"need":0}
    work_list["work"+str(work_num+1)]=template
    
    # jsonファイルへの書き出しに差し替え
    with open(path, mode='w') as file:
        json.dump(work_list, file, ensure_ascii=False, indent=2)
    
    @app.action("work_name_input-action")
    def checkInputData(body,ack,say):
        ack()
        input_item=body["actions"][0]["value"]
        
        # jsonファイルへの読み込みに差し替え
        with open(path, mode='r') as file:
            work_list = json.load(file)
            
        work_list["work"+str(work_num+1)]["name"]=input_item
        
        # jsonファイルへの書き出しに差し替え
        with open(path, mode='w') as file:
            json.dump(work_list, file, ensure_ascii=False, indent=2)
        
    @app.action("select_weight")
    def checkWeightData(body, ack, say):
        ack()
        select_items=body["actions"][0]["selected_option"]["text"]["text"]
        
        # jsonファイルへの読み込みに差し替え
        with open(path, mode='r') as file:
            work_list = json.load(file)
            
        work_list["work"+str(work_num+1)]["weight"]=select_items
        
        # jsonファイルへの書き出しに差し替え
        with open(path, mode='w') as file:
            json.dump(work_list, file, ensure_ascii=False, indent=2)
    
    @app.action("select_need")
    def checkNeedData(body,ack,say):
        ack()
        select_items=body["actions"][0]["selected_option"]["text"]["text"]
        
        # jsonファイルへの読み込みに差し替え
        with open(path, mode='r') as file:
            work_list = json.load(file)
            
        work_list["work"+str(work_num+1)]["need"]=select_items
        
        # jsonファイルへの書き出しに差し替え
        with open(path, mode='w') as file:
            json.dump(work_list, file, ensure_ascii=False, indent=2)


# アプリを起動します
if __name__ == "__main__":
    sm=SocketModeHandler(app, jsn["SLACK_APP_TOKEN"]["token"]).start()