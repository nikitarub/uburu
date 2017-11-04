from django.shortcuts import render
from .forms import KeywordsForm, UserTextForm
from utext.core import math_module, parser


def get_input(request):
    # Получение введенных форм
    keywords = ""
    keywords_array = []
    text_array = []
    text = ""
    out_data = []
    index = 0
    weight = 0
    sentence = ""
    if request.method == "POST":
        form_keywords = KeywordsForm(request.POST)
        form_usertext = UserTextForm(request.POST)

        if form_usertext.is_valid():
            data = form_usertext.cleaned_data
            text = data['text']
            words = parser.parse_into_words(text)
            words = parser.del_free_lines(words)
            text_array = parser.parse_into_sentences(words)

        if form_keywords.is_valid():
            data = form_keywords.cleaned_data
            keywords = data["keywords"]
            keywords_array = parser.parse_into_words(keywords)
            keywords_vector = math_module.get_resulting_vector(keywords_array)
            sentences_weight = math_module.find_associated_sentences_weight(
                keywords_vector, text_array)
            weight_dict = [(index, i)
                           for index, i in enumerate(sentences_weight)]
        else:
            key_vec = math_module.get_resulting_vector_full_text(text_array)
            sentences_weight = math_module.find_associated_sentences_weight(
                key_vec, text_array)
            weight_dict = [(index, i)
                           for index, i in enumerate(sentences_weight)]

        out_data = parser.get_out_data(weight_dict, text_array)
        out_data = sorted(out_data, key=parser.sort_by_weight)
        out_data = [i[2] for i in out_data][:int(len(out_data)/3)]

    return render(request, "utext/index.html", {"keywords": keywords,
                                                "text": text,
                                                "out_data": out_data})
