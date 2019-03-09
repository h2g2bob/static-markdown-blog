#!/bin/bash
set -o errexit
set -o noclobber
set -o nounset
set -o pipefail

find public/ -type f -name '*.md' -print | while read mdfile
do
	htmlfile="${mdfile%%.md}.html"
	echo "${htmlfile}"
	if [ ! -e "${htmlfile}" ] || [ "${mdfile}" -nt "${htmlfile}" ]
	then
		echo "${mdfile}"
		./content.html.sh "${mdfile}" >| "${htmlfile}"
	fi
done
