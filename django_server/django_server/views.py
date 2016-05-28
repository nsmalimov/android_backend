# -*- coding: utf-8 -*-
import json

import diplom_django.worker_directory.psql_work
import diplom_django.worker_directory.worker_func
from django.http import HttpResponse
from django.shortcuts import render_to_response

import data_path


def main_window(request):
    if request.method == 'GET':
        return render_to_response('autorization.html', )


def route_infom(request):
    if request.method == 'GET':
        return render_to_response('route_information.html', )


def build_route(request):
    if request.method == 'GET':
        return HttpResponse("Only Post")
    if request.method == 'POST':
        q = request.POST
        some_dict = q.dict()
        # print some_dict
        result_route = diplom_django.worker_directory.worker_func.main_worker_func(some_dict)
        return HttpResponse(json.dumps(result_route), content_type="application/json")


def list_route(request):
    if request.method == 'GET':
        return render_to_response('list_route.html', )


def addit_func(request):
    if request.method == 'GET':
        return render_to_response('event_addition.html', )


def asses_func(request):
    if request.method == 'POST':
        q = request.POST
        some_dict = q.dict()
        # print some_dict
        # {u'event_name': u'\u0430\u0440\u0442, u'asses': u'1', u'id': u'21747799'}
        diplom_django.worker_directory.psql_work.add_assesment(some_dict)

        # print some_dict
        result_route = "accept"

        return HttpResponse(json.dumps(result_route), content_type="application/json")


def geo_map(request):
    if request.method == 'GET':
        return render_to_response('geo_map.html', )


def wich_days(request):
    if request.method == 'GET':
        answer_date = data_path.get_wich_days()
        return HttpResponse(json.dumps(answer_date), content_type="application/json")
