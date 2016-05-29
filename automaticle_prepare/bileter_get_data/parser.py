# -*_ coding: utf-8 -*-

import copy
import datetime
import json
import os
import pickle
import sys
import time
import urllib2

from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

# duration на сайте

# разобраться с discription

domain = 'http://www.bileter.ru'

event_categories = [
    ('theater', 'type1', 'Театры'),  # 1
    ('concert', 'type2', 'Концерты'),  # 3
    ('show', 'type3', 'Шоу'),  # 3
    ('clubs', 'type4', 'Клубы'),  # 4
    ('kids', 'type5', 'Детские мероприятия'),  # 5
    ('excursions', 'type6', 'Экскурсии'),  # 6
    ('exhibition', 'type7', 'Выставки'),  # 7
    ('sport', 'type9', 'Спорт'),  # 8
]

event_categories_list = ['theater', 'concert', 'show', 'clubs', 'kids', 'excursions', 'exhibition', 'sport']

page_conv = lambda n: "/list%d" % n


def get_coordinates(address):
    url_yandex = "http://geocode-maps.yandex.ru/1.x/?format=json&geocode=" + address
    response = urllib2.urlopen(url_yandex)
    data = json.load(response)
    coord = ""
    try:
        coord = data[u'response'][u'GeoObjectCollection'][u'featureMember'][0][u'GeoObject'][u'Point'][u"pos"]
    except:
        return 0

    coord_split = coord.split(" ")

    latitude = float(coord_split[1])
    longitude = float(coord_split[0])

    return latitude, longitude


def get_today_data():
    today_date = datetime.date.today()
    return today_date


def get_need_time(num_days):
    today_date = get_today_data()
    delta = datetime.timedelta(days=1)
    last_date = today_date
    date_array_out = []
    date_array_out.append(str(today_date))
    for i in xrange(num_days - 1):
        date = last_date + delta
        date_array_out.append(str(date))
        last_date = date

    return date_array_out


def make_request(url, delay=2):
    time.sleep(delay)
    headers = {'User-agent': "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}
    request = urllib2.Request(url, None, headers)
    request.add_header('Accept-Encoding', 'utf-8')
    return urllib2.urlopen(request)


def parse_events(date):
    parsed_data = []

    for cat_eng, cat_type, cat_rus, in event_categories:
        i_page = 0
        url = domain + '/afisha/' + cat_type + "/" + date + "/list" + str(i_page + 1) + ".html"
        try:
            soup = BeautifulSoup(make_request(url))
        except:
            continue

        try:
            # проверить
            n_pages = soup.find(class_="page_nav").findAll('li')[-2].string
            n_pages = int(n_pages)
        except:
            n_pages = 1

        return_checker = 0
        while i_page != n_pages:
            url = domain + '/afisha/' + cat_type + "/" + date + "/list" + str(i_page + 1) + ".html"
            print url

            try:
                soup = BeautifulSoup(make_request(url))
                afisha_events_item = soup.find_all(class_='middle_part')
            except:
                continue

            for event in afisha_events_item:
                parsed_event = {}
                parsed_event['categories'] = cat_eng
                parsed_event['categoriesrus'] = cat_rus

                try:
                    title = event.find(class_='mp_news_item_text').find('h2').find('a')['title']
                    parsed_event['title'] = str(title)
                except Exception as inst:
                    continue

                try:
                    ticket = event.find(class_='bt_buy fr')['href']
                    parsed_event['ticket'] = str(domain + ticket)
                except:
                    parsed_event['ticket'] = "no"

                try:
                    place_url = event.find(class_='place_title').a['href']
                    place_url = domain + place_url
                except:
                    continue

                try:
                    event_url = event.find(class_='mp_news_item_text').a['href']
                    event_url = domain + event_url
                    parsed_event['url'] = str(event_url)
                except:
                    continue

                try:
                    # переход на страницу места проведения события
                    place_soup = BeautifulSoup(make_request(place_url))
                    address = place_soup.find(class_='event_nav_item nav_place').find('span').string
                    parsed_event['address'] = str(address)
                except:
                    continue

                try:
                    # переход на страницу события
                    event_soup = BeautifulSoup(make_request(event_url))
                    time = event_soup.find(class_='event_nav_item nav_date').find('span').string
                    time = ' '.join(str(time).split())
                    parsed_event['display_dates_string'] = time
                except:
                    continue

                try:
                    description = event_soup.find(class_='event_bigtext').text
                    description = ' '.join(str(description).split())
                    parsed_event['description'] = description
                except:
                    parsed_event['description'] = "no"

                try:
                    duration_time = event_soup.find(itemprop="duration").string
                    parsed_event['duration'] = str(duration_time)
                except:
                    parsed_event['duration'] = "no"

                try:
                    image = event_soup.find(class_='event_image fl').findAll('img')[0].attrs['src']
                    parsed_event['images'] = str(image)
                except:
                    parsed_event['images'] = "no"

                parsed_data.append(copy.deepcopy(parsed_event))
            return_checker += 1

            if (return_checker == 50):
                return []

            i_page += 1

    return parsed_data


def parsing(time_array_need):
    counter = 0
    array_need_time = copy.deepcopy(time_array_need)

    bileter_data = []

    for index, i in enumerate(array_need_time):
        day_array = []
        day_array = parse_events(i)

        for k in xrange(len(day_array)):
            day_array[k]['fixedtime'] = True
            day_array[k]['rank'] = 1
            day_array[k]['phone'] = "no"

            try:
                latitude, longitude = get_coordinates(day_array[k]['address'])
            except:
                try:
                    latitude, longitude = get_coordinates("Санкт-Петербург, " + day_array[k]['address'])

                    split_address = day_array[k]['address'].split(" ")
                    if (len(split_address) != 0):
                        if (split_address[0] != u"Санкт-Петербург,"):
                            day_array[k]['address'] = "Санкт-Петербург, " + day_array[k]['address']
                except Exception as inst:
                    print inst
                    continue

            day_array[k]['latitude'] = latitude
            day_array[k]['longitude'] = longitude

        bileter_data.append(copy.deepcopy(day_array))

    path = os.path.dirname(os.path.abspath(__file__)) + "/data/"

    output = open(path + "bileter.pkl", 'w')

    pickle.dump(bileter_data, output)

    output.close()
