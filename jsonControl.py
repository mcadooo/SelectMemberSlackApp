# -*- coding: utf-8 -*-
"""
Created on Wed Jun  1 17:32:09 2022

@author: shimalab
"""

import json
import numpy as np
import copy
from operator import itemgetter


# 人を追加
def registerPerson(name, exp, history, person_list):
    '''===人を追加===
    name    [str] : 名前,
    exp     [int] : これまでの仕事量,
    history [str] : 前回の仕事,
    person_list [dic] : 追加先の辞書リスト(return 追加後)
    =============='''
    i = len(person_list) + 1
    add_person = {"name": name, "exp": exp, 'history': history}
    person_list['person'+str(i)] = add_person
    return person_list


# 仕事を追加
def registerWork(name, weight, need, work_list):
    '''===仕事を追加===
    name   [str] : 仕事名,
    weight [int] : この仕事の重さ,
    need   [int] : 必要人数,
    work_list [dic] : 追加先の辞書リスト(return 追加後)
    =============='''
    i = len(work_list) + 1
    add_work = {"name": name, "weight": weight, 'need': need}
    work_list['work'+str(i)] = add_work
    return work_list


# 人，仕事を削除
def deleteObject(my_list, obj_name):
    '''===人，仕事を削除===
    obj_name   [str] : 人，仕事のID(person1, work1など),
    my_list [dic] : 削除元の辞書リスト(return 削除後)
    =============='''
    my_list.pop(obj_name)
    return my_list


# 名前探索
def nameSearch(name, person_list):
    '''===名前からID探索===
    name   [str] : 仕事名,
    person_list  [dic] : メンバーの辞書リスト,
    person_ids  [str] : nameの人のＩＤ(return)
    =============='''
    person_ids = [key for key, dic in person_list.items() if dic['name'] == name]
    return person_ids[0]


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
    copy_array = copy.deepcopy(array)
    return copy_array


# 人数と仕事の数が一致するように予備を追加
# 仕事の割り当て直前に実施
def addJobless(person_list, work_list):
    '''===人数と仕事の数が一致するように予備を追加===
    person_list  [dic] : 今日の仕事できる人の辞書リスト,
    work_list    [dic] : 今日の仕事場所の辞書リスト(return jobless追加後)
    ======================'''
    work_num = 0  # 仕事に必要な合計人数
    w_value = [dic for key, dic in work_list.items()]

    for work in w_value:
        work_num += work["need"]

    add_num = len(person_list) - work_num  # 余った人数
    if add_num > 0:
        work_list = registerWork("jobless", 0, add_num, work_list)

    return work_list



# 履歴チェック
def historyCheck(sorted_person, sorted_work):
    '''===履歴チェック===
    履歴のworkと今回のworkが被った人が1，その他の人が0の配列作成\n
    sorted_person  [list(dic)] : 今日の仕事できる人のソート済み辞書リスト,
    sorted_work    [list(dic)] : 今日の仕事場所のソート済み辞書リスト,
    histry_result  [numpy.array(int)] : sorted_personの順に，0 or 1(return)
    ======================'''
    person_count = 0  # 人番号（人の辞書のkey）
    history_result = np.zeros(len(sorted_person))  # 履歴と被ってしまった人が1になる配列

    for i in range(len(sorted_work)):
        # その仕事に必要な人数だけ割り振り
        for _ in range(sorted_work[i]['need']):

            # 履歴のworkと今回のworkが被ったとき
            if sorted_person[person_count]['history'] == sorted_work[i]['name']:
                history_result[person_count] = 1  # フラグを立てる
            person_count += 1  # 次の人へ

    return history_result


# 人の入れ替え
# key1とkey2の辞書の入れ替え
def changePerson(sorted_person, key1, key2):
    tmp_person = sorted_person[key1]
    sorted_person[key1] = sorted_person[key2]
    sorted_person[key2] = tmp_person

    return sorted_person


# 人の並び順変更
def reSorted(sorted_person, sorted_work):
    '''===人の並び順変更===
    履歴のworkと今回のworkが被った人が1，その他の人が0の配列作成\n
    sorted_person  [list(dic)] : 今日の仕事できる人のソート済み辞書リスト,
    sorted_work    [list(dic)] : 今日の仕事場所のソート済み辞書リスト,
    sorted_person  [list(dic)] : 場所の連続を考慮して，並び変えたソート済み辞書リスト(return)
    ======================'''
    num_person = len(sorted_person) #合計人数

    for i in range(num_person):
        history_result = historyCheck(sorted_person, sorted_work)
        history_count = np.count_nonzero(history_result == 1)  # 履歴被りした人数

        # 履歴フラグが立ってるとき
        if history_result[i] == 1:
            # 最後の人（上にしか人がいない）
            if i == num_person - 1:
                # 人リストの端から端まで
                for j in range(num_person - 1):
                    # 下の人との入れ替え
                    sorted_person = changePerson(sorted_person, i, i - j - 1)

                    # 入れ替えで履歴被りが減ったとき
                    if np.count_nonzero(historyCheck(sorted_person,sorted_work) == 1) < history_count:
                        break

            # 最初の人（下にしか人がいない）
            elif i == 0:
                # 人リストの端から端まで
                for j in range(num_person - 1):
                    # 上の人との入れ替え
                    sorted_person = changePerson(sorted_person, i, i + j + 1)

                    # 入れ替えで履歴被りが減ったとき
                    if np.count_nonzero(historyCheck(sorted_person, sorted_work) == 1) < history_count:
                        break

            # 上下に人がいる人
            else:
                change_distance = 1  # 入れ替え先との距離
                while(True):
                    # 下の人との入れ替え可能かどうか
                    if i + change_distance < num_person:
                        # 下の人との入れ替え
                        sorted_person = changePerson(sorted_person, i, i + change_distance)

                        # 入れ替えで履歴被りが減ったとき
                        if np.count_nonzero(historyCheck(sorted_person, sorted_work) == 1) < history_count:
                            break
                    # 上の人との入れ替え可能かどうか
                    elif i - change_distance >= 0:
                        # 上の人との入れ替え
                        sorted_person = changePerson(sorted_person, i, i - change_distance)

                        # 入れ替えで履歴被りが減ったとき
                        if np.count_nonzero(historyCheck(sorted_person, sorted_work) == 1) < history_count:
                            break
                        else:
                            change_distance += 1
                    # 入れ替えがもうできないとき
                    # 探索終了
                    else:
                        break

    return sorted_person


# 重み更新関数
def updateWeight(copy_person, copy_work, role_table):
    print(copy_person)
    print(copy_work)
    for i in range(len(role_table)):
        role_person = role_table[i][1]
        role_work = role_table[i][0]

        print(role_person)
        now_p = [dic_person for key_person, dic_person in copy_person.items() if dic_person['name'] == role_person]
        now_w = [dic_work for key_work, dic_work in copy_work.items() if dic_work['name'] == role_work]
        print(now_p)
        print(now_w)

        now_p[0]['exp'] += now_w[0]['weight']   # 重み更新
        now_p[0]['history'] = now_w[0]['name']  # history更新
        print(now_p)

    return copy_person

def selectMember(person_list, work_list):
    '''===人数と仕事の数が一致するように予備を追加===
    person_list  [dic] : 今日の仕事できる人の辞書リスト(return exp,history更新後),
    work_list    [dic] : 今日の仕事場所の辞書リスト,
    role_table   [list(str)] : 分担表(return)
    ======================'''
    copy_person = copyArray(person_list)
    copy_work = copyArray(work_list)

    #予備追加
    copy_work = addJobless(copy_person, copy_work)

    # 人を仕事量順でソート(少ない順)
    p_value = [dic for key, dic in copy_person.items()]
    sorted_person = sorted(p_value, key=itemgetter('exp'))

    # 仕事を仕事量順でソート(重い順)
    w_value = [dic for key, dic in copy_work.items()]
    sorted_work = sorted(w_value, key=itemgetter('weight'), reverse=True)

    # ここから仕事の割り当て
    sorted_person = reSorted(sorted_person, sorted_work)
    sorted_work_list = [sort_w['name'] for sort_w in sorted_work for _ in range(sort_w['need'])]
    role_table = [[sorted_w, sorted_p['name']] for sorted_p, sorted_w in zip(sorted_person, sorted_work_list)]
    print(role_table)

    # 関数起動部
    p_key = [nameSearch(person['name'], copy_person) for person in sorted_person]
    copy_person = dict(zip(p_key, sorted_person))
    copy_person = updateWeight(copy_person, copy_work, role_table)

    return role_table, copy_person


if __name__ == "__main__":
    person_list = dict()
    work_list = dict()
    history = []
    totalnum = 2

    person_l = dict()


    # テスト用
    person_list = registerPerson('Aさん', 5, 'pointE', person_list)
    person_list = registerPerson('Bさん', 6, 'pointC', person_list)
    person_list = registerPerson('Cさん', 9, 'pointG', person_list)
    person_list = registerPerson('Dさん', 4, 'pointA', person_list)
    person_list = registerPerson('Eさん', 2, 'pointC', person_list)
    person_list = registerPerson('Fさん', 3, 'pointD', person_list)
    person_list = registerPerson('Gさん', 8, 'pointF', person_list)
    person_list = registerPerson('Hさん', 6, 'pointB', person_list)
    person_list = registerPerson('Iさん', 7, 'pointE', person_list)
    person_list = registerPerson('Jさん', 1, 'pointD', person_list)
    person_list = registerPerson('Kさん', 5, 'pointF', person_list)
    work_list = registerWork('pointA', 2, 1, work_list)
    work_list = registerWork('pointB', 5, 1, work_list)
    work_list = registerWork('pointC', 3, 2, work_list)
    work_list = registerWork('pointD', 4, 2, work_list)
    work_list = registerWork('pointE', 2, 1, work_list)
    work_list = registerWork('pointF', 1, 2, work_list)
    work_list = registerWork('pointG', 1, 1, work_list)

    role, person = selectMember(person_list, work_list)

    #予備追加
    work_list = addJobless(person_list, work_list)

    copy_person = copyArray(person_list)
    copy_work = copyArray(work_list)


    # 仕事量順でソート
    p_value = [dic for key, dic in copy_person.items()]
    sorted_person = sorted(p_value, key=itemgetter('exp'))

    w_value = [dic for key, dic in copy_work.items()]
    sorted_work = sorted(w_value, key=itemgetter('weight'), reverse=True)




    # ここから仕事の割り当て
    re_sorted_person = reSorted(sorted_person, sorted_work)


    # 関数起動部
    # copy_person=updateWeight(copy_person, copy_work, role_table)
