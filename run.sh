#!/bin/sh -e

cd "$(dirname "$0")"

pattern() {
    printf '(^\\d+\\t(user|chat|channel)\\t\\d+\\t).*(%s).*$' "$1"
}

# Separate sessions are needed. Clients will eat each others events otherwise
echo Preparing listen session
python prepare_session.py --api api.py listen.session
echo Creating forward session
python prepare_session.py --api api.py forward.session

echo 'Starting The Pipe'
python -u listen.py --api api.py --session listen.session me |
    stdbuf -oL grep -P "$(pattern 'hello|bye')" |
    python forward.py --api api.py --session forward.session 'Destination Chat'
