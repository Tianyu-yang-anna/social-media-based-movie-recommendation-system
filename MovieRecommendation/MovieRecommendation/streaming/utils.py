from datetime import datetime
import re 
from ..algorithm.deep_learning import process

def string_cleaning(s: str):

    s = s.strip().lower()
    s = s.replace("&nbsp;", " ")
    s = re.sub(r'<br(\s\/)?>', ' ', s)
    s = re.sub(r' +', ' ', s)  # merge multiple spaces into one

    return s 


def clean_and_tokenize(x):
    return x 


def reformat_date(x):
    x.created_at = datetime.strptime(str(x.created_at)[:10], '%Y-%m-%d').strftime('%Y-%m-%d')
    return x

def fun_get_model_res_count(x, estimator):
    estimator = estimator
    def get_model_res_count(x):
        return process(x, estimator)
    return get_model_res_count

def preprocess_youtube_comment(x):
    return x 