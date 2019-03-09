#!/bin/bash
set -o errexit
set -o noclobber
set -o nounset
set -o pipefail

mdfile="$1"
title=$( cat "${mdfile}" | sed -r -n -e 's/^# (.*)$/\1/p' )
cat <<END
<!DOCTYPE html>
<html>
<head>
<title>${title} - dbatley.com</title>
<link rel="stylesheet" href="../../media/style.css" />
</head>
<body>
$( markdown_py -x fenced_code -x meta "${mdfile}" )
</body>
</html>
END
