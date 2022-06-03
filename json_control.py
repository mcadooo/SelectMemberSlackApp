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
register_person(1,'Aさん',5,'pointA')
register_person(2,'Bさん',6,'pointB')
register_person(3,'Cさん',9,'pointC')
register_person(4,'Dさん',2,'pointD')
register_person(5,'Eさん',2,'pointD')
register_work(1,'pointA',50,1)
register_work(2,'pointB',60,1)
register_work(3,'pointC',20,1)
register_work(4,'pointD',40,2)


copy_person=copy_array(person_list)
copy_work=copy_array(work_list)


#仕事量順でソート
p_value=[dic for key,dic in copy_person.items()]
sorted_person=sorted(p_value,key=itemgetter('exp'))

w_value=[dic for key,dic in copy_work.items()]
sorted_work=sorted(w_value,key=itemgetter('weight'),reverse=True)


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