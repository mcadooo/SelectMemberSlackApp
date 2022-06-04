# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:32:09 2022

@author: shimalab
"""

import json
import numpy as np
from operator import itemgetter


# 人を追加
def registerPerson(i, name, exp, history, person_list):
    '''===人を追加===
    i       [int] : 登録ID,
    name    [str] : 名前,
    exp     [int] : これまでの仕事量,
    history [str] : 前回の仕事,
    person_list [dic] : 追加先の辞書リスト（return）
    =============='''
    add_person = {"name": name, "exp": exp, 'history': history}
    person_list['person'+str(i)] = add_person
    return person_list


# 仕事を追加
def registerWork(i, name, weight, need, work_list):
    '''===仕事を追加===
    i      [int] : 登録ID,
    name   [str] : 仕事名,
    weight [int] : この仕事の重さ,
    need   [int] : 必要人数,
    work_list [dic] : 追加先の辞書リスト（return）
    =============='''
    add_work = {"name": name, "weight": weight, 'need': need}
    work_list['work'+str(i)] = add_work
    return work_list


# 人，仕事を削除
def deleteObject(my_list, name):
    my_list.pop(name)
    return my_list


# 人，仕事をJSONファイルへ出力
def jsonWrite(path, my_list):
    with open(path, mode='w') as file:
        json.dump(my_list, file, ensure_ascii=False, indent=2)


# JSONファイルから読み取り，人，仕事オブジェクトへ
def jsonRead(path):
    with open(path, mode='r') as file:
        data = json.load(file)
    return data


# 追加や削除を行う用の配列
def copyArray(array):
    copy = array
    return copy


# 仕事量からメンバーを選択し，出力
# def selectMember():


# 名前探索
def nameSearch(name, person_list):
    person_ids = [key for key, dic in person_list.items() if dic['name'] == name]
    return person_ids

#履歴チェック
#履歴のworkと今回のworkが被った人が1，その他の人が0の配列作成
def historyCheck(sorted_person,sorted_work):
    person_count = 0 #人番号（人の辞書のkey）
    history_result = np.zeros(len(sorted_person)) #履歴と被ってしまった人が1になる
    
    for i in range(len(sorted_work)):
        #その仕事に必要な人数だけ割り振り
        for j in range(sorted_work[i]['need']):
            
            #履歴のworkと今回のworkが被ったとき
            if sorted_person[person_count]['history'] == sorted_work[i]['name']:
                history_result[person_count] = 1 #フラグを立てる
            person_count += 1 #次の人へ
            
    return(history_result)


#人の入れ替え
#key1とkey2の辞書の入れ替え
def changePerson(sorted_person,key1,key2):
    tmp_person = sorted_person[key1]
    sorted_person[key1] = sorted_person[key2]
    sorted_person[key2] = tmp_person
    
    return sorted_person

#人の並び順変更
def reSorted(sorted_person,sorted_work):
    num_person = len(sorted_person) #合計人数
    
    for i in range(num_person):
        
        history_result = historyCheck(sorted_person, sorted_work)
        
        #履歴被りした人数
        history_count = np.count_nonzero(history_result == 1)
        
        
        #履歴フラグが立ってるとき
        if history_result[i] == 1:
            #最後の人（上にしか人がいない）
            if i == num_person - 1:
                #人リストの端から端まで
                for j in range(num_person - 1):
                    #下の人との入れ替え
                    sorted_person = changePerson(sorted_person, i, i - j - 1)
                    
                    #入れ替えで履歴被りが減ったとき
                    if np.count_nonzero(historyCheck(sorted_person,sorted_work) == 1) < history_count:
                        break
            
            #最初の人（下にしか人がいない）
            elif i == 0:
                #人リストの端から端まで
                for j in range(num_person - 1):
                    #上の人との入れ替え
                    sorted_person = changePerson(sorted_person, i, i + j + 1)
                    
                    #入れ替えで履歴被りが減ったとき
                    if np.count_nonzero(historyCheck(sorted_person,sorted_work) == 1) < history_count:
                        break
            
            #上下に人がいる人
            else:
                change_distance = 1 #入れ替え先との距離
                while(True):
                    #下の人との入れ替え可能かどうか
                    if i + change_distance < num_person:
                        #下の人との入れ替え
                        sorted_person = changePerson(sorted_person, i, i + change_distance)
                        
                        #入れ替えで履歴被りが減ったとき
                        if np.count_nonzero(historyCheck(sorted_person,sorted_work) == 1) < history_count:
                            break
                    #上の人との入れ替え可能かどうか
                    elif i - change_distance >= 0:
                        #上の人との入れ替え
                        sorted_person = changePerson(sorted_person, i, i - change_distance)
                        
                        #入れ替えで履歴被りが減ったとき
                        if np.count_nonzero(historyCheck(sorted_person,sorted_work) == 1) < history_count:
                            break
                        else:
                            change_distance += 1
                    #入れ替えがもうできないとき
                    #探索終了
                    else:
                        break
        
    return sorted_person


if __name__ == "__main__":
    person_list = dict()
    work_list = dict()
    history = []
    totalnum = 2

    person_l = dict()

    # path_person='C:\\Users\\shimalab\\Desktop\\person.json'
    # path_work='C:\\Users\\shimalab\\Desktop\\work.json'
    # path_person = '.'
    # path_work = '.'
    # json_person_read(path_person)
    # json_work_read(path_work)

    # テスト用
    person_list = registerPerson(1, 'Aさん', 5, 'pointE', person_list)
    person_list = registerPerson(2, 'Bさん', 6, 'pointC', person_list)
    person_list = registerPerson(3, 'Cさん', 9, 'pointG', person_list)
    person_list = registerPerson(4, 'Dさん', 4, 'pointA', person_list)
    person_list = registerPerson(5, 'Eさん', 2, 'pointC', person_list)
    person_list = registerPerson(6, 'Fさん', 3, 'pointD', person_list)
    person_list = registerPerson(7, 'Gさん', 8, 'pointF', person_list)
    person_list = registerPerson(8, 'Hさん', 6, 'pointB', person_list)
    person_list = registerPerson(9, 'Iさん', 7, 'pointE', person_list)
    person_list = registerPerson(10, 'Jさん', 1, 'pointD', person_list)
    person_list = registerPerson(11, 'Kさん', 5, 'pointF', person_list)
    work_list = registerWork(1, 'pointA', 2, 1, work_list)
    work_list = registerWork(2, 'pointB', 5, 1, work_list)
    work_list = registerWork(3, 'pointC', 3, 2, work_list)
    work_list = registerWork(4, 'pointD', 4, 2, work_list)
    work_list = registerWork(5, 'pointE', 2, 2, work_list)
    work_list = registerWork(6, 'pointF', 1, 2, work_list)
    work_list = registerWork(7, 'pointG', 1, 1, work_list)


    copy_person = copyArray(person_list)
    copy_work = copyArray(work_list)


    # 仕事量順でソート
    p_value = [dic for key, dic in copy_person.items()]
    sorted_person = sorted(p_value, key=itemgetter('exp'))

    w_value = [dic for key, dic in copy_work.items()]
    sorted_work = sorted(w_value, key=itemgetter('weight'), reverse=True)


    # ここから仕事の割り当て
    re_sorted_person = reSorted(sorted_person, sorted_work)


