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
    i18n_data = open('json/%s' % lang, 'r')
    i18n = json.load(i18n_data)

    tr_list = generateTranslations(def_mod)

    for tr in tr_list:
        if tr not in i18n:
            if lang == 'en.json':
                i18n[tr] = tr
            else:
                i18n[tr] = ""

    return i18n

def addTranslations(def_mod, lang):
    add = findTranslations(def_mod, lang)
    add = dict(sorted(add.items()))

    i18n_data = open('json/%s' % lang, 'w')
    json.dump(add, i18n_data, indent=2)

def getFiles():
    with open('definitionModifier.json') as data_file:
        data = json.load(data_file)
        data = data['DefinitionModifier'.decode('utf-8')]
        data = data['SetAttribute'.decode('utf-8')]

    lang_files = os.listdir("json")

    for l in lang_files:
        addTranslations(data, l)

getFiles()
