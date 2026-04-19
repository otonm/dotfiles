#!/usr/bin/env bash
p="$1"
HOME_DIR=$(eval echo ~)

ICON_HOME=$'\uf015'   # 
ICON_DIR=$'\uf07b'    # 

if [ "$p" = "$HOME_DIR" ]; then
    echo "${ICON_HOME} ~"
    exit 0
fi

if echo "$p" | grep -q "^$HOME_DIR/"; then
    rel="${p#$HOME_DIR/}"
    n=$(echo "$rel" | tr -cd '/' | wc -c)
    if [ "$n" -le 1 ]; then
        echo "${ICON_HOME} ~/$rel"
    else
        top=$(echo "$rel" | cut -d'/' -f1)
        current=$(basename "$rel")
        echo "${ICON_HOME} ~/$top/.../$current"
    fi
else
    n=$(echo "$p" | tr -cd '/' | wc -c)
    if [ "$n" -le 2 ]; then
        echo "${ICON_DIR} $p"
    else
        base=$(echo "$p" | cut -d'/' -f2)
        current=$(basename "$p")
        echo "${ICON_DIR} /$base/.../$current"
    fi
fi
