#!/usr/bin/env bash
p="$1"
cd "$p" 2>/dev/null || exit 0
git rev-parse --is-inside-work-tree 2>/dev/null | grep -q true || exit 0

ICON_BRANCH=$'\ue0a0'   # 
ICON_AHEAD=$'\uf55c'    # 
ICON_BEHIND=$'\uf544'   # 
ICON_MODIFIED=$'\uf044' # 
ICON_STAGED=$'\uf067'   # 
ICON_UNTRACKED=$'\uf128' # 

branch=$(git symbolic-ref --short HEAD 2>/dev/null || git rev-parse --short HEAD 2>/dev/null)
[ -z "$branch" ] && exit 0

flags=""
git diff --quiet 2>/dev/null          || flags="${flags} ${ICON_MODIFIED}"
git diff --cached --quiet 2>/dev/null || flags="${flags} ${ICON_STAGED}"
git ls-files --others --exclude-standard --quiet "$p" | grep -q . && flags="${flags} ${ICON_UNTRACKED}"

upstream=$(git rev-parse --abbrev-ref @{upstream} 2>/dev/null)
if [ -n "$upstream" ]; then
    ahead=$(git rev-list --count @{upstream}..HEAD 2>/dev/null)
    behind=$(git rev-list --count HEAD..@{upstream} 2>/dev/null)
    [ "$ahead" -gt 0 ]  && flags="${flags} ${ICON_AHEAD}${ahead}"
    [ "$behind" -gt 0 ] && flags="${flags} ${ICON_BEHIND}${behind}"
fi

echo "${ICON_BRANCH} $branch$flags"
