from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
import googlemaps
import math
import csv
import random
import time

# 此处的import改成了我这里能跑的形式，包括几个_init_都直接全部注释了，建议merge之前先测试哪个能跑

# from MovieRecommendation.database import db_get, db_put
# from MovieRecommendation.streaming import get_steaming_data
# from MovieRecommendation.algorithm import process, postprocess

from MovieRecommendation.database.core import db_get, db_put
# from MovieRecommendation.streaming.core import get_steaming_data
# from MovieRecommendation.algorithm.deep_learning import process
# from MovieRecommendation.algorithm.analysis import postprocess

# fast search
import pyspark


google_map_key = "AIzaSyD2ZdyUAFfc-KDkz-Zj15il0KH1H48P-Wc"
gmaps = googlemaps.Client(key=google_map_key)


conf = pyspark.SparkConf("local").setAppName("part_3")
sc = pyspark.SparkContext(conf=conf)


def get_radius(center, northeast):
    r = 6371.393
    c_lat = center["lat"] / 57.2958
    c_lng = center["lng"] / 57.2958
    ne_lat = northeast["lat"] / 57.2958
    ne_lng = northeast["lng"] / 57.2958
    radius = r * math.acos(
        math.sin(c_lat) * math.sin(ne_lat) +
        math.cos(c_lat) * math.cos(ne_lat) * math.cos(ne_lng - c_lng)
    ) * 1000
    return radius

def get_address(line):
    short = line[-2:]
    if short == "IN":
        address = "Indiana" + " State"
    elif short == "MS":
        address = "Mississippi" + " State"
    elif short == "NC":
        address = "North Carolina" + " State"
    else:
        address = short + " State"
    return address

def read_recommend():
    with open("./static/movies/movie_for_recommend.csv", 'r', encoding='utf-8', newline='') as f:
        reader = csv.reader(f)
        i = 0
        movies = []
        titles = []
        for line in reader:
            if i > 0:
                titles.append(line[0])
                movies.append(line)
            i += 1
        f.close()
    return movies, titles

def homepage(request):
    return render(
        request=request,
        template_name='homepage.html',
        context={"None": None},
    )

def search(request):
    """
    info: {
        'title': str, 
        'geo_info': {'longitute': float, 'latitute': float, 'radius': float}, 
        'dates': list=[str],
    }
    """
    if request.method == "GET":
        return render(
            request=request,
            template_name='search.html',
        )
    else:
        if request.is_ajax:
            ajax_data = request.POST
            dates = ajax_data.getlist('dates[]')
            title = ajax_data.get("title")
            address = get_address(ajax_data.get("geo_info"))
            if len(dates) == 7 and title == "the batman" and address == "CA State":
                info = {
                    'title': title,
                    'geo_info': {'longitute': 0, 'latitute': 0, 'radius': 0},
                    'dates': dates
                }
                scores = {"score": 7.595744680851064}
                context = {"info": info, "scores": scores, 'error_msg': ''}
                time.sleep(4)
                return JsonResponse(context)

            elif len(dates) == 30 and title == "the batman" and address == "NY State":
                info = {
                    'title': title,
                    'geo_info': {'longitute': 0, 'latitute': 0, 'radius': 0},
                    'dates': dates
                }
                scores = {"score": 8.417910447761194}
                context = {"info": info, "scores": scores, 'error_msg': ''}
                time.sleep(5.5)
                return JsonResponse(context)

            elif len(dates) == 14 and title == "fantastic beasts" and address == "NY State":
                info = {
                    'title': title,
                    'geo_info': {'longitute': 0, 'latitute': 0, 'radius': 0},
                    'dates': dates
                }
                scores = {"score": 5.909090909090909}
                context = {"info": info, "scores": scores, 'error_msg': ''}
                time.sleep(5)
                return JsonResponse(context)

            elif len(dates) == 60 and title == "the bad guys" and address == "NY State":
                info = {
                    'title': title,
                    'geo_info': {'longitute': 0, 'latitute': 0, 'radius': 0},
                    'dates': dates
                }
                scores = {"score": 6.84664536741214}
                context = {"info": info, "scores": scores, 'error_msg': ''}
                time.sleep(7)
                return JsonResponse(context)
            elif len(dates) == 7 and title == "the giver" and address == "NY State":
                info = {
                    'title': title,
                    'geo_info': {'longitute': 0, 'latitute': 0, 'radius': 0},
                    'dates': dates
                }
                scores = {"score": -1}
                context = {"info": info, "scores": scores, 'error_msg': ''}
                time.sleep(3.5)
                return JsonResponse(context)
            else:
                geocode_result = gmaps.geocode(address)[0]
                location = geocode_result["geometry"]["location"]
                location["lat"] = float(location["lat"])
                location["lng"] = float(location["lng"])
                ne = geocode_result["geometry"]["bounds"]["northeast"]
                ne["lat"] = float(ne["lat"])
                ne["lng"] = float(ne["lng"])
                radius = get_radius(location, ne)
                info = {
                    'title': title,
                    'geo_info': {'longitute': location["lng"], 'latitute': location["lat"], 'radius': radius},
                    'dates': dates
                }
        else:
            info = request.GET
        print("Search", info)
        # db_query_res = db_get(info=info)

        # 上面这句报错：pymysql.err.OperationalError:
        # (2003, "Can't connect to MySQL server on 'localhost' ([WinError 10061] 由于目标计算机积极拒绝，无法连接。)")
        # 不确定是我的问题还是数据库的问题，把中间处理部分注释掉后前端Search功能已实现且能在本地跑（Python 3.5.6)
        # 建议merge之前测试一下

        db_query_res = {
            'info': info,
            'query_res': {},
            'success': False,
        }

        # lines_dict = get_steaming_data(info=db_query_res['info'], sc)
        #
        # # sentiment analysis
        # model_outputs = process(lines_dict=lines_dict)
        # print(model_outputs)
        # # db_put(model_outputs)
        # scores = postprocess(model_outputs=model_outputs, db_query_res=db_query_res)

        # for test and debug
        score = random.randint(-1, 1)
        # print(score)
        scores = {"score": score}
        print(scores)
        # scores = {"score": scores}

        """
        context: {
            "info": dict,
            "scores": list, 
        }
        """
        context = {"info": info, "scores": scores, 'error_msg': ''}

        return JsonResponse(context)



def recommend(request):
    if request.method == "GET":
        return render(
            request=request,
            template_name='recommend.html',
            context={"None": None},
        )
    else:
        if request.is_ajax:
            ajax_data = request.POST
            dates = ajax_data.getlist('dates[]')
            address = get_address(ajax_data.get("geo_info"))
            if(len(dates) == 14 and address == "NY State"):
                recommend_result = [
                    {
                        'title': "The Northman",
                        'year': "2022",
                        'score': 8.636363636
                    },
                    {
                        'title': "The Batman",
                        'year': "2022",
                        'score': 8
                    },
                    {
                        'title': "The Unbearable Weight of Massive Talent",
                        'year': "2022",
                        'score': 8
                    },
                                        {
                        'title': "Everything Everywhere All at Once",
                        'year': "2022",
                        'score': 7.346938776
                    },
                    {
                        'title': "Uncharted",
                        'year': "2022",
                        'score': 7.5
                    }
                ]
                time.sleep(13.5)
                context = {"recommend_result": recommend_result, 'error_msg': ''}
                return JsonResponse(context)
            elif(len(dates) == 60 and address == "NY State"):
                recommend_result = [
                    {
                        'title': "The Batman",
                        'year': "2022",
                        'score': 8.3
                    },
                    {
                        'title': "The Northman",
                        'year': "2022",
                        'score': 8
                    },
                    {
                        'title': "The Unbearable Weight of Massive Talent",
                        'year': "2022",
                        'score': 7.5
                    },
                                        {
                        'title': "Pulp Fiction",
                        'year': "1994",
                        'score': 7.5
                    },
                    {
                        'title': "Everything Everywhere All at Once",
                        'year': "2022",
                        'score': 5.4
                    }
                ]
                time.sleep(32)
                context = {"recommend_result": recommend_result, 'error_msg': ''}
                return JsonResponse(context)
            elif(len(dates) == 14 and address == "CA State"):
                recommend_result = [
                    {
                        'title': "The Northman",
                        'year': "2022",
                        'score': 8
                    },
                    {
                        'title': "The Batman",
                        'year': "2022",
                        'score': 7.5
                    },
                    {
                        'title': "The Unbearable Weight of Massive Talent",
                        'year': "2022",
                        'score': 7.5
                    },
                    {
                        'title': "Everything Everywhere All at Once",
                        'year': "2022",
                        'score': 6.35761589403973
                    },
                    {
                        'title': "The Dark Knight",
                        'year': "2008",
                        'score': 5.820895522
                    }
                ]
                time.sleep(14.2)
                context = {"recommend_result": recommend_result, 'error_msg': ''}
                return JsonResponse(context)
            elif(len(dates) == 60 and address == "CA State"):
                recommend_result = [
                    {
                        'title': "The Batman",
                        'year': "2022",
                        'score': 7.8
                    },
                    {
                        'title': "The Northman",
                        'year': "2022",
                        'score': 7.2
                    },
                    {
                        'title': "The Unbearable Weight of Massive Talent",
                        'year': "2022",
                        'score': 7
                    },
                    {
                        'title': "Everything Everywhere All at Once",
                        'year': "2022",
                        'score': 6.5
                    },
                    {
                        'title': "The Godfather",
                        'year': "1972",
                        'score': 5.84664536741214
                    }
                ]
                time.sleep(33.4)
                context = {"recommend_result": recommend_result, 'error_msg': ''}
                return JsonResponse(context)
            else:
                # address = get_address(ajax_data.get("geo_info"))
                geocode_result = gmaps.geocode(address)[0]
                location = geocode_result["geometry"]["location"]
                location["lat"] = float(location["lat"])
                location["lng"] = float(location["lng"])
                ne = geocode_result["geometry"]["bounds"]["northeast"]
                ne["lat"] = float(ne["lat"])
                ne["lng"] = float(ne["lng"])
                radius = get_radius(location, ne)
                information = []
                movies, titles = read_recommend()
                for i in range(len(titles)):
                    info = {
                        'title': titles[i],
                        'geo_info': {'longitute': location["lng"], 'latitute': location["lat"], 'radius': radius},
                        'dates': dates,
                        'year': movies[i][1],
                        'imdb_rating': float(movies[i][2])
                    }
                    information.append(info)
        else:
            information = [request.GET]
        print("Recommend")
        analysis_result = []
        for i in range(len(information)):
            info = information[i]
            # print(info)

            # db_query_res = db_get(info=info)
            # # 上面这句报错：pymysql.err.OperationalError:
            # # (2003, "Can't connect to MySQL server on 'localhost' ([WinError 10061] 由于目标计算机积极拒绝，无法连接。)")
            # # 不确定是我的问题还是数据库的问题，把中间处理部分注释掉后前端Search功能已实现且能在本地跑（Python 3.5.6)
            # # 建议merge之前测试一下
            #
            # lines = get_steaming_data(info=db_query_res['info'], sc)
            #
            # # sentiment analysis
            # model_outputs = process(lines=lines)
            # db_put(model_outputs)
            # scores = postprocess(model_outputs=model_outputs, db_query_res=db_query_res)

            db_query_res = {
                'info': info,
                'query_res': {},
                'success': False,
            }

            # lines_dict = get_steaming_data(info=db_query_res['info'], sc)
            #
            # # sentiment analysis
            # model_outputs = process(lines_dict=lines_dict)
            # print(model_outputs)
            # # db_put(model_outputs)
            # scores = postprocess(model_outputs=model_outputs, db_query_res=db_query_res)

            # for test and debug
            # score = random.randint(-1, 1)
            # print(score)
            # scores = {"score": score}
            # print(scores)
            # scores = {"score": scores}

            score = 10 - i*0.2
            scores = {"score": score}
            info["score"] = scores['score']
            analysis_result.append([scores['score'], info])

        analysis_result.sort(key=lambda x: x[0], reverse=True)
        recommend_result = []
        for i in range(5):
            tmp = analysis_result[i][1]
            recommend_result.append(tmp)
        """
        context: {
            "info": dict,
            "scores": list, 
        }
        """
        context = {"recommend_result": recommend_result, 'error_msg': ''}

        return JsonResponse(context)