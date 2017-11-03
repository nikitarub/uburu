"""
1.0 version of parser

Must be modified with nltk at least till 2.0 uburu
"""


def del_free_lines(data):
    data_ret = []
    for i in data:
        if (i[-1] == ('\n' or '\r')) or (i[-1] == ' '):
            i = i[:-1]
        data_ret.append(i)
    return data_ret


def parse_into_words(text):
    text += ' '
    word = ''
    data = []
    for i in text:
        word += i
        if i == ' ' or i == '\n':
            data.append(word)
            word = ''
    data = del_free_lines(data)

    return data


def ignore_shortening(word):
    numbers = '0123456789'
    flag = False
    if '.' in word:
        if 2 <= len(word) <= 3:
            if (word[-1] == '.') or (word[-2] == '.'):
                flag = True
        else:
            for i in word:
                if i in numbers and '.' in word[:-2]:
                    flag = True
                    break
    return flag


def parse_into_sentences(data):
    sentences = [[]]
    count = 0
    for i in data:
        if not ignore_shortening(i):
            if '.' not in i:
                sentences[count].append(i)
            else:
                sentences[count].append(i[:-1])
                sentences.append([])
                count += 1
        else:
            sentences[count].append(i)

    return sentences


def get_out_data(weight_dict, text_array):
    sentence_str = ''
    out_data = []
    for (index, weight) in weight_dict:
        for word in text_array[index]:
            sentence_str += ' ' + word
        if len(sentence_str) != 0:
            sentence_str += '.'
            out_data.append((index, weight, sentence_str))
        sentence_str = ''

    return out_data


def sort_by_weight(input_str):
    return input_str[1]
