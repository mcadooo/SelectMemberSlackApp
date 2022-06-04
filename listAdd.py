# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 23:50:07 2022

@author: lonytom
"""

from email import message
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json

#jsonからトークンを読み取る
with open('token.json') as f:
    jsn = json.load(f)

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=jsn["SLACK_BOT_TOKEN"]["token"])

# 仕事一覧の辞書型を改行入りの一つの文字列に変換する関数
def makeWorkComment(work_list):
    text=""
    for w in work_list:
        print(w)
        w=work_list[w]
        text+=w["name"]+"  "+w["weight"]+"  "+w["need"]+"\n"
    
    return text

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

    # 追加する仕事名の入力フォーム送信
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
	
    # 追加する仕事の重みを入力
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
    
    # 追加する仕事の必要人数を入力
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
    
    # 追加した仕事のリストを確認，更新を実行するボタン
    say(
        blocks=[
            {
                "type": "actions",
                "elements":[
                    {
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "確認",
						"emoji": True
					},
					"value": "click_check_work",
					"action_id": "check_work_list"
				},
                {
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "更新",
						"emoji": True
					},
					"value": "click_update_work",
					"action_id": "update_work_list"
				},
                ]
            }
        ]

    )
    
    base_path="./log/"
    if not os.path.isdir(base_path):
        os.makedirs(base_path)
    
    path=base_path+"temp_work.json"
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
    
    @app.action("check_work_list")
    def checkWorkList(body,ack,say):
        ack()
        path="./log/temp_work.json" # 当日の仕事リストのパス(場所とファイル名はしらないので要変更)
        # jsonファイルへの読み込みに差し替え
        with open(path, mode='r') as file:
            all_work_today = json.load(file)
        
        text=makeWorkComment(all_work_today)
        print(text)
        
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

@app.action("update_work_list")
def updateWorkList(message,say):
    path_work_list="./log/work_copy.json" # 当日の仕事リストのパス(場所とファイル名はしらないので要変更)
    path_temp_work="./log/temp_work.json" # 一次的に追加したい仕事のリストのパス
    work_list=dict()
    
    # jsonファイルへの読み込みに差し替え
    with open(path_work_list, mode='r') as file:
        work_list = json.load(file)
    
    # jsonファイルへの読み込みに差し替え
    with open(path_temp_work, mode='r') as file:
        temp_work = json.load(file)
    
    work_list["work"+str(len(work_list))]=temp_work

    # jsonファイルへの書き出しに差し替え
    with open(path_work_list, mode='w') as file:
        json.dump(work_list, file, ensure_ascii=False, indent=2)

# アプリを起動します
if __name__ == "__main__":
    sm=SocketModeHandler(app, jsn["SLACK_APP_TOKEN"]["token"]).start()