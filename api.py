import requests
import re
import time

url_start = "https://www.dictionaryapi.com/api/v3/references/collegiate/json/"
url_end = "?key=1d218d21-dc07-4abc-8198-1cb5fadb100d"

def longestSubstringFinder(string1, string2):
    start_time = time.time()
    answer = ""
    len1, len2 = len(string1), len(string2)
    for i in range(len1):
        match = ""
        for j in range(len2):
            if (i + j < len1 and string1[i + j] == string2[j]):
                match += string2[j]
            else:
                if (len(match) > len(answer)): answer = match
                match = ""
    end_time = time.time()
    print(f"{end_time - start_time}")
    return answer

def get_word_data(word):
    url = url_start + word + url_end
    response = requests.get(url)
    try:
        data = response.json()[0]
        return data
    except IndexError:
        return None


def get_etym(word):
    data = get_word_data(word)
    try:
        etym_string = data['et'][0][1]
        pattern = '{it}(.*?){/it}'
        etym_list_commas = re.findall(pattern, etym_string)
        etym_list_split = []
        for string in etym_list_commas:
            etym_list_split = etym_list_split + string.split(', ')
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
            print("Couldn't get data")
            return False, None, None

    except TypeError:
        return False, None, None

