#!/usr/bin/env bash
p="$1"

ICON_VENV=$'\ue606'   # 
ICON_PY=$'\ue606'     # 

find_venv() {
    local dir="$p"
    while [ "$dir" != "/" ]; do
        for name in .venv venv; do
            cfg="$dir/$name/pyvenv.cfg"
            if [ -f "$cfg" ]; then
                echo "$dir/$name"
                return 0
            fi
        done
        dir=$(dirname "$dir")
    done
    return 1
}

venv_dir=$(find_venv) || exit 0

venv_name=$(grep '^prompt' "$venv_dir/pyvenv.cfg" 2>/dev/null | cut -d= -f2 | tr -d ' ()')
[ -z "$venv_name" ] && venv_name=$(basename "$venv_dir")

py_version=$("$venv_dir/bin/python" --version 2>/dev/null | awk '{print $2}')
[ -n "$py_version" ] && py_str=" ${ICON_PY} $py_version" || py_str=""

echo "${ICON_VENV} $venv_name$py_str"
