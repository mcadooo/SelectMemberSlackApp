# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:32:09 2022

@author: shimalab
"""

import json
import numpy as np
from operator import itemgetter


#人を追加
def register_person(i,name,exp,history):
    add_person={"name": name, "exp": exp, 'history': history}
    person_list['person'+str(i)]=add_person
    
#仕事を追加
def register_work(i,name,weight,need):
    add_work={"name": name, "weight": weight, 'need': need}
    work_list['work'+str(i)]=add_work

#人を削除
def delete_person(p_list,name):
    p_list.pop(name)
    
#人を削除
def delete_work(w_list,name):
    w_list.pop(name)
    

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


#追加や削除を行う用の配列
def copy_array(array):
    copy=array
    
    return copy
    

#仕事量からメンバーを選択し，出力
#def select_member():
    

#名前探索
def json_search():
    personnum=[key for key,dic in person_list.items() if dic['name']=='Aさん'] 
    #print(personnum)
    
    return personnum

#履歴チェック
def history_check(sorted_person,sorted_work):
    person_count = 0
    history_result = np.zeros(len(sorted_work)) #履歴のworkと今回のworkが被りフラグ
    for i in range(len(sorted_work)):
       capacity = sorted_work[i]['need']
       
       for j in range(capacity):
           #履歴のworkと今回のworkが被ったとき
           if sorted_person[person_count]['history'] == sorted_work[i]['name']:
               history_result[i] = 1
           person_count += 1
    
           
           
    return(history_result)

"""       
#仕事の順番入れ替え
def change_work(sorted_work,history_result):
    for i in range(len(sorted_work)):
        if history_result[i] == 1:
            if 
"""

# 重み更新関数
def updateWeight(copy_person, copy_weight, role_table):
    for i in range(len(role_table)):
        role_person = role_table[i][1]
        role_work = role_table[i][0]
    
        print(role_person)

        now_p = [dic_person for key_person, dic_person in copy_person.items() if dic_person['name'] == role_person]
        now_w = [dic_work for key_work, dic_work in copy_work.items() if dic_work['name'] == role_work]
    
        print(now_p)
        print(now_w)

        now_p[0]['exp'] += now_w[0]['weight']     #重み更新
        now_p[0]['history'] + now_w[0]['name']   #history更新
    
    return copy_person
    


person_list=dict()
work_list=dict()
history=[]
totalnum=2

person_l=dict()

#path_person='C:\\Users\\shimalab\\Desktop\\person.json'
#path_work='C:\\Users\\shimalab\\Desktop\\work.json'

#path_person = '.'
#path_work = '.'

#json_person_read(path_person)
#json_work_read(path_work)



#テスト用
register_person(1,'Aさん',5,'pointE')
register_person(2,'Bさん',6,'pointC')
register_person(3,'Cさん',9,'pointG')
register_person(4,'Dさん',4,'pointA')
register_person(5,'Eさん',2,'pointC')
register_person(6,'Fさん',3,'pointD')
register_person(7,'Gさん',8,'pointF')
register_person(8,'Hさん',6,'pointB')
register_person(9,'Iさん',7,'pointE')
register_person(10,'Jさん',1,'pointD')
register_person(11,'Kさん',5,'pointF')
register_work(1,'pointA',2,1)
register_work(2,'pointB',5,1)
register_work(3,'pointC',3,2)
register_work(4,'pointD',4,2)
register_work(5,'pointE',2,2)
register_work(6,'pointF',1,2)
register_work(7,'pointG',1,1)


role_table=[]
hold_list1=['pointA','Aさん']
hold_list2=['pointB','Bさん']
hold_list3=['pointC','Cさん']
hold_list4=['pointC','Dさん']

role_table.append(hold_list1)
role_table.append(hold_list2)
role_table.append(hold_list3)
role_table.append(hold_list4)



copy_person=copy_array(person_list)
copy_work=copy_array(work_list)


# 関数起動部
copy_person=updateWeight(copy_person, copy_work, role_table)

print(copy_person)
