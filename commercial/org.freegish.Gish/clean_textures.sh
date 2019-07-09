find /app/share/freegish/texture/ -name "*.tga" -exec sh -c 'rm $(dirname {})/$(basename {} ".tga").png' \;
