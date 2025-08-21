# Welcome to the .SkullBot Project

This Bot/Collection of Discord Automation Scripts was made for The Escarpment of [Hearthlight](https://www.hearthlightgame.org/).

### Current Features

- Creating *Threads* in a *Thread Channel* 
- Notifying *Role(s)* and *Sending Messages* to *Threads* in the *Thread Channel*

## Contributing

#### Recommended Reading

[Discord Developer Documentation](https://discord.com/developers/docs/intro)

[Python Requests HTTP Library](https://requests.readthedocs.io/en/latest/)

---

## Usage

To use these scripts, they can be manually run to execute actions as the bot, 
however it is typically more desirable to schedule these scripts to run using 
something like [Cron](https://en.wikipedia.org/wiki/Cron).

We'll dive it to Schedule in the next section **Setting Everything Up**.

### Creating Threads

Creating threads is handled by `practice-threads.py`. In order to make use of thread notifications without getting 
databases involved, or saving thread data to cache files, I use the format of the threads name to determine when to notify that thread.

The `notify-practice-threads.py` script will be checking for Threads with a date at the end like "MM/DD/YYYY or MM/DD/YY". More on that in the next part of Usage, "Notifying Threads"

In `practice-threads.py`, we declare the threads to create each week.

```python
payloads = [
    # Saturday Practice
    {
        "name": f"Saturday Practice {saturday.strftime('%m/%d/%Y')}",
        "auto_archive_duration": 10080,
        "type": 11  # 11 is for public threads
    },
    ...
```

Each thread needs a `name` ("Descriptive Name 08/20/2025"), an `auto_archive_duration` and the thread `type`.

Each time the script is run, threads will be created, so its best to run this one once per week.

### Notifying Threads

TODO: *section in progress*

---

## Setting Everything Up

While there are lots of ways to set-up your environment, this one is how I'm setting up my development environment.

### Python Project

To run everything you're going to need Python 3.11+ and a few other required packages:

- venv
- requests
- python-dotenv

#### Your Working Directory

Create a working directory for this project.

```bash
mkdir chapername-skullbot
cd chaptername-skullbot
```

#### Pulling the Repo

Either use git to pull the repo, or download and extract the skullbot project to your working directory.

After, the assumed project structure is:
```
chaptername-skullbot/
  L skullbot/
    L discord/
    | L __init__.py # Constants and utils
    | L client.py # API Client
    L weathergov/
    | L __init__.py # Constants and utils
    | L client.py # API Client
    L notify-practice-threads.py # Notify practice of the day, provide weather forecast.
    L practice-threads.py # Create practice threads
    L README.md # You are here
    L requirements.txt # required packages/libraries for .SkullBot
```

#### Geting Python Virtual Environment

Inside your skullbot working directory you'll need to create a python virtual environment. You'll need the `venv` package.

```bash
pip install venv
```

After getting `venv` or if you already have it, verify you're in you skullbot working directory and create your python virtual environment.

```bash
cd skullbot
python3 -m venv env
```

#### Installing Requirements

From inside your skullbot working directory you'll need to install the requirements `requirements.txt` to your virtual environment `env/`

```bash
env/bin/python3 -m pip install -r requirements.txt
```

#### Setting Up Your Environment

This project relies on a number of environment variables, they are:

```bash
# Set this for weather alerts near the chapter
export WEATHERGOV_GRIDID=""
export WEATHERGOV_GRIDX=""
export WEATHERGOV_GRIDY=""
# Set this for the Discord API Client
export DISCORDBOT_KEY=""
export DISCORD_SERVER_ID=""
export DISCORD_THREAD_CHANNEL_ID=""
```

When I am developing I typically append them to `env/bin/activate` and transition to other secrets management methods such as `python-dotenv`.

---

### Cron
#### Scheduling .SkullBot Actions

I've scheduled The Escarpment's Practice Threads to be created on Tuesdays at 1 PM.

`0 13 * * TUE`

I've the `notify-practice-threads.py` script to check every day, at 9 AM for threads to reply to.

`0 9 * * *`

Don't get the syntax? Thats okay, checkout [Crontab.guru](https://crontab.guru/)!

We're going to be adding cron rules to the crontab. To edit it:

```bash
crontab -e
```

Replace `<path-to-your-skullbot-working-directory>` with the actual path to your working directory. If your project structure is different, you may need to adjust these rules.

```crontab
0 13 * * TUE /bin/bash -c 'cd <path-to-your-skullbot-working-directory>/skullbot && source env/bin/activate && <path-to-your-skullbot-working-directory>/skullbot/env/bin/python practice-threads.py' >> <path-to-your-skullbot-working-directory>/skullbot/log.txt 2>&1
0 9 * * * /bin/bash -c 'cd <path-to-your-skullbot-working-directory>/skullbot && source env/bin/activate && <path-to-your-skullbot-working-directory>/skullbot/env/bin/python notify-practice-threads.py' >> <path-to-your-skullbot-working-directory>/skullbot/log.txt 2>&1
```