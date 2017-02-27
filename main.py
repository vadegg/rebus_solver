import pymorphy2
from tqdm import tqdm

word_list1 = pymorphy2.MorphAnalyzer().iter_known_word_parses()
word_list2 = pymorphy2.MorphAnalyzer().iter_known_word_parses()

TQDM_MODE = False


def interesting_word(item):
    def tag_checker(tag):
        if "NOUN" not in tag or 'nomn' not in tag or "sing" not in tag:
            return False

        stop_list = ["Abbr",
                     "Name",
                     "Surn",
                     "Patr",
                     "Geox",
                     "Orgn",
                     "Trad"]

        for stop_word in stop_list:
            if stop_word in tag:
                return False

        return True

    def word_checker(word_to_check:str):
        if '-' in word_to_check or len(word_to_check) <= 3:
            return False

        preficses = ["авиа",
                     "анти",
                     "авто",
                     "одно",
                     "двух",
                     "трех",
                     "трёх",
                     "четырех",
                     "четырёх",
                     "пяти",
                     "шести",
                     "семи",
                     "восьми",
                     "девяти",
                     "десяти",
                     "одиннадцати",
                     "двенадцати",
                     "тринадцати",
                     "четырнадцати",
                     "пятнадцати",
                     "шестнадцати",
                     "семнадцати",
                     "восемнадцати",
                     "девтнадцати",
                     "двадцати",
                     "агро",
                     "астро",
                     "аудио",
                     "аэро",
                     "баро",
                     "бензо",
                     "био",
                    "вело",
                    "вибро",
                    "видео",
                    "гекто",
                    "гелио",
                    "гео",
                    "гетеро",
                    "гидро",
                    "гомо",
                    "дендро",
                    "зоо",
                    "изо",
                    "кило",
                    "кино",
                    "космо",
                    "макро",
                    "метео",
                    "микро",
                    "моно",
                    "мото",
                    "невро",
                    "нейро",
                    "нео",
                    "орто",
                    "палео",
                    "пиро",
                    "пневмо",
                    "порно",
                    "психо",
                    "радио",
                    "ретро",
                    "сейсмо",
                    "социо",
                    "спектро",
                    "стерео",
                    "термо",
                    "турбо",
                    "фито",
                    "фоно",
                    "фото",
                    "эвако",
                    "экзо",
                    "эко",
                    "электро",
                    "эндо",
                    "энерго"]

        for pref in preficses:
            if word_to_check.startswith(pref):
                return False

        return True

    return word_checker(item.word) and tag_checker(item.tag)

if TQDM_MODE:
    gen1 = tqdm(word_list1)
else:
    gen1 = word_list1

for word in gen1:
    if not interesting_word(word):
        continue

    first_part = word.word[:len(word.word)-3]

    current_letter = ''

    if TQDM_MODE:
        gen2 = tqdm(word_list2)
    else:
        gen2 = word_list2

    for word_ in gen2:

        if word_.word[0:2] != current_letter:
            current_letter = word_.word[0:2]
            print("Current letter: " + current_letter)

        if not interesting_word(word_):
            continue

        second_part = word_.word[:len(word_.word)-1]
        if 'о' not in second_part:
            continue

        second_part = second_part.replace('о', 'а')

        second_part += 'о'
        print("Checking " + word.word + " and " + word_.word + " to check: " + first_part + second_part)

        if pymorphy2.MorphAnalyzer().word_is_known(first_part + second_part):
            print("FINDED!!!\n" + word.word + ' + ' + word_.word + " = " + first_part + second_part + "\n")





