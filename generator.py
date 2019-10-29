import os
import re
import wget
from os import path
from PIL import Image
from wordcloud import (WordCloud, get_single_color_func)
import multidict as multidict
import numpy as np
import matplotlib.pyplot as plt



global color_background, color_first, color_second, color_third, color_fourth, color_none
color_background, color_first, color_second, color_third, color_fourth, color_none = '#edeff1', '#ffd635', '#b8001f', '#349e48', '#0266b3', '#373c3f'


class SimpleGroupedColorFunc(object):
    

    def __init__(self, color_to_words, default_color):
        self.word_to_color = {word: color for (color, words) in color_to_words.items() for word in words}
        self.default_color = default_color

        
    def __call__(self, word, **kwargs):
        return self.word_to_color.get(word, self.default_color)


def format_input():
    input = open('text.txt').read()
    with open('temporary.txt', 'w') as f:
        f.write(re.sub('[,.!?#:\"\'\(\)\n/^\[\]`*0-9\<\>\“\”;–&º_@$…%&*§]+', ' ', input))
    input_file = open(path.join(d, 'temporary.txt')).read().lower()
    return input_file
        
        
def clear_output():
    with open('words.txt', 'w'), open('filtered.txt', 'a') as f:
        output_file = f.write('')
    return output_file
    
    
def filter_words():
    if not os.path.isfile('filter.txt'):
        dictionary_file = []
    else:
        with open('filter.txt', 'r') as f:
            dictionary_file = f.read()
            dictionary_file = dictionary_file.split('\n')
            dictionary_file = list(filter(None, dictionary_file))
    return dictionary_file

    
def make_picture(text):
    global color_background, color_first, color_second, color_third, color_fourth, color_none
    word_cloud = WordCloud(font_path = 'NotoSans-Regular.ttf', width = 1440, height = 1080, scale = 10, background_color = color_background)
    word_cloud.generate_from_frequencies(text)
    tier_one = open('tier_one.txt').read().replace('\'', '').split()
    tier_two = open('tier_two.txt').read().replace('\'', '').split()
    tier_three = open('tier_three.txt').read().replace('\'', '').split()
    tier_four = open('tier_four.txt').read().replace('\'', '').split()
    color_to_words = {
    color_first: tier_one,
    color_second: tier_two,
    color_third: tier_three,
    color_fourth: tier_four
    }
    default_color = color_none
    grouped_color_func = SimpleGroupedColorFunc(color_to_words, default_color)
    word_cloud.recolor(color_func = grouped_color_func)
    plt.figure()
    plt.imshow(word_cloud, interpolation = 'bilinear')
    plt.axis('off')    
    plt.savefig('cloud.png', dpi = (130 * 2.25) - 0.1, bbox_inches = 'tight', pad_inches = 0)
    
    
def count_frequency(sentence):
    main_dictionary = multidict.MultiDict()
    extra_dictionary = multidict.MultiDict()
    temporary_main_dictionary = {}
    temporary_extra_dictionary = {}
    for text in sentence.split():
        if text in dictionary_file:
            continue
        if text.startswith('-'):
            continue
        value = temporary_main_dictionary.get(text, 0)
        temporary_main_dictionary[text] = value + 1
    for key in temporary_main_dictionary:
        main_dictionary.add(key, temporary_main_dictionary[key])
        with open ('temp.txt', 'a') as f:
            f.write(str(key) + '|' + str(temporary_main_dictionary[key]) + '\n')
    temporary_input = open('temp.txt').read().strip()
    temporary_output = open('t.txt', 'w')
    temporary_output.write(re.sub('[^0-9\n]', '', temporary_input))
    with open('temp.txt') as f:
        line_order = sorted(f, key=lambda x: int(''.join(filter(str.isdigit, x))))
        reverse_order = list(reversed(line_order))
    with open('t.txt', 'w') as f:
        f.write(re.sub('[0-9]', '', str(reverse_order).replace('|', '').replace('[','').replace(']', '').replace('\\n', '\n').replace('\', \'','').replace('\'', '')))
    with open('words.txt', 'w') as f:
        f.write(str(reverse_order).replace('[','').replace(']', '').replace('\\n', '\n').replace('\', \'','').replace('\'', ''))
    first_tier = 10
    second_tier = 25
    third_tier = 50
    fourth_tier = 100
    with open('t.txt', 'r') as f:
        position = 0
        for key in f:
            position = position + 1
            if position<12.5:
                with open ('tier_one.txt', 'a') as f:
                    f.write(key.replace('\n', ' '))
            if position>12.5 and position<=25:
                with open ('tier_two.txt', 'a') as f:
                    f.write(key.replace('\n', ' '))
            if position>25 and position<=50:
                with open ('tier_three.txt', 'a') as f:
                    f.write(key.replace('\n', ' '))
            if position>50 and position<=100:
                with open ('tier_four.txt', 'a') as f:
                    f.write(key.replace('\n', ' '))
            else:
                continue
    for text in sentence.split():
        if text not in dictionary_file:
            continue
        if text.startswith('-'):
            continue
        value = temporary_extra_dictionary.get(text, 0)
        temporary_extra_dictionary[text] = value + 1
    for key in temporary_extra_dictionary:
        extra_dictionary.add(key, temporary_extra_dictionary[key])
        with open ('filtered.txt', 'a') as f:
            f.write(str(key) + '|' + str(temporary_extra_dictionary[key]) + '\n')
    return main_dictionary

    
def delete_temporaries():
    temporary_files = os.remove('temporary.txt')
    temporary_files = os.remove('temp.txt')
    temporary_files = os.remove('t.txt')
    temporary_files = os.remove('tier_one.txt')
    temporary_files = os.remove('tier_two.txt')
    temporary_files = os.remove('tier_three.txt')
    temporary_files = os.remove('tier_four.txt')
    temporary_files = os.remove('NotoSans-Regular.ttf')
    return temporary_files
    

d = path.dirname(__file__) if '__file__' in locals() else os.getcwd()
wget.download('https://github.com/google/fonts/blob/master/ofl/notosans/NotoSans-Regular.ttf?raw=true')
input_file = format_input()
output_file = clear_output()
dictionary_file = filter_words()
make_picture(count_frequency(input_file))
temporary_files = delete_temporaries()
