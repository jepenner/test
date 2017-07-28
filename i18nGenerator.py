import json
import os
import operator

def generateTranslations(json):
    result_list = list()

    for elem in json:
        for att in elem:
            if att != 'XPath'.decode('utf-8'):
                result_list.append(elem[att])
    
    return result_list

def findTranslations(def_mod, lang):
    i18n = dict()

    with open('json/%s' % lang, 'r') as i18n_data:
        i18n = json.load(i18n_data)

    tr_list = generateTranslations(def_mod)

    for tr in tr_list:
        if tr not in i18n:
            if lang == 'en.json':
                i18n[tr] = tr
            else:
                i18n[tr] = ""

    for tr in list(i18n):
        if tr not in tr_list:
            del i18n[tr]

    return i18n

def addTranslations(def_mod, lang):
    add = findTranslations(def_mod, lang)
    
    with open('json/%s' % lang, 'w') as i18n_data:
        json.dump(add, i18n_data, indent=2)

def lang_check(lang_list):
    existing = os.listdir("json")
    empty = dict()

    for l in lang_list:
        if l not in existing:
            with open('json/%s' % l, 'w+') as fp:
                json.dump(empty, fp)
            fp.close()

    for l in existing:
        if l not in lang_list:
            os.remove("json/%s" % l)

def getFiles():
    with open('definitionModifier.json') as data_file:
        data = json.load(data_file)
        data = data['DefinitionModifier'.decode('utf-8')]
        data = data['SetAttribute'.decode('utf-8')]

    with open('lang.txt', 'r') as lang_files:
        lang_files = eval(lang_files.read())
        lang_list = ["%s.json" % s for s in lang_files]
        lang_check(lang_list)

        for l in lang_list:
            addTranslations(data, l)

getFiles()
