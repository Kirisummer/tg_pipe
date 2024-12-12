#!/bin/sh

pattern() {
    printf '(^\\d+\\t(user|chat|channel)\\t\\d+\\t).*(%s).*$' "$1"
}

python -u listen.py me | 
    stdbuf -oL grep -P "$(pattern 'hello|bye')" |
    python forward.py destination
