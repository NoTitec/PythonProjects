import requests
import pymysql
import json
from bs4 import BeautifulSoup

baseURL = "https://www.10000recipe.com/recipe/"


def PageCrawler(recipeurl):
    url = baseURL + recipeurl

    page = requests.get(url)
    soup = BeautifulSoup(page.content.decode('UTF-8', 'replace'), 'html.parser')

    recipe_title = []
    recipe_source = {}
    recipe_step = {}
    recipe_image = []

    try:
        res = soup.find('div', 'view2_summary')
        res = res.find('h3')
        recipe_title.append(res.get_text())
        res = soup.find('div', 'view2_summary_info')
        # recipe_title.append(res.get_text().replace('\n',' '))

        res = soup.select_one('#main_thumbs')
        recipe_image.append(res['src'])


    except(AttributeError):
        return

    try:
        res = soup.find('div', 'ready_ingre3')
        n = res.find('ul')

        source = []
        title = '[재료]'
        recipe_source[title] = ''

        for tmp in n.find_all('li'):

            # 조건문 추가 (비어있는 케이스가 존재함)

            tempSource = tmp.get_text().replace('\n', '').replace(' ', ' ')

            if tempSource == ' ' or tempSource == '':
                continue

            sourceName = tempSource.split("                                                        ")[0]
            sorceCount = tempSource.split("                                                        ")[1]
            source.append(sourceName + "," + sorceCount)

        recipe_source[title] = source
    except (AttributeError):
        return

    try:
        countstep = 1
        x = 1
        stedivs = "view_step_cont media step" + str(countstep)
        while True:  # calulate all step number

            res = soup.find('div', stedivs)

            if res is None:
                break
            else:
                countstep = countstep + 1
                stedivs = "view_step_cont media step" + str(countstep)

        while x < countstep:
            step = []
            stepc = str(x)
            recipe_step[stepc] = ""
            stedivs = "view_step_cont media step" + str(x)
            res = soup.find('div', stedivs)
            tempres = res.find_all('br')
            brcount = len(tempres)
            if brcount == 0:
                tempstep = res.get_text()
                step.append(tempstep.split("    ")[0])
                recipe_step[stepc] = step
            else:
                for tmp in res.find_all('br'):
                    tempstep = res.get_text().replace('\n', '').replace(' ', ' ')
                    step.append(tempstep.split("    ")[0])
                recipe_step[stepc] = step
            x = x + 1;

    except(AttributeError):
        return

    recipe_all = [recipe_title, recipe_source, recipe_step, recipe_image]  # 제목, 재료

    return (recipe_all)


def CrawlingBetweenRanges(startRecipeid, endRecipeid):
    for i in range(startRecipeid, endRecipeid):
        if i % 1000 == 0:
            print("count:" + str(i))
        res = PageCrawler(str(i))
        if res is None:
            continue
        else:

            # print(res)

            # DB에 값 넣는 부분
            foodName = res[0][0]
            link = res[3][0]
            dict_ingredient = res[1]
            dict_foodstep = res[2]

            # foods테이블 추가
            mysql_controller.insert_foods(foodName, link)

            # foodstep테이블 추가
            mysql_controller.insert_foodstep(foodName, dict_foodstep)

            # ingredient 테이블 추가
            mysql_controller.insert_Ingredient(dict_ingredient)

            # requiredmaterials 테이블 추가
            mysql_controller.insert_requiredmaterials(foodName, dict_ingredient)

            print(str(i) + "번째 페이지 성공... (" + foodName + ")")


class MysqlController:
    def __init__(self, host, id, pw, db_name):
        try:
            self.conn = pymysql.connect(host=host, user=id, password=pw, db=db_name, charset='utf8')
            self.curs = self.conn.cursor(pymysql.cursors.DictCursor)
        except self.conn.DatabaseError as e:
            print(e)
            self.conn.close()

    def insert_foods(self, foodName, link):
        try:
            sql = 'Insert into foods(foodName, imgLink) VALUE (%s, %s)'
            self.curs.execute(sql, (foodName, link))
            self.conn.commit()
            return self.curs.lastrowid
        except self.conn.DatabaseError as e:
            print(e)

    def insert_foodstep(self, foodName, dict_foodstep):
        try:

            # 먼저 select문으로 foodNum을 찾는다.
            # 중복데이터 존재시 낮은 번호를 가져옴
            sql = 'SELECT foodNum FROM foods WHERE foodName = %s'

            self.curs.execute(sql, (foodName))
            foodNum = self.curs.fetchone()
            foodNum = foodNum['foodNum']

            for i in range(1, len(dict_foodstep) + 1):
                step = dict_foodstep.get(str(i))[0]
                sql = 'Insert into foodstep(foodNum, Step) VALUE (%s, %s)'
                self.curs.execute(sql, (foodNum, step))
                self.conn.commit()
            return self.curs.lastrowid
        except self.conn.DatabaseError as e:
            print(e)

    def insert_Ingredient(self, dict_ingredient):
        try:
            list_ingredient = dict_ingredient.get('[재료]')

            for i in range(len(list_ingredient)):
                ingredient_name = list_ingredient[i].split(',')[0]
                sql = 'SELECT * FROM ingredient where IngredientName = %s'
                self.curs.execute(sql, (ingredient_name))
                temp = self.curs.fetchall()

                if len(temp) == 0:  # 재료 테이블에 없을때만 추가
                    link = "https://www.coupang.com/np/search?component=&q=" + ingredient_name + "+&channel=user"
                    sql = 'Insert into ingredient(ingredientlink, ingredientName) values (%s, %s)'
                    self.curs.execute(sql, (link, ingredient_name))
                    self.conn.commit()

            return self.curs.lastrowid

        except self.conn.DatabaseError as e:
            print(e)

    def insert_requiredmaterials(self, foodName, dict_ingredient):
        try:

            # 먼저 select문으로 foodNum을 찾는다.
            # 중복데이터 존재시 낮은 번호를 가져옴
            sql = 'SELECT foodNum FROM foods WHERE foodName = %s'

            self.curs.execute(sql, (foodName))
            foodNum = self.curs.fetchone()
            foodNum = foodNum['foodNum']

            list_ingredient = dict_ingredient.get('[재료]')

            for i in range(len(list_ingredient)):
                ingredient_name = list_ingredient[i].split(',')[0]
                ingredient_amount = list_ingredient[i].split(',')[1]

                sql = 'SELECT IngredientNumber FROM ingredient WHERE IngredientName = %s'
                self.curs.execute(sql, (ingredient_name))
                ingredientNum = self.curs.fetchone()
                ingredientNum = ingredientNum['IngredientNumber']

                sql = 'Insert into requiredmaterials(foodNum, IngredientNumber, IngredientAmount) values (%s, %s, %s)'
                self.curs.execute(sql, (foodNum, ingredientNum, ingredient_amount))
                self.conn.commit()

            return self.curs.lastrowid

        except self.conn.DatabaseError as e:
            print(e)


# main
mysql_controller = MysqlController('localhost', 'root', 'root', 'recommendfood')

CrawlingBetweenRanges(6950002,7000000) #10만개 시도 예정

#CrawlingBetweenRanges(6881851, 6950001)