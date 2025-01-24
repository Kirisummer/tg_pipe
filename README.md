# Telegram piping scripts

## Wha? Huh?
1. Create a venv, enter it (optional):
```
python -m venv venv
source venv/bin/activate # for POSIX shells. If you have some other shell you know what to do better than I do
venv\Scripts\activate # for Windows
```

2. Install dependencies
```
pip -r requirements.txt
```

3. Get your API credentials from my.telegram.org and put them into `api.py`

4. Prepare sessions for each script that needs to run at the same time: `
```
python prepare_session.py --api api.py session_name.session
```
Keep in mind that scripts can't use the same session or a copy of a session file.
Telegram probably sends only one event per session, and clients will steal each others events.

5. Run the scripts ([example](run.sh))

## What scripts?

Scripts have built-in help available, try running them with `--help`.

| Name       | Description                                                        |
| ---------- | ------------------------------------------------------------------ |
| listen.py  | Listen to Telegram sources (channels, users, chats) and print them |
| forward.py | Forward messages to a Telegram channel, chat or user               |
