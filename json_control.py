# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:32:09 2022

@author: shimalab
"""

import json


#人を追加
def register_person(i,name,exp,history):
    add_person={"name": name, "exp": exp, 'history': history}
    person_list['person'+str(i)]=add_person
    
#仕事を追加
def register_work(i,name,weight,need):
    add_work={"name": name, "weight": weight, 'need': need}
    work_list['work'+str(i)]=add_work

#人を削除
def delete_person(name):
    person_list.pop(name)
    

# ヒトをJSONファイルへ出力
def json_person_read(path):
    with open(path, mode='w') as file:
        json.dump(person_list, file, ensure_ascii=False, indent=2)


# 仕事をJSONファイルへ出力
def json_work_read(path):
    with open(path, mode='w') as file:
        json.dump(work_list, file, ensure_ascii=False, indent=2)


# ヒトオブジェクトをJSONファイルへ出力
def json_person_write(path,totalnum):
    with open(path, mode='r') as file:
        data=json.load(file)

    return data

# 仕事オブジェクトをJSONファイルへ出力
def json_work_write(path,totalnum):
    with open(path, mode='r') as file:
        data=json.load(file)

    return data

#仕事量からメンバーを選択し，出力
#def select_member():
    
#追加や削除を行う用の配列
def copy_array(array):
    copy=array
    
    return copy
    

#名前探索
def json_search():
    personnum=[key for key,dic in person_list.items() if dic['name']=='AA'] 
    #print(personnum)
    
    return personnum



person_list=dict()
work_list=dict()
history=[]
totalnum=2

person_l=dict()

path_person='C:\\Users\\shimalab\\Desktop\\person.json'
path_work='C:\\Users\\shimalab\\Desktop\\work.json'
json_person_read(path_person)
json_work_read(path_work)



#テスト用
register_person(1,'AA',5,'place')
register_person(2,'BA',6,'place2')
register_work(1,'place',50,4)
register_work(2,'place',50,4)


copy_person=copy_array(person_list)
copy_work=copy_array(work_list)


delete_person("person1")

print(person_list)


data1=json_person_write(path_person,totalnum)
data2=json_work_write(path_work,totalnum)

print(data1)
print(data2)