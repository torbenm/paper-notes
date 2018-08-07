 #!/bin/sh
PDF_LOC="data/paper/pdf/*"
PNG_LOC="data/paper/png/"


for f in $PDF_LOC; do mv "$f" "${f// /_}"; done

rm -r $PNG_LOC/*
for d in $PDF_LOC; do
    bname="$(basename $d)"
    filename="${bname%.*}"
    echo "Converting $bname ..."
    convert -density 300 $d -quality 100 -alpha off "$PNG_LOC/$filename.png"
done