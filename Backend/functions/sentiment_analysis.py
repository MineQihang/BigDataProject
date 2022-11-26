from typing import List
import torch

import multiprocessing as mul

def sentiment_analysis_sentences(sentence:str, tokenizer, model):
    '''
    分析句子情感
    :param sentence 待情感分析句子
    :param tokenizer
    :param model
    :return sentiment 情感分析结果
    '''

    output=model(torch.tensor([tokenizer.encode(sentence)]))
    label = torch.nn.functional.softmax(output.logits,dim=-1)[0]
    if label[0]>label[1]:
        return "negative"
    return "positive"

def mul_sentiment_analysis(sentences: List[str], tokenizer, model, thread_num = 1):
    '''
    分析句子情感
    :param sentences 待情感分析句子列表
    :param thread_num 线程数
    :param tokenizer
    :param model
    :return sentiment 情感分析结果
    '''

    data = [(sentence,tokenizer,model)for sentence in sentences]
    pool = mul.Pool(thread_num)
    sentiment = pool.starmap(sentiment_analysis_sentences, data)
    return sentiment