DST=$1
SRC="`dirname \"$0\"`"

if [ -z "${DST}" ]
then
    echo "deploy.sh <destination_dir>"
    exit 1
fi

mkdir -p "${DST}"
cp -v "${SRC}/"*.{py,html,css} "${DST}"
cp -v -R "${SRC}/"{images,js} "${DST}"

