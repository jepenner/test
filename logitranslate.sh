#!/bin/bash

export cmd="$1"

if [ "$cmd" == "gen" ]; then
  python i18nGenerator.py
  python json2xml.py
  echo "Translation files have been generated."

elif [ "$cmd" == "add-lang" ]; then
  export lang_abb="$2"
  export lang_full="$3"
  if [ ${#lang_abb} == "2" ]; then
    if grep -F -q "'$lang_abb'" lang.txt; then
      echo "ERROR: That language already exists"
    elif [ ${#lang_full} != "0" ]; then 
      sed -i -e "s/\ \}/,\ \'${lang_abb}\': \'${lang_full}DMF\' }/g" lang.txt
      python i18nGenerator.py
      python json2xml.py
      echo "Language successfully added."
    else
      echo "ERROR: Invalid file name; must be \"add [st] [String]\""
    fi
  else
    echo "ERROR: Invalid file name; must be \"add [st] [String]\""
  fi

elif [ "$cmd" == "del-lang" ]; then
  export lang_abb="$2"
  export lang_full="$3"
  if [ "${#lang_abb}" == "2" ]; then
    if [ "$lang_abb" == "en" ]; then
      echo "ERROR: Not permitted to delete the English translation"
    elif grep -q "$lang_abb" lang.txt; then
      if grep -q "$lang_full" lang.txt; then
        sed -i -e "s/, '${lang_abb}': '${lang_full}DMF'//g" lang.txt
        python i18nGenerator.py
        python json2xml.py
        echo "Language successfully deleted."
      else
	echo "ERROR: Language does not exist"
      fi
    else
      echo "ERROR: Language does not exist"
    fi
  else
    echo "ERROR: Invalid file name; must be \"del [st] [String]\""	 
  fi

elif [ "$cmd" == "add-trans" ]; then
  read -r -p "XPath: " "xpath"
  while ( grep -F -q "\"XPath\": \"$xpath\"" definitionModifier.json ) do
    echo "ERROR: That path already exists"
    read -r -p "XPath: " "xpath"
  done
  read -r -p "Caption Type: " "captype"
  while ( echo "$captype" | grep -q ' ' ) do
    echo "ERROR: Caption Type must be one string"
    read -r -p "Caption Type: " "captype"
  done
  read -r -p "Phrase: " "ph"
  sed -i ':a;N;$!ba;s/} ]/},\n  { new } ]/g' definitionModifier.json
  sed -i "s|{ new }|{ "\""XPath"\"": "\""${xpath}"\"", "\""${captype}"\"": "\""${ph}"\"" }|g" definitionModifier.json
  python i18nGenerator.py
  python json2xml.py
  echo "Definition Modifier added successfully"

elif [ "$cmd" == "del-trans" ]; then
  read -r -p "Delete by: [X]Path  [P]hrase >>" "opt"
  if [ "$opt" == "X" ]; then
    read -r -p "XPath: " "xpath"
    while !( grep -F -q "\"XPath\": \"$xpath\"" definitionModifier.json ) do
      echo "ERROR: That path does not exist"
      read -r -p "XPath: " "xpath"
    done
    sed -i "s|{ \"XPath\": \""${xpath}"\".* }|{ old }|g" definitionModifier.json
    sed -i ':a;N;$!ba;s/,\n  { old }//g' definitionModifier.json
    python i18nGenerator.py
    python json2xml.py
    echo "Definition Modifier deleted successfully"
  elif [ "$opt" == "P" ]; then
    read -r -p "Phrase: " "ph"
    while !( grep -F -q "\"$ph\"" definitionModifier.json ) do
      echo "ERROR: That phrase does not exist"
      read -r -p "Phrase: " "ph"
    done
    sed -i "s|{ \"XPath\": \".*\", \".*\": \"${ph}\" }|{ old }|g" definitionModifier.json
    sed -i ':a;N;$!ba;s/,\n  { old }//g' definitionModifier.json
    python i18nGenerator.py
    python json2xml.py
    echo "Definition Modifier deleted successfully"
  else
    echo "ERROR: Invalid option"
  fi

elif [ "$cmd" == "list-lang" ]; then
  grep "" lang.txt

elif [ "$cmd" == "list-dm" ]; then
  grep "" definitionModifier.json

else
  echo "ERROR: Invalid input"
  echo "Usage: logitranslate [OPTION] [STRING]"
  echo "Options:"
  echo "    -gen			initiate language file generation"
  echo "    -add-lang [st] [String]	add translation, lang file will become [st].json
				and xml file will become [String]DMF.xml"
  echo "    -del-lang [st] [String]	delete [st] translation"
  echo "    -add-dm			add definition modifier"
  echo "    -del-dm			delete definition modifier"
  echo "    -list-lang			lists available languages"
  echo "    -list-dm			lists all definition modifiers"
fi
