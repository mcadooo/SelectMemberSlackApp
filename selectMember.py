# -*- coding: utf-8 -*-
"""
Created on Fri May 27 18:53:49 2022

@author: shimalab
"""
import numpy as np
import random as ran


#class MemberSelect:

member = []

N = len(member)     # メンバー数

func = []

K = len(func)     #役割数


# 役割の決定
Max_Ite = 60                  # 日数設定
flag = np.zeros(N)             # フラグ用(被らないように)
result = np.zeros([Max_Ite,K])      # 結果格納用(数値)
output=[]                    #ファイル出力用(名前)
All=[]
hold=[]

#回数分ループ
for Ite in range(Max_Ite):
    
    #役割数分ループ
    for k in range(K):
        #while(flag0 < 1):
           n = ran.randint(0,N-1)
           

           if flag[n]==0:
               # まだ選ばれていない場合
               result[Ite,k] = n

               hold.append(member[n])
               flag[n] = 1        # フラグを立てる
              

    output.append(hold.copy())
    
    hold.clear()
    flag = np.zeros(N)             # フラグ用(被らないように)
    
    
#最終出力
output.insert(0,func)
