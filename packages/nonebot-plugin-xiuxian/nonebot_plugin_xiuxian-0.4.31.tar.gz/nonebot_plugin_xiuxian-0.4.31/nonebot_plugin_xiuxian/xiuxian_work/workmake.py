from .reward_data_source import *
import random

def workmake(level, exp):
    jsondata = reward()
    yaocaidata = jsondata.reward_yaocai_data()
    levelpricedata = jsondata.reward_levelprice_data()
    anshadata = jsondata.reward_ansa_data()
    zuoyaodata = jsondata.reward_zuoyao_data()
    spoilsdata = jsondata.reward_spoils_data()
    workjson = {}
    worklist = [yaocaidata[level], anshadata[level], zuoyaodata[level]]
    i = 1
    for w in worklist:
        workname = random.choice(w)
        levelpricedata_temp = random.choice(levelpricedata[level])
        rate, isOut = countrate(exp, levelpricedata_temp["needexp"])
        spoilsdata_temp = random.choice(spoilsdata[level])
        print(f'{i}、寻找{workname},完成几率{rate},报酬{levelpricedata_temp["award"]}灵石,预计需{int(levelpricedata_temp["time"] * isOut)}分钟,可能获取额外{spoilsdata_temp}')
        workjson[workname] = [rate, levelpricedata_temp["award"], int(levelpricedata_temp["time"] * isOut), spoilsdata_temp]
        i += 1
    
    jsondata = json.dumps(workjson, ensure_ascii=False)
    
    return workjson

def countrate(exp, needexp):
    rate = int(exp / needexp * 100)
    isOut = 1
    if rate >= 100:
        i = 1
        flag = True
        while(flag):
            r = exp / needexp * 100
            if r > 100:
                i += 1
                exp /= 1.5
            else:
                flag = False
                
        rate = 100
        isOut = float(1 - i * 0.05)
        if isOut < 0.5:
            isOut = 0.5
    return rate, round(isOut, 2)
