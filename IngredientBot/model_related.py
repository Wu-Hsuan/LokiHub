#!/user/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import logging
import pandas as pd
from random import choice
from datetime import datetime

import ingredientBot as iB

inSeasonDICT = json.load(open("./info/inSeason.json", encoding="utf-8")) 
IngredientRelatedDICT = json.load(open("./info/ingredient.json", encoding="utf-8"))


def checkInSeason(ingredient):
    currentMonth = datetime.now().month
    ingr_inseasonLIST = inSeasonDICT[str(currentMonth)+"月"]

    if ingredient in ingr_inseasonLIST["蔬菜"]+ingr_inseasonLIST["水果"]+ingr_inseasonLIST["海鮮"]:
        return True
    else:
        return False

def inSeason(rejectLIST, time, type):
    if time in ["現在", "目前", "今天"]:
        month = str(datetime.now().month)+"月"
    elif "1月" in time or "一月" in time:
        month = "1月"
    elif "2月" in time or "二月" in time:
        month = "2月"
    elif "3月" in time or "三月" in time:
        month = "3月"
    elif "4月" in time or "四月" in time:
        month = "4月"
    elif "5月" in time or "五月" in time:
        month = "5月"
    elif "6月" in time or "六月" in time:
        month = "6月"
    elif "7月" in time or "七月" in time:
        month = "7月"
    elif "8月" in time or "八月" in time:
        month = "8月"
    elif "9月" in time or "九月" in time:
        month = "9月"
    elif "10月" in time or "十月" in time:
        month = "10月"
    elif "11月" in time or "十一月" in time:
        month = "11月"
    elif "12月" in time or "十二月" in time:
        month = "12月"
    else:
        month = str(datetime.now().month)+"月"

    if "蔬菜" in type:
        type = "蔬菜"
    elif "水果" in type:
        type = "水果"
    elif "海鮮" in type:
        type = "海鮮"
    else:
        type = choice(["蔬菜", "水果", "海鮮"])

    ingr_inseasonLIST = inSeasonDICT[month][type]
    ingr_inseason_excludeLIST = [x for x in ingr_inseasonLIST if x not in rejectLIST]

    return choice(ingr_inseason_excludeLIST), month, type

def price(ingredient):
    table = pd.read_html("http://www.tapmc.com.taipei/")
    table[0].columns = ['品名', '品種', '上價', '中價', '下價']

    priceDICT={}
    for index,row in table[0].iterrows():
        tmp=[]
        tmp.append(row["上價"])
        tmp.append(row["中價"])
        tmp.append(row["下價"])
        name = str(row["品名"]) + "(" + str(row["品種"]) + ")"
        priceDICT[name]=tmp

    ingr_priceDICT={}
    for key in priceDICT.keys():
        if ingredient in key:
            ingr_priceDICT[key]=priceDICT[key]

    return ingr_priceDICT

def recipe(ingredient):
    if ingredient in IngredientRelatedDICT:
        return IngredientRelatedDICT[ingredient]["作法"]
    else:
        return {}
    
def taboo(ingredient):
    if ingredient in IngredientRelatedDICT:
        return IngredientRelatedDICT[ingredient]["禁忌"]
    else:
        return {}
    
def selection(ingredient):
    if ingredient in IngredientRelatedDICT:
        return IngredientRelatedDICT[ingredient]["挑法"]
    else:
        return {}

def recommend():
    random_ingr = choice(list(IngredientRelatedDICT.keys()))
    recommend = choice(IngredientRelatedDICT[random_ingr]["作法"])

    return recommend

def which_season(ingredient):
    season = []
    for month in inSeasonDICT.keys():
        for type in inSeasonDICT[month].keys():
            if ingredient in inSeasonDICT[month][type]:
                season.append(month)
    season = sorted(list(set(season)))

    return season

def all_ingr(time, type):
    if time in ["現在", "目前", "今天"]:
        month = str(datetime.now().month)+"月"
    elif "1月" in time or "一月" in time:
        month = "1月"
    elif "2月" in time or "二月" in time:
        month = "2月"
    elif "3月" in time or "三月" in time:
        month = "3月"
    elif "4月" in time or "四月" in time:
        month = "4月"
    elif "5月" in time or "五月" in time:
        month = "5月"
    elif "6月" in time or "六月" in time:
        month = "6月"
    elif "7月" in time or "七月" in time:
        month = "7月"
    elif "8月" in time or "八月" in time:
        month = "8月"
    elif "9月" in time or "九月" in time:
        month = "9月"
    elif "10月" in time or "十月" in time:
        month = "10月"
    elif "11月" in time or "十一月" in time:
        month = "11月"
    elif "12月" in time or "十二月" in time:
        month = "12月"
    else:
        month = str(datetime.now().month)+"月"

    if "蔬菜" in type:
        type = "蔬菜"
    elif "水果" in type:
        type = "水果"
    elif "海鮮" in type:
        type = "海鮮"
    else:
        type = "食材"

    if type == "食材":
        all_ingr_inseasonLIST = inSeasonDICT[month]["蔬菜"] + inSeasonDICT[month]["水果"] + inSeasonDICT[month]["海鮮"]
    else:
        all_ingr_inseasonLIST = inSeasonDICT[month][type]

    return all_ingr_inseasonLIST, month, type


def findIngredient(resultDICT, mscDICT):
    if "ingredient" in resultDICT.keys():
        ingredient = resultDICT["ingredient"]
    else:
        ingredient = mscDICT["ingredient"]   #如果回覆中未提到討厭甚麼食材，以上一次提供的當季食材當作討厭的食材

    return ingredient


def getLokiResult(inputSTR):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")
    filterLIST = []
    resultDICT = iB.runLoki(inputLIST, filterLIST)

    return resultDICT

def model(mscDICT):
    resultDICT = getLokiResult(mscDICT["msgSTR"])
    logging.info("Loki 回傳的結果: {}".format(resultDICT))
    
    if len(resultDICT) > 0: #有找到對應的intent
        #intent = check，想確認這項食材是不是當季
        if "check" in resultDICT.keys():
            ingr = findIngredient(resultDICT, mscDICT)
            
            if checkInSeason(ingr):
                mscDICT["replySTR"] = resultDICT["ingredient"] + "是當季食材沒錯！"
            else:
                mscDICT["replySTR"] = resultDICT["ingredient"] + "不是當季食材哦~"

            #紀錄
            mscDICT["ingredient"] = ingr

        #intent = inseason，想知道現在有哪些當季食材
        if "inseason" in resultDICT.keys():
            if "time" in resultDICT.keys():
                time = resultDICT["time"]
            else:
                time = ""
            if "type" in resultDICT.keys():
                type = resultDICT["type"]
            else:
                type = ""
            
            ingr_inseason, res_time, res_type = inSeason(mscDICT["rejectLIST"], time, type)

            if type == "" or  type == "食材":
                if time == "":
                    mscDICT["replySTR"] = "現在最好吃的是{}哦！".format(ingr_inseason)
                else:
                    mscDICT["replySTR"] = "{}最好吃的是{}哦！".format(res_time, ingr_inseason)
            else:
                if time == "":
                    mscDICT["replySTR"] = "你喜歡吃{}呀？現在最好吃的是{}哦！".format(res_type, ingr_inseason)
                else:
                    mscDICT["replySTR"] = "你喜歡吃{}呀？{}最好吃的是{}哦！".format(res_type, res_time, ingr_inseason)

            #紀錄
            mscDICT["ingredient"] = ingr_inseason
            mscDICT["time"] = res_time
            mscDICT["type"] = res_type

        #intent = reject
        if "reject" in resultDICT.keys():
            reject_ingr = findIngredient(resultDICT, mscDICT)
            mscDICT["rejectLIST"].append(reject_ingr)   #紀錄使用者reject過的食材

            #再提供另一個當季食材
            if mscDICT["time"] == "":
                time = "現在"
            else:
                time = mscDICT["time"]
            
            if mscDICT["type"] == "":
                type = choice(["蔬菜", "水果", "海鮮"])
            else:
                type = mscDICT["type"]

            ingr_inseason, res_time, res_type = inSeason(mscDICT["rejectLIST"], time, type)
            mscDICT["replySTR"] = "那麼" + ingr_inseason + "如何？"

            #紀錄
            mscDICT["ingredient"] = ingr_inseason
            mscDICT["time"] = res_time
            mscDICT["type"] = res_type

        #intent = price，想知道這項食材的價格
        if "price" in resultDICT.keys():
            ingr = findIngredient(resultDICT, mscDICT)
            
            close_time0 = datetime.strptime(str(datetime.now().date())+'0:00', '%Y-%m-%d%H:%M')
            close_time1 =  datetime.strptime(str(datetime.now().date())+'7:30', '%Y-%m-%d%H:%M')
            n_time = datetime.now()
            n_weekday = datetime.today().weekday()

            if n_weekday == 0:
                mscDICT["replySTR"] = "星期一休市"
            
            elif close_time0 < n_time and n_time < close_time1:
                mscDICT["replySTR"] = "食材尚在運送拍賣中"

            else:
                ingr_priceDICT = price(ingr)
                if len(ingr_priceDICT) > 0:
                    replySTR = ""
                    for key in ingr_priceDICT:
                        replySTR = replySTR + key + "的今日價格：{}元(上價)，{}元(中價)，{}元(下價)".format(ingr_priceDICT[key][0], ingr_priceDICT[key][1], ingr_priceDICT[key][2]) + "\n"

                    mscDICT["replySTR"] = replySTR
                else:
                    mscDICT["replySTR"] = "查不到{}的價錢！".format(ingr)

            #紀錄
            mscDICT["ingredient"] = ingr

        #intent = recipe，想知道這項食材有什麼作法
        if "recipe" in resultDICT.keys():
            ingr = findIngredient(resultDICT, mscDICT)
            recipe_result = recipe(ingr)
            if len(recipe_result) > 0:
                recipeGroup = "、".join(recipe_result)
                
                replySTR0 = "{}，這些都是{}的料理，你可以做看看。".format(recipeGroup, ingr)
                replySTR1 = "{}可以這樣料理：{}".format(ingr, recipeGroup)
                replySTR2 = "{}，你想做哪一道{}料理？。".format(recipeGroup, ingr)
                replyLIST = [replySTR0, replySTR1, replySTR2]

                mscDICT["replySTR"] = choice(replyLIST)
            else:
                mscDICT["replySTR"] = "查不到{}的作法！".format(ingr)

            #紀錄
            mscDICT["ingredient"] = ingr

        #intent = taboo
        if "taboo" in resultDICT.keys():
            ingr = findIngredient(resultDICT, mscDICT)
            taboo_result = taboo(ingr)
            if len(taboo_result) > 0:
                mscDICT["replySTR"] = taboo_result
            else:
                mscDICT["replySTR"] = "這邊沒有記載{}的禁忌！".format(ingr)
              
            #紀錄
            mscDICT["ingredient"] = ingr

        #intent = selection
        if "selection" in resultDICT.keys():
            ingr = findIngredient(resultDICT, mscDICT)
            selection_result = selection(ingr)
            if len(selection_result) > 0:
                mscDICT["replySTR"] = selection_result
            else:
                mscDICT["replySTR"] = "查不到{}的挑法！".format(ingr)

            #紀錄
            mscDICT["ingredient"] = ingr

        #intent = recommend
        if "recommend" in resultDICT.keys():
            recommend_result = recommend()
            mscDICT["replySTR"] = "可以試試看{}".format(recommend_result)

        #intent = capability
        if "capability" in resultDICT.keys():
            mscDICT["replySTR"] = "我知道現在的當季食材有什麼，還有一些關於食材的資訊，像是價格、挑選方法或是禁忌，還有它可以做成什麼料理..."

        #intent = which_season
        if "which_season" in resultDICT.keys():
            ingr = findIngredient(resultDICT, mscDICT)
            ws_result = which_season(ingr)
            if len(ws_result) > 0:
                group = "、".join(ws_result)
                mscDICT["replySTR"] = group + "是{}的產季。".format(ingr)
            else:
                mscDICT["replySTR"] = "查不到{}的產季！".format(ingr)

            #紀錄
            mscDICT["ingredient"] = ingr

        #intent = all_ingr，想知道所有當季食材
        if "all_ingr" in resultDICT.keys():
            if "time" in resultDICT.keys():
                time = resultDICT["time"]
            else:
                time = ""
            if "type" in resultDICT.keys():
                type = resultDICT["type"]
            else:
                type = ""

            all_ingrLIST, res_time, res_type = all_ingr(time, type)

            all_ingrGroup = "、".join(all_ingrLIST)
            if type == "":
                if time == "":
                    mscDICT["replySTR"] = "這些全是現在的當季食材：{}".format(all_ingrGroup)
                else:
                    mscDICT["replySTR"] = "這些全是{}的當季食材：{}".format(res_time, all_ingrGroup)
            else:
                if time == "":
                    mscDICT["replySTR"] = "這些全是現在的當季{}：{}".format(res_type, all_ingrGroup)
                else:
                    mscDICT["replySTR"] = "這些全是{}的當季{}：{}".format(res_time, res_type, all_ingrGroup)

        #紀錄本次的intent
        mscDICT["intent"] = []
        for key in resultDICT.keys():
            if key not in ['ingredient', 'time' 'type']:
                mscDICT["intent"].append(key)

    else: #沒有找到對應的intent
        if mscDICT["msgSTR"].lower() in ["哈囉","嗨","你好","您好","hi","hello", "早安", "午安", "晚安", "早", "HIHI"]:
            
            currentMonth = choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
            type = choice(["蔬菜", "水果", "海鮮"])            
            ingr_inseason = choice(inSeasonDICT[str(currentMonth)+"月"][type])

            mscDICT["replySTR"] = "嗨，我是小幫手，你喜歡" + ingr_inseason + "嗎？"

            #紀錄
            mscDICT["ingredient"] = ingr_inseason
            mscDICT["time"] = "現在"
            mscDICT["type"] = type

        #accept
        elif mscDICT["msgSTR"].lower() in ["Ok","了解","好哦","好喔","沒問題","可以", "喜歡", "喜歡ㄟ", "好ㄟ"]:
            if "reject" in mscDICT["intent"]:
                mscDICT["replySTR"] = "你可以問我更多關於{}的資訊哦 ^_^".format(mscDICT["ingredient"])
            else:
                if mscDICT["ingredient"] == "":
                    mscDICT["replySTR"] = "歡迎問我關於食材的問題哦 ^_^"
                else:
                    mscDICT["replySTR"] = "你可以問我更多關於{}的資訊哦 ^_^".format(mscDICT["ingredient"])

        #reject
        elif mscDICT["msgSTR"].lower() in ["討厭", "還有呢"]:
            reject_ingr = findIngredient(resultDICT, mscDICT)
            mscDICT["rejectLIST"].append(reject_ingr)   #紀錄使用者reject過的食材

            #再提供另一個當季食材
            if mscDICT["time"] == "":
                time = "現在"
            else:
                time = mscDICT["time"]
            if mscDICT["type"] == "":
                type = choice(["蔬菜", "水果", "海鮮"])
            else:
                type = mscDICT["type"]

            ingr_inseason, res_time, res_type = inSeason(mscDICT["rejectLIST"], time, type)
            mscDICT["replySTR"] = "那麼" + ingr_inseason + "如何？"

            #紀錄
            mscDICT["ingredient"] = ingr_inseason
            mscDICT["time"] = res_time
            mscDICT["type"] = res_type
            
        else: #DEFAULT
            mscDICT["replySTR"] = choice(["好喔", "Ok", "繼續問我更多食材問題吧"])
    
        #紀錄本次的intent
        mscDICT["intent"] = []

    return mscDICT

