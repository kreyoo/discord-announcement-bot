# Description

This is a discord bot which announces joining, leaving, muting, unmuting, deafening, and undeafening of a member.


# Deployment
<p>

**Python 3.8 is recommended!**</p>
<p>

In the directory do
`pip install -r requirements.txt`
to get the python modules.
</p>

<p>

If you are on a **linux-based system**, you must install ffmpeg.

For Distributions of **Ubuntu** or **Debian** you could use:
`sudo apt install -y ffmpeg`
</p>
<p>

Then create a token.key file and insert your bot token into it.
</p>
<p>

After that you can start the bot with
`python main.py` (Windows)

`python3 main.py` (Linux)
</p>

<p>

**NOTE**: The main.py fetches the [ffmpeg](https://github.com/BtbN/FFmpeg-Builds/releases) binary automatically if you are on windows. However, if you wish to have another binary you can replace the old one.
</p>

# TODO

- Handling of people moving between channels
- Handling of events that happen while the BOT is announcing another event
- Configuration options to disable/enable features and change the volume
- Cache clearing
- Make announcements of deafening and muting work
