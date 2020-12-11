from bs4 import BeautifulSoup
import requests
import html5lib
import psycopg2

html = requests.get("https://salon.av.by/catalog").text
soup = BeautifulSoup(html, 'html5lib')

def get_autos():
    autos = [(li.a.get('href'), li.a.text)
             for div1 in soup('div', {'class' : 'outer'})
             for div2 in div1('div', {'class' : 'inner m-top'})
             for div3 in div2('div', {'class' : 'col-2 col-2-nobd'})
             for div4 in div3('div', {'class' : 'col-c'})
             for div5 in div4('div', {'class' : 'col-i'})
             for div6 in div5('div', {'class' : 'b-sub-nav b-sub-nav-pd b-sub-nav-pd3 coll5'})
             for div7 in div6('div', {'class' : 'b-lists'})
             for ul in div7('ul')
             for li in ul('li', {'data-popular' : '1'})]
    return autos

def get_model_in_autos(auto):
    html = requests.get(auto).text
    soup = BeautifulSoup(html, 'html5lib')
    models = [(li.a.get('href'), li.a.span.text)
              for div1 in soup('div', {'class' : 'outer'})
              for div2 in div1('div', {'class' : 'inner m-top'})
              for div3 in div2('div', {'class' : 'col-2 col-2-nobd'})
              for div4 in div3('div', {'class' : 'col-c'})
              for div5 in div4('div', {'class' : 'col-i'})
              for div6 in div5('div', {'class' : 'b-widget vendor_models'})
              for div7 in div6('div', {'class' : 'tab-content'})
              for div8 in div7('div', {'id' : 'tab-all'})
              for ul in div8('ul')
              for li in ul('li', {'is_new' : 1})]
    return models

def get_model_gens_in_auto(model):
    html = requests.get(model).text
    soup = BeautifulSoup(html, 'html5lib')
    model_gens = [(li.a.get('href'), li.a.get('title'))
                for div1 in soup('div', {'class' : 'outer'})
                for div2 in div1('div', {'class' : 'inner m-top'})
                for div3 in div2('div', {'class' : 'col-2 col-2-nobd'})
                for div4 in div3('div', {'class' : 'col-c'})
                for div5 in div4('div', {'class' : 'col-i'})
                for dl in div5('dl')
                for dd in dl('dd')
                for ul in dd('ul')
                for li in ul('li', {'is_new' : '0'})]
    return model_gens

def get_model_engine(model_gen):
    html = requests.get(model_gen).text
    soup = BeautifulSoup(html, 'html5lib')
    model_gen_specs = [(a.get('href'), a.text)
                        for div1 in soup('div', {'class' : 'outer'})
                        for div2 in div1('div', {'class' : 'inner grid'})
                        for div3 in div2('div', {'class' : 'col-2 col-2-nobd'})
                        for div4 in div3('div', {'class' : 'col-c'})
                        for div5 in div4('div', {'class' : 'col-i'})
                        for div6 in div5('div', {'id' : 'compare'})
                        for table in div6('table')
                        for tbody in table('tbody')
                        for tr in tbody('tr')
                        for td in tr('td', {'class' : 'col2 model-name'})
                        for a in td('a')]
    return model_gen_specs

def get_model_img(model_gen):
    html = requests.get(model_gen).text
    soup = BeautifulSoup(html, 'html5lib')
    model_gen_img = [(a.get('href'))
                     for div1 in soup('div', {'class' : 'outer'})
                     for div2 in div1('div', {'class' : 'inner grid nopd image-viewer__wrapper'})
                     for div3 in div2('div', {'class' : 'col-3 image-viewer'})
                     for div4 in div3('div', {'class' : 'thumb-slide-list'})
                     for div5 in div4('div', {'class' : 'thumb-slide-overview'})
                     for div6 in div5('div', {'class' : 'thumb-slide'})
                     for span in div6('span', {'itemprop' : 'associatedMedia'})
                     for a in span('a')]
    return model_gen_img

def get_specs(model_engine):
    html = requests.get(model_engine).text
    soup = BeautifulSoup(html, 'html5lib')
    mas = [tbody
           for div1 in soup('div', {'class' : 'outer'})
           for div2 in div1('div', {'class' : 'inner nopd'})
           for div3 in div2('div', {'class' : 'col-2 col-2-nobd'})
           for div4 in div3('div', {'class' : 'col-c'})
           for div5 in div4('div', {'class' : 'col-i m-characteristics'})
           for table in div5('table')
           for tbody in table('tbody')]
    data = []
    for i in range(14):
        data.append('-1')
    f = False
    for tbody in mas:
        for tr in tbody('tr'):
            res = [td.text for td in tr('td')]
            if res[0] == 'Длина': #0
                data[0] = res[1]
            elif res[0] == 'Ширина': #1
                data[1] = res[1]
            elif res[0] == 'Высота': #2
                data[2] = res[1]
            elif res[0] == 'Колёсная база': #3
                data[3] = res[1]
            elif (res[0] == 'Минимальный объём багажника' or res[0] == 'Максимальный объём багажника') and f != True: #4
                data[4] = res[1]
                f = True
            elif res[0] == 'Время разгона до 100 км/ч': #6
                data[5] = res[1]
            elif res[0] == 'Расход топлива в смешанном цикле': #7
                data[6] = res[1]
            elif res[0] == 'Тип двигателя': #8
                data[7] = res[1]
            elif res[0] == 'Объем двигателя в литрах': #10
                data[8] = res[1]
            elif res[0] == 'Максимальная мощность': #11
                data[9] = res[1]
            elif res[0] == 'Максимальный крутящий момент': #12
                data[10] = res[1]
            elif res[0] == 'Коробка передач': #13
                data[11] = res[1]
            elif res[0] == 'Количество передач': #14
                data[12] = res[1]
            elif res[0] == 'Привод': #15
                data[13] = res[1]
    return data

def update_data(mas):
    data = []
    for z in mas:
        str = ''
        for i in range(len(z)):
            if z[i] == ' ':
                break
            str += z[i]
        data.append(str)
    return data

def update_img_data(model_gen_img):
    img_data = []
    for i in range(8):
        if len(model_gen_img) <= i:
            img_data.append('-')
            continue
        img_data.append(model_gen_img[i])
    return img_data

def get_years(model_gen):
    html = requests.get(model_gen).text
    soup = BeautifulSoup(html, 'html5lib')
    year = [(meta.get('content'))
                for div1 in soup('div', {'class': 'outer'})
                for div2 in div1('div', {'class': 'inner grid nopd'})
                for div3 in div2('div', {'class': 'col-2 col-2-nobd'})
                for div4 in div3('div', {'class': 'col-c'})
                for div5 in div4('div', {'class': 'col-i m-social_top'})
                for div6 in div5('div', {'class': 'header'})
                for div7 in div6('div', {'class': 'dropdown_model_container'})
                for div8 in div7('div')
                for a in div8('a')
                for meta in a('meta')]
    if len(year) >= 3:
        return year[2]
    else:
        return '0'



connection = psycopg2.connect(host="localhost", port="5432", database="cars", user="postgres", password="1234")
cursor = connection.cursor()
cursor.execute("CREATE TABLE brands(brand_id SERIAL PRIMARY KEY, name TEXT)")
cursor.execute("CREATE TABLE models(model_id SERIAL PRIMARY KEY, name TEXT, brand_id INTEGER)")
cursor.execute("CREATE TABLE model_gen(gen_id SERIAL PRIMARY KEY, name TEXT, year TEXT, model_id INTEGER, "
                "length INTEGER, width INTEGER, height INTEGER, wheelbase INTEGER, trunk_volume INTEGER)")
cursor.execute("CREATE TABLE model_engine(engine_id SERIAL PRIMARY KEY, name TEXT, "
                "gen_id INTEGER, engine_type TEXT, engine_capacity TEXT, engine_horsepower INTEGER, engine_torque INTEGER, "
                "acceleration_0_100 REAL, combined_fuel_economy REAL, gearbox_name_full TEXT, gearbox_speed INTEGER, "
                "drivegear TEXT)")
cursor.execute("CREATE TABLE model_img(model_gen_id INTEGER, img1 TEXT, img2 TEXT, img3 TEXT, "
               "img4 TEXT, img5 TEXT, img6 TEXT, img7 TEXT, img8 TEXT)")
autos = get_autos()
for auto, auto_name in autos:
    cursor.execute("INSERT INTO brands (name) VALUES (%s);", (auto_name,))
    models = get_model_in_autos(auto)
    cursor.execute("SELECT * FROM brands WHERE name=%s", (auto_name,))
    connection.commit()
    result = cursor.fetchall()
    BRAND_id = result[0][0]
    for model, model_name in models:
        cursor.execute("INSERT INTO models (name, brand_id) VALUES (%s, %s)", (model_name, BRAND_id,))
        connection.commit()
        model_gens = get_model_gens_in_auto(model)
        cursor.execute("SELECT * FROM models WHERE name=%s", (model_name,))
        result = cursor.fetchall()
        MODEL_id = result[0][0]
        print(model_name)
        for model_gen, model_gen_name in model_gens:
            year = get_years(model_gen)
            model_gen_engine = get_model_engine(model_gen)
            model_gen_img = get_model_img(model_gen)
            if len(model_gen_engine) != 0:
                flag = False
                for gen_specs, name_engine in model_gen_engine:
                    data = update_data(get_specs(gen_specs))
                    if flag == False:
                        cursor.execute("INSERT INTO model_gen (name, year, model_id, length, width, height, wheelbase, trunk_volume)"
                                    " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                                    (model_gen_name, year, MODEL_id, int(data[0]), int(data[1]), int(data[2]),
                                    int(data[3]), int(data[4]),))
                        connection.commit()
                        cursor.execute("SELECT * FROM model_gen WHERE name=%s", (model_gen_name,))
                        result = cursor.fetchall()
                        MODEL_gen_id = result[0][0]
                        img_data = update_img_data(model_gen_img)
                        cursor.execute("INSERT INTO model_img (model_gen_id, img1, img2, img3, img4, img5, img6, img7, img8)"
                                        " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (int(MODEL_gen_id), img_data[0],
                                        img_data[1], img_data[2], img_data[3], img_data[4], img_data[5], img_data[6], img_data[7],))
                        connection.commit()
                        flag = True
                        cursor.execute("SELECT * FROM model_gen WHERE name=%s", (model_gen_name,))
                        result = cursor.fetchall()
                        MODEL_GEN_id = result[0][0]
                    cursor.execute("INSERT INTO model_engine (name, gen_id, engine_type, engine_capacity, engine_horsepower, "
                                "engine_torque, acceleration_0_100, combined_fuel_economy, gearbox_name_full, "
                                "gearbox_speed, drivegear) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                                (name_engine, MODEL_GEN_id, data[7], data[8], int(data[9]), int(data[10]),
                                float(data[5]), float(data[6]), data[11], int(data[12]), data[13],))
                    connection.commit()
        cursor.execute("SELECT * FROM model_gen WHERE model_id=%s", (MODEL_id,))
        result = cursor.fetchall()
        if len(result) == 0:
            print('!!!!!!!!!!!!!!!!!')
            cursor.execute("DELETE FROM models WHERE model_id=%s", (MODEL_id,))
connection.close()
