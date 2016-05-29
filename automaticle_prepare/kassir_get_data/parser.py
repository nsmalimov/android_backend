# -*_ coding: utf-8 -*-

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

domain = 'https://spb.kassir.ru/'

event_categories = [
    ('concert', 'categories=c13', 'Концерты'),  # 1
    ('theater', 'categories=c3', 'Театры'),  # 2
    ('show', 'categories=c1', 'Шоу'),  # 3
    ('clubs', 'categories=c25', 'Клубы'),  # 4
    ('kids', 'categories=c8', 'Детские мероприятия'),  # 5
    ('excursions', 'categories=c23', 'Экскурсии'),  # 61
    ('exhibition', 'categories=c22', 'Выставки'),  # 7
    ('sport', 'categories=c11', 'Спорт'),  # 8
]

event_categories_list = ['theater', 'concert', 'show', 'clubs', 'kids', 'excursions', 'exhibition', 'sport']

page_conv = lambda n: "/list%d" % n


def get_today_data():
    today_date = datetime.date.today()
    return today_date


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


def check_slipped(event_date, need_date):
    month_array = [u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября',
                   u'октября', u'ноября', u'декабря']

    date_split = need_date.split(u"-")

    need_date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))

    year = int(date_split[0])

    date_split = event_date.split(" ")
    month = month_array.index(date_split[1]) + 1
    find_date = datetime.date(year, month, int(date_split[0]))

    s = str(find_date - need_date)

    s_split = s.split(" ")

    try:
        num = int(s_split[0])
    except:
        return False

    if (num > 0):
        return True
    else:
        return False


def date_check(event_date, date):
    month_array = [u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября',
                   u'октября', u'ноября', u'декабря']

    date_split = date.split("-")

    month_num = date_split[1]
    if (month_num[0] == "0"):
        month_num = month_num[1]

    month_num = int(month_num)

    month = month_array[month_num - 1]

    if (date_split[2][0] == "0"):
        date_split[2] = date_split[2][1]

    need_date = date_split[2] + " " + month

    if (need_date == event_date):
        return True
    else:
        return False


def parse_events(one_date):
    stop_marker = False
    first_marker = False
    slipped_marker = False

    parsed_data = []

    date_prepare = str(one_date).replace("-", ".")

    date_prepare_split = date_prepare.split(".")

    date_prepare = date_prepare_split[2] + "." + date_prepare_split[1] + "." + date_prepare_split[0]

    for cat_eng, cat_type, cat_rus, in event_categories:
        i_page = 0
        url = domain + 'kassir/search/?date=' + date_prepare + '&' + cat_type + "&page=" + str(i_page + 1)

        try:
            soup = BeautifulSoup(make_request(url))
        except:
            continue

        try:
            # проверить
            n_pages = soup.find(class_='last').a['href']
            n_pages_split = n_pages.split("&page=")
            n_pages = int(n_pages_split[-1])
        except Exception as inst:
            n_pages = 1

        return_checker = 0
        while i_page != n_pages:
            url = domain + 'kassir/search/?date=' + date_prepare + '&' + cat_type + "&page=" + str(i_page + 1)
            print url

            try:
                soup = BeautifulSoup(make_request(url))
                afisha_events_item = soup.find_all(class_='list-view')
            except:
                print url + " error open"
                break

            for event in afisha_events_item:

                # добавить выход из цикла если дата не подходит
                parsed_event = {}
                parsed_event['categories'] = cat_eng
                parsed_event['categoriesrus'] = cat_rus

                try:
                    title = event.find(class_='b-event-item__tile__name').find(class_='double').text
                except:
                    print url + " error title"
                    continue
                parsed_event['title'] = str(title)

                try:
                    ticket = domain + event.find(class_="link-buy")['href']
                except:
                    ticket = "no"
                parsed_event['ticket'] = str(ticket)

                try:
                    event_url = domain + event.find(class_='link')['href']
                except:
                    event_url = "no"
                parsed_event['url'] = str(event_url)

                try:
                    # переход на страницу события
                    event_soup = BeautifulSoup(make_request(event_url))
                    event_date = event_soup.find(class_='event-header__date').find('span').contents[0]
                    stop_marker = date_check(event_date, one_date)
                    slipped_marker = check_slipped(event_date, one_date)
                except:
                    print url + " open event url"
                    continue

                if (slipped_marker):
                    break

                if (stop_marker):
                    first_marker = True

                if (not (first_marker)):
                    continue

                if (not (stop_marker) and first_marker):
                    break

                try:
                    time_event = event_soup.find(class_='event-header__date').find(class_='time').string
                    parsed_event['display_dates_string'] = str(time_event)
                except:
                    print "time event error"
                    continue

                try:
                    description = "".join([node if node else ""
                                           for node in event_soup.find(id='event-description').text])

                    description = ' '.join(str(description).split())
                except Exception as inst:
                    description = "no"
                parsed_event['description'] = description

                try:
                    image = event_soup.find(class_='event-header__image').findAll('img')[0].attrs['src']
                except:
                    image = "no"

                parsed_event['images'] = str(image)

                try:
                    place_url = domain + event_soup.find(class_='hoveritem place')['href']
                except:
                    print url + " place url"
                    continue

                # переход на страницу места проведения события
                try:
                    place_soup = BeautifulSoup(make_request(place_url))

                    address = place_soup.find(class_='info-item').find_all('div')[1].string
                    parsed_event['address'] = str(address)
                except:
                    print url + " error address"
                    continue

                parsed_data.append(copy.deepcopy(parsed_event))

            if (not (stop_marker) and first_marker):
                break

            if (slipped_marker):
                break

            return_checker += 1

            if (return_checker == 50):
                return []

            i_page += 1

        stop_marker = False
        first_marker = False
        slipped_marker = False

    return parsed_data


import copy


def parsing(time_array_need):
    counter = 0
    array_need_time = copy.deepcopy(time_array_need)

    kassir_data = []

    for index, i in enumerate(array_need_time):

        # массив с элементами на один день
        # каждый элемент - это скловарь
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
                    continue

            day_array[k]['latitude'] = latitude
            day_array[k]['longitude'] = longitude

        kassir_data.append(copy.deepcopy(day_array))

    path = os.path.dirname(os.path.abspath(__file__)) + "/data/"

    output = open(path + "kassir.pkl", 'w')

    pickle.dump(kassir_data, output)

    output.close()
