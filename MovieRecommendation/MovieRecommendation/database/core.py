import pymysql

def exec_db_query(query: str) -> int:
    conn = pymysql.connect(
        host="localhost",
        port=3306,
        user="root",
        password="********",
        db="********")
    cursor = conn.cursor()
    cursor.execute(query)
    res = cursor.fetchall()
    conn.commit()
    return res

def db_get(info: dict) -> dict:
    """
    input:
        info: {
            'title': str, 
            'geo_info': {'longitute': float, 'latitute': float, 'radius': float}, 
            'dates': list=[str],
        }
    output: 
        db_query_res: {
            'info': dict,
            'query_res': dict,
            'success': bool, //if there still exist dates in info which need to be extracted using twitter, success = False
        }

        query_res is a dict. Keys are dates, values are dicts. map(str -> {'pos': int, 'neg': int})

    """
    dates = info['dates']
    new_date = []
    query_res = {}
    flag = True
    for date in dates:
        query = 'select pos, neg from 6889proj.model_res where date = \'' + date + '\';'
        pos_neg = exec_db_query(query)
        if not pos_neg:
            new_date.append(date)
            flag = False
        else:
            query_res[date] = {'pos': pos_neg[0][0], 'neg': pos_neg[0][1]}
    info['dates'] = new_date
    db_query_res = {
        'info': info,
        'query_res': query_res,
        'success': flag,
    }
    return db_query_res


def db_put(model_outputs: dict) -> bool:
    for date, vals in model_outputs.items():
        query = 'insert into 6889proj.model_res (date, pos, neg) values ('
        query += '\'' + date + '\',' + str(vals['pos']) + ',' + str(vals['neg']) + ');'
        res = exec_db_query(query)
        print(res)
    return False

# if __name__ == '__main__':
#     # model_outputs = {
#     #     '2000-01-03': {'pos': 0, 'neg': 0},
#     #     '2000-01-02': {'pos': 0, 'neg': 0},
#     # }
#     # db_put(model_outputs)
#     info = {
#         'dates': ['2022-04-11', '2022-04-12', '2022-05-12']
#     }
#     print(db_get(info))