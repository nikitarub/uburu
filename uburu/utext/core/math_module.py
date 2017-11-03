import sys
import os
import numpy as np
import word2vec
from scipy.spatial import distance
from uburu.settings import ROOT_MODEL_HISTORY
sys.path.insert(0, '')
# костыльно, но лучше решения я не нашел
__path__ = os.path.dirname(__file__)
__path__ = __path__[:-11]
sys.path.insert(0, __path__)

model = word2vec.load(ROOT_MODEL_HISTORY)


def dist(a, b):
    # В последствии могут пригодится и другие расстояния
    return distance.cosine(a, b)


def find_associated_sentences_weight(key_vector, sentences):
    # поиск предложений в которых есть слова близкие к ключеым
    # коэфициенты (веса) предложений
    sentences_weight = []

    for sentence in sentences:
        distances_in_sentence = []

        for word in sentence:
            # try работает быстрее, нежели проверять наличие слова в словаре
            try:
                vector_word = model.get_vector(word)
                vector_distance = dist(key_vector, vector_word)
                distances_in_sentence.append(vector_distance)
            except KeyError:
                pass

        if len(distances_in_sentence) != 0:
            weight = (sum(distances_in_sentence) *
                      np.median(distances_in_sentence) /
                      (len(distances_in_sentence)))
        else:
            # орицательный вес подобран имперически
            weight = 2

        sentences_weight.append(weight)

    return sentences_weight


def get_resulting_vector(sentence):
    resulting_vector = np.zeros(len(model.get_vector(model.vocab[0])))
    for word in sentence:
        # try работает быстрее, нежели проверять наличие слова в словаре
        try:
            vector_word = model.get_vector(word)
            resulting_vector += vector_word
        except KeyError:
            pass
    return resulting_vector


def get_resulting_vector_full_text(sentences):
    vector_length = len(model.get_vector(model.vocab[0]))
    resulting_vectors = []
    text_resulting_vector = np.zeros(vector_length)

    # подумать как сделать кол-во предложений адаптивным
    amount_resulting_vector = int(len(sentences) / 4)
    res_vectors_distances = []

    # получение результирующих векторов
    for sentence in sentences:
        resulting_vector = get_resulting_vector(sentence)
        resulting_vectors.append(resulting_vector)
        text_resulting_vector += resulting_vector

    # расстояния результирующих векторов и основного рез вектора
    for index, resulting_vector in enumerate(resulting_vectors):
        d = dist(resulting_vector, text_resulting_vector)
        res_vectors_distances.append((d, index))

    res_vectors_distances.sort()

    return sum([resulting_vectors[i[1]]
                for i in res_vectors_distances[:amount_resulting_vector]])
