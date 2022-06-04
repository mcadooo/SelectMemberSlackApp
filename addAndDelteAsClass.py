# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 15:07:11 2022

@author: ShimaLab
"""
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json

#jsonからトークンを読み取る
with open('token.json') as f:
    jsn = json.load(f)

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
app = App(token=jsn["SLACK_BOT_TOKEN"]["token"])

class selectOptions:
    def __init__(self):
        self.chart=[["ゴミ捨て1","AA"],["ゴミ捨て2","AB"],["ゴミ捨て3","AC"],["教員室1","AD"],["教員室2","AE"]]
        
        self.delete_work=[]
        self.delete_person=[]
    
    # 与えられた配列から選択肢を作成する関数
    # num:0=仕事，1＝メンバ
    def makeOptions(self,array,num):
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
    
    def makeResultMessage(self,array):
        text=""
        for i in range(len(array)):
            text+=array[i]
            if i<len(array)-1:
                text+=","
    	
        return text
	
    # 欠席者の選択肢をSlackに送信する関数
    @app.message("欠席者")
    def selectDeletePerson(self,message,say):
        # 掃除当番表の配列を返す関数に変更予定
        array=self.chart
        
        # 辞書型の選択肢一覧（options）を作成
        person=self.makeOptions(array, 1)
    	
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
    def selectDeleteWork(self,message,say):
        # 掃除当番表の配列を返す関数に変更予定
        array=self.chart
        
        # 辞書型の選択肢一覧（options）を作成
        work=self.makeOptions(array, 0)
    	
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
	
	# マルチ選択のそうじ項目で何か選択されたら
@app.action("multi_work_select-action")
def actionWorkButtonClick(self,body, ack, say):
	# アクションを確認したことを即時で応答します
	ack()
	select_items=body["actions"][0]["selected_options"]
	work=[s["text"]["text"] for s in select_items]
	self.delete_work=work
	text=self.makeResultMessage(work)

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
	])

	# マルチ選択のメンバ項目で何か選択されたら
	@app.action("multi_person_select-action")
	def actionPersonButtonClick(self,body, ack, say):
		# アクションを確認したことを即時で応答します
		ack()
		select_items=body["actions"][0]["selected_options"]
		person=[s["text"]["text"] for s in select_items]
		self.delete_person=person
		text=self.makeResultMessage(person)

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
		])

# アプリを起動します
if __name__ == "__main__":
	so=selectOptions()
	SocketModeHandler(app, jsn["SLACK_APP_TOKEN"]["token"]).start()