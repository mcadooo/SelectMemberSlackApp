# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:32:09 2022

@author: shimalab
"""

import json




def register_person(i,name,exp,history):
    add_person={"name": name, "exp": exp, 'history': history}
    person_list['person'+str(i)]=add_person
    
def register_work(i,name,weight,need):
    add_work={"name": name, "weight": weight, 'need': need}
    work_list['work'+str(i)]=add_work


# 辞書オブジェクトをJSONファイルへ出力
def json_person_read(path):
    with open(path, mode='w') as file:
        json.dump(person_list, file, ensure_ascii=False, indent=2)


# 辞書オブジェクトをJSONファイルへ出力
def json_work_read(path):
    with open(path, mode='w') as file:
        json.dump(work_list, file, ensure_ascii=False, indent=2)


# 辞書オブジェクトをJSONファイルへ出力
def json_person_write(path,totalnum):
    with open(path, mode='r') as file:
        data=json.load(file)

    return data

# 辞書オブジェクトをJSONファイルへ出力
def json_work_write(path,totalnum):
    with open(path, mode='r') as file:
        data=json.load(file)

    return data

person_list=dict()
work_list=dict()
history=[]
totalnum=2

person_l=dict()

#テスト用
register_person(1,'AA',5,['place','place2'])
register_person(2,'BA',6,['place','place2'])
register_work(1,'place',50,4)
register_work(2,'place',50,4)


print(person_list['person1']['name'])


path_person='C:\\Users\\shimalab\\Desktop\\person.json'
path_work='C:\\Users\\shimalab\\Desktop\\work.json'
json_person_read(path_person)
json_work_read(path_work)

data1=json_person_write(path_person,totalnum)
data2=json_work_write(path_work,totalnum)
print(data1)
print(data2)
