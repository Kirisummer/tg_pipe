# Telegram piping scripts

[Donate to Ukraine!](https://war.ukraine.ua/donate/)

## Why?
Maybe you want to record some messages filtered by regex.

Maybe you want to analyze messages in some chat in near-real time.

Maybe you want to filter alerts from air raid alert channels in Telegram
[because your neighbor is a bastard](https://war.ukraine.ua) and they
[shower your home city with suicide drones and rockets](https://war.ukraine.ua/russia-war-crimes/#attacking-civilians-or-civilian-objects).

Who knows


## Wha? Huh?
1. Create a venv, enter it (optional):
```shell
python -m venv venv
source venv/bin/activate # for POSIX shells. If you have some other shell you know what to do better than I do
venv\Scripts\activate # for Windows
venv/Scripts/Activate.ps1 # Windows Powershell
venv/bin/Activate.ps1 # Linux Powershell
```

2. Install dependencies
```shell
pip -r requirements.txt
```

3. Get your API credentials from my.telegram.org and put them into `api.py`

4. Prepare sessions for each script that needs to run at the same time:
```shell
python prepare_session.py --api api.py session_name.session
```
Keep in mind that scripts can't use the same session or a copy of a session file.
Telegram probably sends only one event per session, and clients will steal each others events.

5. Run the scripts ([example](run.sh))


## What scripts?

Scripts have built-in help available, try running them with `--help`.

| Name                 | Description                                                        |
| -------------------- | ------------------------------------------------------------------ |
| `prepare_session.py` | Prepare session for other scripts                                  |
| `listen.py`          | Listen to Telegram sources (channels, users, chats) and print them |
| `forward.py`         | Forward messages to a Telegram channel, chat or user               |
| `tail.py`            | Print text of last messages in Telegram channel, char or user      |
