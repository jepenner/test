import json

with open('definitionModifier.json') as data_file:
    data = json.load(data_file)

def json2xml(json_obj, lang, line_padding=""):
    result_list = list()

    json_obj_type = type(json_obj)

    for tag_name in json_obj:
        sub_obj = json_obj[tag_name]
        if tag_name.encode('utf-8') == 'SetAttribute':
            for item in sub_obj:
                text = tag_name
                for att in item:
                    if att.encode('utf-8') == 'XPath':
                        text = text + " " + att + "=\"" + item[att] + "\""
                    else:
                        text = text + " " + att + "=\"" + lang[item[att]] + "\""
                result_list.append("%s<%s>" % (line_padding, text + " /"))
        else:
            result_list.append("%s<%s>" % (line_padding, tag_name))
            result_list.append(json2xml(sub_obj, lang, "\t" + line_padding))
            result_list.append("%s</%s>" % (line_padding, tag_name))

    return "\n".join(result_list)

lang_list = { 'en': 'EnglishXML', 'fr': 'FrenchXML' }

for lang in lang_list:
    i18n_data = open('json/%s.json' % lang, 'r')
    i18n = json.load(i18n_data)

    lang_file = open('xml/%s.xml' % lang_list[lang], 'w')
    lang_file.write(str(json2xml(data, i18n)))
    lang_file.close()