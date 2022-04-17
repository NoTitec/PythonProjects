import requests
import pymysql
import json
from bs4 import BeautifulSoup

baseURL="https://www.10000recipe.com/recipe/"

def PageCrawler(recipeurl):
    url=baseURL+recipeurl

    page=requests.get(url)
    soup=BeautifulSoup(page.content,'html.parser')

    recipe_title=[]
    recipe_source={}
    recipe_step={}
    try:
        res=soup.find('div','view2_summary')
        res=res.find('h3')
        recipe_title.append(res.get_text())
        res=soup.find('div','view2_summary_info')
        recipe_title.append(res.get_text().replace('\n',' '))
    except(AttributeError):
        return

    try:
        res=soup.find('div','ready_ingre3')
        for n in res.find_all('ul'):
            source = []
            title = n.find('b').get_text()
            recipe_source[title] = ''
            for tmp in n.find_all('li'):
                tempSource = tmp.get_text().replace('\n', '').replace(' ', ' ')
                source.append(tempSource.split("    ")[0])

            recipe_source[title] = source
    except (AttributeError):
        return

    try:
        countstep = 1
        x = 1
        stedivs = "view_step_cont media step" + str(countstep)
        while True:  # calulate all step number

            res=soup.find('div',stedivs)

            if res is None :
                break
            else :
                countstep = countstep + 1
                stedivs = "view_step_cont media step" + str(countstep)

        while x<countstep:
            step=[]
            stepc=str(x)
            recipe_step[stepc]=""
            stedivs = "view_step_cont media step" + str(x)
            res=soup.find('div',stedivs)
            tempres=res.find_all('br')
            brcount=len(tempres)
            if brcount==0:
                tempstep=res.get_text()
                step.append(tempstep.split("    ")[0])
                recipe_step[stepc] = step
            else:
                for tmp in res.find_all('br'):
                    tempstep = res.get_text().replace('\n', '').replace(' ', ' ')
                    step.append(tempstep.split("    ")[0])
                recipe_step[stepc] = step
            x=x+1;

    except(AttributeError):
        return

    recipe_all = [recipe_title, recipe_source,recipe_step]  # 제목, 재료

    return (recipe_all)

def CrawlingBetweenRanges(mydb,startRecipeid,endRecipeid):
    for i in range(startRecipeid,endRecipeid):
        if i%1000==0:
            print("count:"+str(i))
        res=PageCrawler(str(i))
        if res is None:
            continue
        else :
            print(res)
            #재료
            ing= res[1]
            realkey=list(ing.keys())[0]
            value=ing[realkey]
            ingresult=' '.join(s for s in value)
            #조리순서
            stepd=res[2]
            stepcount=len(stepd.keys())
            onestepcount=len(stepd.values())
            stempkey=list(stepd.keys())
            stempvalue=list(stepd.values())
            finalstr=''
            for j in range(stepcount):
                finalstr+=stempkey[j]
                finalstr+=' :'
                for k in range(onestepcount):
                    finalstr+=''.join(stempvalue[k])
            #print(res[0][0]);print(ingresult);print(finalstr);print(type(res[0][0]));print(type(ingresult));print(type(finalstr))
            menuid=mydb.insert_menu(res[0][0],ingresult,finalstr,baseURL+str(i))
            print(menuid)


class MysqlController:
    def __init__(self,host,id,pw,db_name):
        try:
           self.conn=pymysql.connect(host=host,user=id,password=pw,db=db_name,charset='utf8')

        except self.conn.DatabaseError as e:
            print(e)
            self.conn.close()
    def insert_menu(self,mname,mingredient,mstep,url):
        try:
            with self.conn.cursor() as cursor:
                sql='insert into food.foods (food_name,food_ingredient,food_step,food_link) values (%s, %s, %s, %s)'
                cursor.execute(sql,(mname,mingredient,mstep,url))
            self.conn.commit()
            return cursor.lastrowid
        except self.conn.DatabaseError as e:
            print(e)


mydb=MysqlController('localhost','root','root','food')
CrawlingBetweenRanges(mydb,1460120,7000000)
#CrawlingBetweenRanges(mydb,6900000,7000000)