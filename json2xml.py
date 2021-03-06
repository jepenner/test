import json
import os

def json2xml(json_obj, lang, line_padding=""):
    result_list = list()

    for tag_name in json_obj:
        sub_obj = json_obj[tag_name]
        if tag_name.encode('utf-8') == 'SetAttribute':
            for item in sub_obj:
                text = tag_name
                for att in item:
                    if item[att] in lang:
                        if lang[item[att]] == "":
                            text = text + " " + att + "=\"" + item[att] + "\""
                        else:
                            text = text + " " + att + "=\"" + lang[item[att]] + "\""
                    else:
                        text = text + " " + att + "=\"" + item[att] + "\""
                result_list.append("%s<%s>" % (line_padding, text + " /"))
        else:
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, lang, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

    return "\n".join(result_list)

def lang_check():
    existing_json = [elem[:2] for elem in os.listdir("json")]
    existing_xml = [elem[:-4] for elem in os.listdir("xml")]
    lang_list = list()

    with open('lang.txt', 'r') as lang_data:
        lang_list = eval(lang_data.read())

        for l in list(lang_list):
            if l not in existing_json:
                del lang_list[l]
                
        for l in existing_xml:
            if l not in lang_list:
                os.remove("xml/%s.xml" % l)

    return lang_list

def getFiles():
    data = dict()
    i18n = dict()

    with open('definitionModifier.json') as data_file:
        data = json.load(data_file)

    lang_list = lang_check()

    for lang in lang_list:
        with open('json/%s.json' % lang, 'r') as i18n_data:
            i18n = json.load(i18n_data)

        with open('xml/%s.xml' % lang_list[lang], 'w') as lang_file:
            lang_file.write(str(json2xml(data, i18n)))
            lang_file.close()

getFiles()