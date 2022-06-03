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


copy_person=copy_array(person_list)
copy_work=copy_array(work_list)


#仕事量順でソート
p_value=[dic for key,dic in copy_person.items()]
sorted_person=sorted(p_value,key=itemgetter('exp'))

w_value=[dic for key,dic in copy_work.items()]
sorted_work=sorted(w_value,key=itemgetter('weight'),reverse=True)


    



#ここから仕事の割り当て
history_result = history_check(sorted_person, sorted_work)





"""
final_list=[]
hold_list=[]
count=0

flag_person=np.zeros(len(sorted_person))

for work in sorted_work:
    capacity=work['need']
    
    for i in range(capacity):
        hold_list.append(work['name'])
        
        for person in sorted_person:

            if((person['history']!=work['name']) and flag_person[count]==0):
                
                
                hold_list.append(person['name'])
                final_list.append(hold_list)
                
                flag_person[count]=1
                count+=1
            
                #hold_list.clear()
                break
"""            
    
    
        # else :
        #     print('a')

    # final_list.append(hold_list)
    # hold_list.clear()



# delete_person(copy_person,"person1")
# delete_person(copy_work,"work1")

# print(person_list)


# data1=json_person_write(path_person,totalnum)
# data2=json_work_write(path_work,totalnum)

# print(data1)
# print(data2)