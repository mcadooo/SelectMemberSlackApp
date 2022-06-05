# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 23:25:52 2022

@author: lonytom
"""

import os
import numpy as np
import pandas as pd
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import json

import selectMember as sm

#jsonからトークンを読み取る
with open('token.json') as f:
    jsn = json.load(f)

# ボットトークンとソケットモードハンドラーを使ってアプリを初期化します
# app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
app = App(token=jsn["SLACK_BOT_TOKEN"]["token"])

# 仕事場所と担当者の二次元配列からメッセージを作成する関数
def makeChart(array):
    # 配列の要素毎に改行を加えて，一つのテキストに変換
    text=""
    col=array.columns.values
    for i in range(len(array)):
        text+=array[col[0]][i]+"   "+array[col[1]][i]+"\n"

    return text

# 選択項目を一列に並べたテキストを生成
def makeResultMessage(array):
    text=""
    for i in range(len(array)):
        text+=array[i]
        if i<len(array)-1:
            text+=","

    return text

# 仕事一覧の辞書型を改行入りの一つの文字列に変換する関数
def makeWorkComment(work_list):
    text=""
    for w in work_list:
        print(w)
        w=work_list[w]
        text+=w["name"]+"  "+w["weight"]+"  "+w["need"]+"\n"

    return text

# 欠席者の選択肢を作成する関数
def makePersonOptions(array):
    options=[]
    for i in range(len(array)):
        template={"text": {
					"type": "plain_text",
					"text": "*this is plain_text text*",
					"emoji": True
					},
				"value": None}
        template["value"]="value-"+str(i)
        template["text"]["text"]=str(array["name"][i])
        options.append(template.copy())

    return options

# そうじ削除の選択肢を作成する関数
def makeWorkOptions(array):
    options=[]
    for i in range(len(array)):
        template={"text": {
					"type": "plain_text",
					"text": "*this is plain_text text*",
					"emoji": True
					},
				"value": None}
        template["value"]="value-"+str(i)
        template["text"]["text"]=str(array["name"][i])
        options.append(template.copy())

    return options

# 仕事の重さの選択肢を作成する関数
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

# 分担表の各項目の文字列長をそろえる関数(引数はpandas)
def alignStringLength(strings):
    strings=pd.Series(map(str, strings),name=strings.name) # 渡された配列の中身をすべてstr型に変換
    length=max(list(map(len,strings))) # 配列の中で最大の文字列長を取得

    # すべての文字列を最大長に合わせるため末尾にスペースを追加
    def addSpace(string):
        string=str(string)
        string+="　"*(length-len(string))
        return string

    # スペースの追加をSeries型の各要素に実行※名前を指定しないと属性情報が消失
    strings=pd.Series(map(addSpace, strings),name=strings.name)

    return strings

# 分担表をSlackに送信する関数
@app.message("分担表")
def send_roll_chart(message,say):
    # jsonから読み込み
    person_list = sm.jsonRead('./log/person_copy.json')
    work_list = sm.jsonRead('./log/work_copy.json')

    # 掃除当番表の配列を返す関数
    role_table, work_list = sm.selectMember(person_list, work_list)
    sm.jsonWrite('./log/work_copy.json', work_list)  # jsonへ書き出し

    # 重み更新して保存
    person_list = sm.updateWeight(person_list, work_list, role_table)
    sm.jsonWrite('personlab.json', person_list)
    sm.jsonWrite('./log/person_copy.json', person_list)

    # 二次元リストならpandasに変換してるけど，最終的にDataFrame型になってればおけ
    role_table = pd.DataFrame(np.array(role_table), columns=["掃除","担当者"])
    role_table = role_table.apply(alignStringLength)
    role_table.to_csv('./log/role_tabel.csv')  # 分担表保存

    # 生成された分担のDataFrameを単一テキストに変換
    tex=makeChart(role_table)

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

    sm.jsonWrite(path, work_list)  # jsonファイルへの書き出し
    work_list = sm.jsonRead(path)  # jsonファイルへの読み込み

    work_num=0 #work_listの長さの最大値を取得

    template={"name":"","weight":0,"need":0}
    work_list["work"+str(work_num+1)]=template

    sm.jsonWrite(path, work_list)  # jsonファイルへの書き出し

    @app.action("work_name_input-action")
    def checkInputData(body,ack,say):
        ack()
        input_item=body["actions"][0]["value"]

        work_list = sm.jsonRead(path)  # jsonファイルへの読み込み

        work_list["work"+str(work_num+1)]["name"]=input_item

        sm.jsonWrite(path, work_list)  # jsonファイルへの書き出し

    @app.action("select_weight")
    def checkWeightData(body, ack, say):
        ack()
        select_items=body["actions"][0]["selected_option"]["text"]["text"]

        work_list = sm.jsonRead(path)  # jsonファイルへの読み込み

        work_list["work"+str(work_num+1)]["weight"]=select_items

        sm.jsonWrite(path, work_list)  # jsonファイルへの書き出し

    @app.action("select_need")
    def checkNeedData(body,ack,say):
        ack()
        select_items=body["actions"][0]["selected_option"]["text"]["text"]

        work_list = sm.jsonRead(path)  # jsonファイルへの読み込み

        work_list["work"+str(work_num+1)]["need"]=select_items

        sm.jsonWrite(path, work_list)  # jsonファイルへの書き出し

    @app.action("check_work_list")
    def checkWorkList(body,ack,say):
        ack()
        path="./log/temp_work.json" # 当日の仕事リストのパス(場所とファイル名はしらないので要変更)
        all_work_today = sm.jsonRead(path)  # jsonファイルへの読み込み

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

    work_list = sm.jsonRead(path_work_list)  # jsonファイルへの読み込み
    temp_work = sm.jsonRead(path_temp_work)  # jsonファイルへの読み込み
    add_work = temp_work.value()

    sm.registerWork(add_work['name'], add_work['weight'], add_work['need'], work_list)
    sm.jsonWrite(path_work_list, work_list)  # jsonファイルへの書き出し

# 欠席者の選択肢をSlackに送信する関数
@app.message("欠席者")
def selectDeletePerson(message,say):
    base_path="./personlab.json"
    person_list = pd.read_json('personlab.json').T

    # jsonから読み込み
    person_copy = sm.jsonRead('personlab.json')
    work_copy = sm.jsonRead('worklab.json')
    # jsonへ書き出し
    sm.jsonWrite('./log/person_copy.json', person_copy)
    sm.jsonWrite('./log/work_copy.json', work_copy)

    # 辞書型の選択肢一覧（options）を作成
    person=makePersonOptions(person_list)

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
 					"text": "Select absentees",
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
    work_list = pd.read_json('worklab.json').T

    # jsonから読み込み
    person_copy = sm.jsonRead('personlab.json')
    work_copy = sm.jsonRead('worklab.json')

    # jsonへ書き出し
    sm.jsonWrite('./log/person_copy.json', person_copy)
    sm.jsonWrite('./log/work_copy.json', work_copy)

    # 辞書型の選択肢一覧（options）を作成
    work=makeWorkOptions(work_list)

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
 					"text": "Select clean",
 					"emoji": True
				},
				"options": work,
				"action_id": "multi_work_select-action"
 			}
		}
 	],
        text=f"Hey there <@{message['user']}>!"  # 表示されなくなる
        )

# マルチ選択の選択したそうじ項目を取得する関数
# 選択した項目を削除する関数に渡す
@app.action("multi_work_select-action")
def actionInputWorkSelect(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    select_items=body["actions"][0]["selected_options"]
    work=[s["text"]["text"] for s in select_items] # 選択したしごと名の一次元配列
    text=makeResultMessage(work)

    # jsonから読み込み
    work_list = sm.jsonRead('./log/work_copy.json')
    # リストから削除
    for name in work:
        workId = sm.nameSearch(name, work_list)
        work_list = sm.deleteObject(work_list, workId)
    # jsonへ書き出し
    sm.jsonWrite('./log/work_copy.json', work_list)

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

# マルチ選択の選択した欠席者項目を取得する関数
# 選択した項目を削除する関数に渡す
@app.action("multi_person_select-action")
def actionInputPersonSelect(body, ack, say):
    # アクションを確認したことを即時で応答します
    ack()
    select_items=body["actions"][0]["selected_options"]
    person=[s["text"]["text"] for s in select_items] # 選択したメンバ名の一次元配列
    text=makeResultMessage(person)

    # jsonから読み込み
    person_list = sm.jsonRead('./log/person_copy.json')
    # リストから削除
    for name in person:
        workId = sm.nameSearch(name, person_list)
        person_list = sm.deleteObject(person_list, name)
    # jsonへ書き出し
    sm.jsonWrite('./log/person_copy.json', person_list)

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

# アプリを起動します
if __name__ == "__main__":
    # SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    SocketModeHandler(app, jsn["SLACK_APP_TOKEN"]["token"]).start()
