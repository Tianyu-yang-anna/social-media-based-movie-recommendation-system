def postprocess(model_outputs: dict, db_query_res: dict) -> list:

    '''    
    input: 
        model_outputs: {
            'date1': {
                'pos': int
                'neg': int
            }
            'date2': {
                'pos': int
                'neg': int
            }
            ......
        }

        db_query_res: {
            'info': dict,
            'query_res': dict,
            'success': bool, //if there still exist dates in info which need to be extracted using twitter, success = False
        }
    output: 
        scores: list of float
    '''

    total_pos = 0
    total_neg = 0
    scores = {}
    
    res_from_db = db_query_res['query_res']
    for date in res_from_db:
        score_set = res_from_db[date]
        total_pos += score_set['pos']
        total_neg += score_set['neg']
    if not db_query_res['success']:
        # for date in db_query_res['info']['dates']:
        for date in model_outputs: #Should be the same?
            score_set = model_outputs[date]
            total_pos += score_set['pos']
            total_neg += score_set['neg']
    if total_neg + total_pos == 0:
        scores["score"] = -1
    else:
        scores["score"] = (10 * total_pos/(total_neg + total_pos))
    # print('num of positive and negative tweets: ', total_pos, total_neg)
    # print('score: ', scores[0])
    return scores

if __name__ == "__main__":
    model_outputs = {
        '2000-01-03': {'pos': 233, 'neg': 334}, 
        '2000-01-04': {'pos': 654, 'neg': 321}, 
    }

    info = {
        'title': 'MOVIE_TITLE', 
        'geo_info': {'longitute': 3.14, 'latitute': 3.15 , 'radius': 3.16}, 
        'dates': ['2000-01-03', '2000-01-04'],#new dates required
    }

    query_res = {
        '2000-01-01': {'pos': 111, 'neg': 222}, 
        '2000-01-02': {'pos': 333, 'neg': 444}, 
    }

    db_query_res = {
        'info': info,
        'query_res': query_res,
        'success': False,
    }
    postprocess(model_outputs, db_query_res)