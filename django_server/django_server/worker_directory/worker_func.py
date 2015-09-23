# -*- coding: utf-8 -*-

import algorithm_opt
import psql_work
import recom_system

def main_worker_func(request_dict):
    #добавление в базу данных
    #построение маршрута

    vk_id = request_dict['id']
    psql_work.add_user(vk_id)

    recom_events = recom_system.main_func(vk_id) #рекомендованные события

    answer_dict = algorithm_opt.get_route_main(request_dict, recom_events)

    return answer_dict

