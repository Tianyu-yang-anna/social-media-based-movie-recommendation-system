from MovieRecommendation.algorithm.model import BertEstimator 
# from dataset import Dataset
import torch 

MAX_SENTENCE_LENGTH = 256

import os 
FILE_ABS_PATH = os.path.abspath(__file__)


def pad(array, n):
    current_len = len(array)
    if current_len > n:
        return array[:n]
    extra = n - current_len
    return array + ([0] * extra)


def process(lines_dict: dict) -> dict:
    """
    input:
        lines: A list of texts.
    output: 
        A list of DL model's predictions for each text input.
  
    lines_dict = {
        '2000-01-01': ["Hello how are you?", "I like you so much."],
        '2000-01-02': ["I hate you.", "I don't like your look."]
    }

    model_outputs = {
        '2000-01-01': {'pos': 0, 'neg': 0}, 
        '2000-01-02': {'pos': 0, 'neg': 0}, 
    }

    """

    model_outputs = {}

    # model_dir = '/'.join(FILE_ABS_PATH.split('/')[:-1]) + "MovieRecommendation/algorithm/weights/"
    model_dir = "/Users/donot/social-media-based-movie-recommendation-system/MovieRecommendation/MovieRecommendation/algorithm/weights/"
    # print('/'.join(FILE_ABS_PATH.split('/')[:-1]))

    estimator = BertEstimator()
    # estimator.load(model_dir="./weights/")
    estimator.load(model_dir=model_dir)

    for date, lines in lines_dict.items():
        scores = []
        
        for line in lines:
            tokens = estimator.tokenizer.tokenize(line)
            tokens = tokens[:MAX_SENTENCE_LENGTH - 2]
            bert_sent = torch.tensor(pad(estimator.tokenizer.convert_tokens_to_ids(["[CLS]"] + tokens + ["[SEP]"]),
                               n=MAX_SENTENCE_LENGTH)).view(1, -1)
            outputs = estimator.model(bert_sent)
            _, is_neg = torch.max(outputs[0], 1)
            score = list(is_neg.cpu().detach().numpy())
            scores.extend(score)
        model_outputs[date] = scores 

    for date, scores in model_outputs.items():
        pos = scores.count(0)
        neg = scores.count(1)
        model_outputs[date] = {'pos': pos, 'neg': neg}
    return model_outputs 


if __name__ == '__main__':
    lines_dict = {
        '2000-01-01': ["Hello how are you?", "I like you so much.", "I hate you.", "I don't like your look."],
        '2000-01-02': ["I hate you.", "I don't like your look.", "Nice to meet you here!"]
    }
    print(process(lines_dict))