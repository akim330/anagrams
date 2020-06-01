import requests
import re
import time
import datetime

url_time = 'http://worldclockapi.com/api/json/utc/now'

def get_time():
    start_time = time.time()
    response = requests.get(url_time)
    data = response.json()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")
    return data

def get_datetime():
    start_time = time.time()
    now = datetime.datetime.now()
    end_time = time.time()
    print(f"Time taken: {end_time - start_time}")


def get_etym(word):
    data = get_word_data(word)
    try:
        etym_string = data['et'][0][1]
        pattern1 = '{it}(.*?){/it}'
        etym_list_commas = re.findall(pattern1, etym_string)
        etym_list_split = []
        for string in etym_list_commas:
            etym_list_split = etym_list_split + string.split(', ')

        if 'literally,' in etym_string:
            etym_list_split.append(word)

        return etym_list_split

    except (TypeError, KeyError):
        return None

def get_prefix_suffix(word):
    try:
        root = get_word_data(word)['meta']['id'].split(':')[0].upper()
        common_root = longestSubstringFinder(root, word)
        try:
            prefix = word.split(common_root)[0]
            suffix = word.split(common_root)[1]
            if prefix or suffix:
                return True, prefix, suffix
            else:
                return False, None, None
        except ValueError:
            # print("Couldn't get data")
            return False, None, None

    except TypeError:
        return False, None, None

