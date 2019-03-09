#!/bin/bash
find public/ -type f -name '*.md' -print | while read mdfile
do
	htmlfile="${filename%%.md}.html"
	if [ ! -e "${htmlfile}" ] || [ "${mdfile}" -nt "${htmlfile}" ]
	then
		echo "${mdfile}"
		markdown_py -x fenced_code "${mdfile}" > "${htmlfile}";
	fi
done
