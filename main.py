import discord, sqlite3, os, asyncio, sys, zipfile
from gtts import gTTS
import urllib.request

current_directory = __file__.rstrip(os.path.basename(__file__))
if not "database.db" in os.listdir(current_directory):
    pass

if not "cache" in os.listdir(current_directory):
    os.mkdir(current_directory+"cache")



if not "ffmpeg.exe" in os.listdir(current_directory):
    if sys.platform == "win32":
        print("Fetching ffmpeg binary...")
        urllib.request.urlretrieve("https://github.com/BtbN/FFmpeg-Builds/releases/download/autobuild-2021-02-14-12-34/ffmpeg-n4.3.1-221-gd08bcbffff-win64-lgpl-4.3.zip",current_directory+"cache/ffmpeg.zip")
        with zipfile.ZipFile(current_directory+"cache/ffmpeg.zip","r") as zipf:
            zipf.extractall(current_directory+"cache")
        os.replace(current_directory+"cache/ffmpeg-n4.3.1-221-gd08bcbffff-win64-lgpl-4.3/bin/ffmpeg.exe",current_directory+"ffmpeg.exe")
        print("Successfully fetched ffmpeg binary!")
        

class bot(discord.Client):
    async def on_ready(self):
        print("Logged on as "+ str(self.user))
        self.database = sqlite3.connect("database.db")
        self.cache_path = current_directory+"cache/"


    def get_cache_content(self):
        return os.listdir(self.cache_path)
    async def join_voice_channel(self,voice_client, target_voice_state):
        if voice_client: 
            if not target_voice_state.channel == voice_client.channel:
                await voice_client.move_to(target_voice_state.channel)
        else:
            voice_client = await target_voice_state.channel.connect()
        return voice_client
    async def on_guild_join(self, guild):
        pass
    

    async def clear_cache(self):
        for f in self.get_cache_content():
            try:
                if not ".mp3" in f:
                    os.remove(self.cache_path+f)
            except PermissionError:
                pass

    async def on_voice_state_update(self, member, voice_before, voice_after):
        self.loop.create_task(self.clear_cache())
        
        def after_play(error):
            pass

        
        def playsound(voice_client,filepath, after=after_play):
            try:
                if not voice_client.is_playing():
                    voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(filepath), 1.0), after=after)
            except discord.errors.ClientException:
                pass

        voice_connection = member.guild.voice_client
        member_leave_file = self.cache_path + str(member.guild.id) + "_"+str(member.id) + "_leave.mp3"
        member_join_file = self.cache_path + str(member.guild.id) + "_"+str(member.id) + "_join.mp3"
        member_mute_file = self.cache_path + str(member.guild.id) + "_" + str(member.id) + "_mute.mp3"
        member_unmute_file = self.cache_path + str(member.guild.id) + "_" + str(member.id) + "_unmute.mp3"
        member_deafen_file = self.cache_path + str(member.guild.id) + "_" + str(member.id) + "_deafen.mp3"
        member_undeafen_file = self.cache_path + str(member.guild.id) + "_" + str(member.id) + "_undeafen.mp3"
        
        if voice_after.afk:
            return

        if member.name == self.user.name:
            return

        if member.guild.name == "Göttinger Turnverein":
            return

        if not os.path.basename(member_leave_file) in self.get_cache_content():
            if member.nick:
                tts = gTTS(member.nick+" left the channel")
            else:
                tts = gTTS(member.name+" left the channel")
            tts.save(member_leave_file)

        if not os.path.basename(member_join_file) in self.get_cache_content():
            if member.nick:
                tts = gTTS(member.nick+" joined the channel")
            else:
                tts = gTTS(member.name+" joined the channel")
            tts.save(member_join_file)
        
        if not os.path.basename(member_mute_file) in self.get_cache_content():
            if member.nick:
                tts = gTTS(member.nick+" is muted now")
            else:
                tts = gTTS(member.name+" is muted now")
            tts.save(member_mute_file)

        if not os.path.basename(member_unmute_file) in self.get_cache_content():
            if member.nick:
                tts = gTTS(member.nick+" is unmuted now")
            else:
                tts = gTTS(member.name+" is unmuted now")
            tts.save(member_unmute_file)

        if not os.path.basename(member_deafen_file) in self.get_cache_content():
            if member.nick:
                tts = gTTS(member.nick+" is deafened now")
            else:
                tts = gTTS(member.name+" is deafened now")
            tts.save(member_deafen_file)

        if not os.path.basename(member_undeafen_file) in self.get_cache_content():
            if member.nick:
                tts = gTTS(member.nick+" is undeafened now")
            else:
                tts = gTTS(member.name+" is undeafened now")
            tts.save(member_undeafen_file)
        if voice_connection:
            if voice_connection.is_playing():
                return
        if voice_after.channel and not voice_before.channel:
            voice_connection = await self.join_voice_channel(voice_connection, voice_after)
            playsound(voice_connection, member_join_file)
        elif voice_before.channel and not voice_after.channel:
            voice_connection = await self.join_voice_channel(voice_connection, voice_before)
            playsound(voice_connection, member_leave_file)
        elif (voice_before.deaf and not voice_after.deaf) or (voice_before.self_deaf and not voice_after.self_deaf):
            voice_connection = await self.join_voice_channel(voice_connection, voice_after)
            playsound(voice_connection, member_undeafen_file)
        elif (voice_after.deaf and not voice_before.deaf) or (voice_after.self_deaf and not voice_before.self_deaf):
            voice_connection = await self.join_voice_channel(voice_connection, voice_after)
            playsound(voice_connection, member_deafen_file)
        elif (voice_after.mute and not voice_before.mute) or (voice_after.self_mute and not voice_before.self_mute):
            voice_connection = await self.join_voice_channel(voice_connection, voice_after)
            playsound(voice_connection, member_mute_file)
        elif (voice_before.mute and not voice_after.mute) or (voice_before.self_mute and not voice_after.self_mute):
            voice_connection = await self.join_voice_channel(voice_connection, voice_after)
            playsound(voice_connection, member_unmute_file)
        


try:
    keyfile = open("token.key","r")
    token = keyfile.read()
    keyfile.close()
    bot_instance = bot()
    bot_instance.run(token)
except FileNotFoundError:
    print("token.key file with token missing")
