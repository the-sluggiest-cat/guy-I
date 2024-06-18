import os
if os.path.exists("vers.txt") is False:
    version = "NULL!"
else:
    version = open("vers.txt", "r").read().splitlines()[0]
for line in open("data/guy.logo", "r").read().splitlines():
    print(line.replace("_VERSION", version))

from data.print_colors import iprint, wprint, eprint, mprint, sprint, bprint, dprint
bprint("print_colors commands successfully initalized", "init")
import discord, dataset, datetime, time, asyncio, random, os, data.print_colors as print_colors, traceback, threading
from discord.ext import commands
from discord import app_commands
bprint("imports complete", "init")
start_time = round(time.time())

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix="guy!", intents=intents, help_command=None)

db = dataset.connect("sqlite:///data/guy.db")
member_table:dataset.Table = db["members"]

WARN_MAX = 3
EMOJI_MAX = 5
emoji_id = 1206301600163958898
ohlala_emoji = 1209351601609904178
guy_extra_id = 1210848336106749982
message_rate_limit = 0

rizzler_id = 735192922768801853
verification_channel_id = 1211260299101872210
verification_msg = 1211261306204725268
verified_role_id = 1211253170186092614

restart_count = int(open("data/restart_count.txt","r").read())
restart_count += 1
with open("data/restart_count.txt", "w") as f:
    f.write(str(restart_count))

if os.path.exists("data/color_roles.json") is False:
    role_ids = {}
else: 
    role_ids = json.load(open("data/color_roles.json","r"))

voice_channel = None
print_messages = False
print_whatever_the_fuck = False
progressive_active = False
progressive_class = None

trigger_emoji = [raw_line.split("||")[0] for raw_line in open("data/keys.txt", "r").read().splitlines()]
people_to_key_ids = [int(raw_line.split("||")[1]) for raw_line in open("data/keys.txt", "r").read().splitlines()]
link_to_send = [raw_line.split("||")[2] for raw_line in open("data/keys.txt", "r").read().splitlines()]

bprint("details set, now waiting for API/library to give us the ready call", "init")

@bot.tree.command(description="See how long guy. has been up for.")
async def uptime(interaction: discord.Interaction):
    await interaction.response.send_message("guy. has restarted <t:%s:R>.\nThe next restart would be number %s." %(str(start_time), restart_count+1), ephemeral=True)
    return

@bot.tree.command(description="Give yourself a colorful role.")
@app_commands.describe(color="Have a pre-defined color? Send the ID here.")
@app_commands.describe(r="Red value.")
@app_commands.describe(g="Green value.")
@app_commands.describe(b="Blue value.")
async def set_color(interaction: discord.Interaction, color:str|None, r:int|None, g:int|None, b:int|None):
    if r>=256 or r<0:
        r = None
    if g>=256 or g<0:
        g = None
    if b>=256 or b<0:
        b = None
    await interaction.response.send_message("Work in progress.", ephemeral=True)
    return

async def member_warn(member: discord.Member, warn_count: int):
    member_entry:dict = member_table.find_one(user_id=member.id)
    if member_entry is None:
        member_table.insert(dict(user_id=member.id, username=member.name, warns=warn_count))
        member_entry = member_table.find_one(user_id=member.id)
    else:
        member_entry["warns"]+=warn_count
        member_table.update(member_entry, ["id"])
    db.commit()
    if member_entry["warns"]>=WARN_MAX:
        await member.ban(reason="guy: member exceeded warn count of %s" %WARN_MAX)
        return

async def start_pulse():
    global message_rate_limit
    while True:
        await asyncio.sleep(10)
        if message_rate_limit > 0:
            message_rate_limit -= 1
            iprint("decremented message_rate_limit to %s" %message_rate_limit, "on_ready.start_pulse")

def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(start_pulse())
    loop.close()

@bot.event
async def on_ready():
    bprint("ready call hit!", "on_ready")
    bprint("signed in as %s (restart count: %s)" %(bot.user, restart_count), "on_ready")
    _thread = threading.Thread(target=between_callback)
    _thread.daemon = True
    _thread.start()
    bprint("all prints from here are by consequence of functions. enjoy guy.!", "on_ready")
    # .silly
    while True:
        await asyncio.sleep(0.001)
        if print_whatever_the_fuck:
            sprint("on_ready")

async def get_message(guild: discord.Guild, channel_id: int, message_id: int):
    channel = discord.utils.get(guild.channels, id=channel_id)
    if channel is None:
        wprint("no channel found, bailing from fetch", "get_message")
        return None
    saved_message = await channel.fetch_message(message_id)
    if saved_message is None:
        wprint("no message found, fetch failed", "get_message")
        return
    return saved_message

class PulseProgress:
    progress_count = 0
    response = None
    
    def __init__(self):
        iprint("progress trigger hit; if on_message.progress is setup correctly, you should only see this once", "PulseProgress.__init__")
        self.progress_count = int(open("data/progress_count.txt", "r").read())
        self.response = open("data/progress.txt", "r").read().splitlines()[self.progress_count]
    
    async def send_message(self, channel: discord.TextChannel | discord.DMChannel):
        if self.progress_count != int(open("data/progress_count.txt", "r").read()):
            wprint("internal progress_count not equal to saved progress_count, assuming it has been edited and saving self to that", "PulseProgress.send_message")
            self.progress_count = int(open("data/progress_count.txt", "r").read())
            self.response = open("data/progress.txt", "r").read().splitlines()[self.progress_count]
            return 0
        if self.response.startswith("[") is False:
            await channel.send("`PT: %s`" %self.response)
        else:
            await channel.send("`%s`" %self.response)
        if self.response == "[ CONNECTION TERMINATED ]":
            return -1
        self.progress_count += 1
        with open("data/progress_count.txt", "w") as f:
            f.write(str(self.progress_count))
        self.response = open("data/progress.txt", "r").read().splitlines()[self.progress_count]
        return 0

@bot.event
async def on_message(message: discord.Message):
    # .on_message
    if message.author == bot.user: return
    msgcont = message.content.replace("<@%s>" %str(bot.user.id), "(guy ping)")
    global message_rate_limit, people_to_key_ids, trigger_emoji, link_to_send, print_messages, print_whatever_the_fuck
    if len(message.attachments)!=0: msgcont += " (attachments)"
    if message.guild is None: msgcont += " (in DMs)"
    mprint("%s: %s" %(message.author.name, " ; ".join([line for line in msgcont.splitlines() if len(line) != 0])), "on_message") if message.guild is None else None # dms will always be recorded
    if "rot" in message.content.lower():
        # .rotify
        message_content = message.content.lower().split(" ")
        if "rot" not in message_content: return
        try:
            await message.author.send(file=discord.File(open("pictures/woe.png", "rb")))
        except discord.errors.Forbidden:
            wprint("%s has us blocked so we couldn't rotify them. very unfortunate. unfortunate indeed." %message.author, "on_message.rotify")
    if "karma 2" in message.content.lower():
        # .ohlala
        try:
            emoji = discord.utils.get(message.guild.emojis, id=ohlala_emoji)
            if emoji is None:
                wprint("ohlala appears to have been deleted; bailing", "on_message.ohlala")
                return
            await message.add_reaction(emoji)
        except discord.errors.Forbidden:
            wprint("damn it. doggo is stinky, we can't react with :ohlala:.", "on_message.ohlala")
    # if rizzler_id == message.author.id:
    #     # .ohlala_rizzler
    #     try:
    #         emoji = discord.utils.get(message.guild.emojis, id=ohlala_emoji)
    #         if emoji is None:
    #             wprint("ohlala appears to have been deleted; bailing", "on_message.ohlala_rizzler")
    #             return
    #         await message.add_reaction(emoji)
    #     except discord.errors.Forbidden:
    #         wprint("damn it. doggo is stinky, we can't react with :ohlala: to rizzler. fuck.", "on_message.ohlala_rizzler")
    # ^ guarddoggo stinks so i guess we're commenting this out
    if os.path.exists("data/dms.txt") is False and message.guild is None:
        with open("data/dms.txt", "wb") as f:
            f.write(bytes("%s: %s" %(message.author, message.content), encoding="utf8"))
    elif message.guild is None:
        with open("data/dms.txt", "ab") as f:
            f.write(bytes("\n%s: %s" %(message.author, message.content), encoding="utf8"))
    mprint("%s: %s" %(message.author.name, " ; ".join([line for line in msgcont.splitlines() if len(line) != 0])), "on_message") if print_messages is True else None
    if "nigg" in message.content.lower() or "n1gg" in message.content.lower() or "n!gg" in message.content.lower() and message.guild is not None:
        wprint("%s hit our n-word filter in the #%s channel. highly recommending to annihilate them." %(message.author, message.channel.name), "on_message.nword")
        if member_table.find_one(user_id=message.author.id) is None:
            delta = datetime.datetime.now().astimezone()+datetime.timedelta(seconds=604800)
            member_table.insert(dict(user_id=message.author.id, username=message.author.name, warns=2))
            db.commit()
            await message.author.timeout(delta, reason="guy: n-word filter | timeout, heavy warn")
            await message.delete()
            await message.author.send("Do not say that again.", file=discord.File(open("pictures/no.gif", "rb")))
            iprint("user %s got dangerously close or exceeded n-word filter; has been warned, warn_count now 2" %message.author.name, "on_message")
            return
        else:
            #user has been warned already, they have an entry after all; kill them on sight
            await message.author.ban(reason="guy: n-word filter | ban")
            iprint("user %s got dangerously close or exceeded n-word filter; has been banned due to past infractions" %message.author.name, "on_message")
            return
    if message.channel.id == 1206439927420690483 or message.channel.id == 1204877106190880778 or (message.guild is None and message.author.id == 434805711625519105):
        # .guy_channel
        responses:list[str] = open("data/responses.txt", "r").read().splitlines()
        for line in responses:
            if "progress" in message.content.lower() and "progressive" not in message.content.lower():
                # .progress

                # progress_count = int(open("data/progress_count.txt", "r").read())
                # response = open("data/progress.txt", "r").read().splitlines()[progress_count]
                # if response == "[ CONNECTION TERMINATED ]": await message.reply("`%s`" %response, mention_author=False); return
                # iprint("progress: %s" %str(progress_count), "on_message.guy_channel.progress")
                # progress_count += 1
                # with open("data/progress_count.txt", "w") as f:
                #     f.write(str(progress_count))
                # if response.startswith("[") is False: await message.reply("`PT: %s`" %response, mention_author=False)
                # else: await message.reply("`%s`" %response, mention_author=False)
                # return
                #^ previous progress activity

                global progressive_active, progressive_class
                if progressive_class is not None: return
                if progressive_active is False: progressive_active = True; progressive_class = PulseProgress()
                while progressive_active is True:
                    if await progressive_class.send_message(message.channel) != 0:
                        progressive_class = None
                        progressive_active = False
                        iprint("progressive_class returned a nonzero integer, assuming that we have reached the end", "on_message.progress")
                        return
                    await asyncio.sleep(30)
            
            is_ping = line.split("||")[0]=="p"
            tag_to_watch = line.split("||")[1].split('"')[0]
            response = None if len(line.split("||")[1].split('"')[1].split("f;"))>1 == False else line.split("||")[1].split('"')[1].replace("_AUTHOR", message.author.mention).replace("\\n", "\n")
            if len(line.split("||")[1].split('"')[1].split("f;"))>1:
                file = discord.File(open("pictures/"+line.split("||")[1].split('"')[1].split("f;")[1], "rb"))
                response = line.split("||")[1].split('"')[1].split("f;")[0].rstrip()
            else:
                file = None
            if is_ping:
                #.is_ping
                if tag_to_watch in message.content.lower() and bot.user in message.mentions:
                    iprint("message hit our tag_to_watch (%s)" %(tag_to_watch), "on_message.guy_channel.is_ping")
                    if "rand;" not in tag_to_watch:
                        rand_list = line.split("||")[1].split('"')[1].lstrip("rand;").split("'") if line.split("||")[1].split('"')[1].startswith("rand;") is True else None
                        if rand_list is not None:
                            cur_state = random.getstate()
                            random.seed(message.author.name + "".join([x for x in message.content.split(" ") if len(x)>1]))
                            response = random.choice(rand_list)
                            if len(rand_list)==1:
                                response = "f;"+random.choice([response[7:]+"/"+file for file in os.listdir("pictures/%s" %response[7:])]) if response.startswith("folder;") else response
                            file = discord.File(open("pictures/"+response.lstrip("f;"), "rb")) if response.startswith("f;") else None
                            if file is not None:
                                response = "`%s`" %response.split("/")[1]
                            random.setstate(cur_state)
                    await message.reply(response, mention_author=False, file=file)
                    del responses
                    return
            else:
                #.no_ping
                if tag_to_watch in message.content.lower() and bot.user not in message.mentions:
                    iprint("message hit our tag_to_watch (%s)" %(tag_to_watch), "on_message.guy_channel.no_ping")
                    rand_list = line.split("||")[1].split('"')[1].lstrip("rand;").split("'") if line.split("||")[1].split('"')[1].startswith("rand;") is True else None
                    if "rand;" in tag_to_watch:
                        cur_state = random.getstate()
                        random.seed(message.author.name + "".join([x for x in message.content.split(" ") if len(x)>1]))
                        response = random.choice(rand_list)
                        if len(rand_list)==1:
                            response = "f;"+random.choice([response[7:]+"/"+file for file in os.listdir("pictures/%s" %response[7:])]) if response.startswith("folder;") else response
                        file = discord.File(open("pictures/"+response.lstrip("f;"), "rb")) if response.startswith("f;") else None
                        if file is not None:
                            response = "`%s`" %response.split("/")[1]
                        random.setstate(cur_state)
                    await message.reply(response, mention_author=False, file=file)
                    del responses
                    if response is None:
                        return
                    if "i love trees" in response:
                        for i in range(10):
                            await message.channel.send("I LOVE TREES. "*10)
                    return
    try:
        if "doggy" in message.content.lower():
            reference = message.reference
            if reference is None:
                return
            ref_message = await get_message(message.guild, message.channel.id, reference.message_id)
            if ref_message is None: return
            if ref_message.author.id != 724229957177442344: return
            await message.reply("What the fuck is wrong with you.")
            return
    except discord.errors.HTTPException:
        return
    if message.author.id != 434805711625519105: return
    if "g!sync" in message.content.lower():
        await bot.tree.sync()
        iprint("resynced commands", "on_message.g!sync")
        await message.add_reaction("✅")
        return
    global voice_channel
    if "g!connect" in message.content.lower():
        channel = message.channel if type(message.channel) is discord.VoiceChannel else None
        if channel is None:
            await message.add_reaction("❌")
        voice_channel = await channel.connect()
        iprint("connected successfully", "on_message.g!connect")
    if "g!play" in message.content.lower():
        message_content = message.content.lower().split()
        if len(message_content)==1:
            await message.reply(":x:")
            return
        try:
            if voice_channel is not None: voice_channel.play(discord.FFmpegPCMAudio("audio/"+message_content[1]))
            else:
                channel = message.channel if type(message.channel) is discord.VoiceChannel else None
                if channel is None:
                    await message.add_reaction("❌")
                voice_channel = await channel.connect()
                voice_channel.play(discord.FFmpegPCMAudio("audio/"+message_content[1]))
            iprint("playing audio %s" %message_content[1], "on_message.g!play")
        except Exception as e:
            await message.reply(":x:")
            eprint("error playing audio %s" %message_content[1], "on_message.g!play")
            raise e
    if "g!stop" in message.content.lower():
        if voice_channel is not None: 
            try:
                await voice_channel.stop()
            except TypeError:
                wprint("weirdo wackiness where voice_channel is both None and not None. thanks, discord.py library", "on_message.g!stop")
        iprint("stopped audio", "on_message.g!stop")
    if "g!disconnect" in message.content.lower():
        if voice_channel is not None:
            await voice_channel.disconnect()
            voice_channel = None
        iprint("disconnected successfully", "on_message.g!disconnect")
    if "g!say" in message.content.lower():
        guild = discord.utils.get(bot.guilds, id=1205638060604264448)
        promotions = discord.utils.get(guild.text_channels, id=1205645246336081971)
        await promotions.send(" ".join(message.content.split(" ")[1:]))
        iprint("sent message in #promotions: %s" %" ".join(message.content.split(" ")[1:]), "on_message.g!say")
        return
    if "g!perms" in message.content.lower():
        guild = discord.utils.get(bot.guilds, id=1205638060604264448)
        me = guild.me
        gp = me.guild_permissions
        permissions = [gp.add_reactions,
                       gp.administrator,
                       gp.attach_files,
                       gp.ban_members,
                       gp.change_nickname,
                       gp.connect,
                       gp.create_expressions,
                       gp.create_instant_invite,
                       gp.create_private_threads,
                       gp.create_public_threads,
                       gp.deafen_members,
                       gp.embed_links,
                       gp.external_emojis,
                       gp.external_stickers,
                       gp.kick_members,
                       gp.manage_channels,
                       gp.manage_emojis,
                       gp.manage_emojis_and_stickers,
                       gp.manage_events,
                       gp.manage_expressions,
                       gp.manage_guild,
                       gp.manage_messages,
                       gp.manage_nicknames,
                       gp.manage_permissions,
                       gp.manage_roles,
                       gp.manage_threads,
                       gp.manage_webhooks,
                       gp.mention_everyone,
                       gp.moderate_members,
                       gp.move_members,
                       gp.mute_members,
                       gp.priority_speaker,
                       gp.read_message_history,
                       gp.read_messages,
                       gp.request_to_speak,
                       gp.send_messages,
                       gp.send_messages_in_threads,
                       gp.send_tts_messages,
                       gp.send_voice_messages,
                       gp.speak,
                       gp.stream,
                       gp.use_application_commands,
                       gp.use_embedded_activities,
                       gp.use_external_emojis,
                       gp.use_external_sounds,
                       gp.use_external_stickers,
                       gp.use_soundboard,
                       gp.view_audit_log,
                       gp.view_channel,
                       gp.view_guild_insights,
                       gp.value]
        name_perms = ["add_reactions",
                       "administrator",
                       "attach_files",
                       "ban_members",
                       "change_nickname",
                       "connect",
                       "create_expressions",
                       "create_instant_invite",
                       "create_private_threads",
                       "create_public_threads",
                       "deafen_members",
                       "embed_links",
                       "external_emojis",
                       "external_stickers",
                       "kick_members",
                       "manage_channels",
                       "manage_emojis",
                       "manage_emojis_and_stickers",
                       "manage_events",
                       "manage_expressions",
                       "manage_guild",
                       "manage_messages",
                       "manage_nicknames",
                       "manage_permissions",
                       "manage_roles",
                       "manage_threads",
                       "manage_webhooks",
                       "mention_everyone",
                       "moderate_members",
                       "move_members",
                       "mute_members",
                       "priority_speaker",
                       "read_message_history",
                       "read_messages",
                       "request_to_speak",
                       "send_messages",
                       "send_messages_in_threads",
                       "send_tts_messages",
                       "send_voice_messages",
                       "speak",
                       "stream",
                       "use_application_commands",
                       "use_embedded_activities",
                       "use_external_emojis",
                       "use_external_sounds",
                       "use_external_stickers",
                       "use_soundboard",
                       "view_audit_log",
                       "view_channel",
                       "view_guild_insights",
                       "value"
        ]
        line = ""
        for index, elem in enumerate(name_perms):
            if index==len(name_perms)-1:
                line += elem+": "+str(permissions[index])
                break
            emoji = ["❌", "✅"]
            line += elem+": "+emoji[int(permissions[index])]+"\n"
        await message.reply(line)
        return
    if "g!securethisfuck" in message.content.lower():
        person_id = int(message.content.split(" ")[1])
        person = discord.utils.get(message.guild.members, id=person_id)
        iprint("target found: %s" %person.name, "on_message.g!securethisfuck")
        for channel in message.guild.channels:
            if channel.id != 1207393047592042577 and channel.id != 1209615521276764200:
                try: 
                    await channel.set_permissions(person, reason="g: fuck you", view_channel=False)
                    if type(channel) is discord.VoiceChannel:
                        await channel.set_permissions(person, reason="g: fuck you", view_channel=False, connect=False)
                except discord.errors.Forbidden:
                    wprint("missing permissions in %s" %channel.name, "on_message.g!securethisfuck")
                    continue
            else:
                try: 
                    await channel.set_permissions(person, reason="g: fuck you", view_channel=True, send_messages=True)
                    if type(channel) is discord.VoiceChannel:
                        await channel.set_permissions(person, reason="g: fuck you", view_channel=True, send_messages=True, connect=True)
                except discord.errors.Forbidden:
                    wprint("missing permissions in %s" %channel.name, "on_message.g!securethisfuck")
                    continue
        await message.reply("Done.")
        return
    if "g!undosecuring" in message.content.lower():
        person_id = int(message.content.split(" ")[1])
        person = discord.utils.get(message.guild.members, id=person_id)
        iprint("target found: %s" %person.name, "on_message.g!securethisfuck")
        for channel in message.guild.channels:
            if channel.id != 1207393047592042577 and channel.id != 1209615521276764200:
                try: 
                    await channel.set_permissions(person, reason="g: be free", view_channel=True)
                    if type(channel) is discord.VoiceChannel:
                        await channel.set_permissions(person, reason="g: be free", view_channel=True, connect=True)
                except discord.errors.Forbidden:
                    wprint("missing permissions in %s" %channel.name, "on_message.g!undosecuring")
                    continue
            else:
                try: 
                    await channel.set_permissions(person, reason="g: be free", view_channel=True, send_messages=True)
                    if type(channel) is discord.VoiceChannel:
                        await channel.set_permissions(person, reason="g: be free", view_channel=True, send_messages=True, connect=True)
                except discord.errors.Forbidden:
                    wprint("missing permissions in %s" %channel.name, "on_message.g!undosecuring")
                    continue
        await message.reply("Done.")
        return
    if "g!printmessages" in message.content.lower():
        print_messages = print_messages is False
        iprint("print_messages has now been set to %s" %str(print_messages).lower(), "on_message.g!printmessage")
        await message.add_reaction(["❌", "✅"][int(print_messages)])
        return
    if "g!printsilly" in message.content.lower():
        print_whatever_the_fuck = print_whatever_the_fuck is False
        iprint("print_whatever_the_fuck has now been set to %s" %str(print_whatever_the_fuck).lower(), "on_message.g!printsilly")
        await message.add_reaction(["❌", "✅"][int(print_whatever_the_fuck)])
        return
    if "g!shutup" in message.content.lower():
        iprint("time to shut everyone tf up about @everyone and @here", "on_message.g!shutup")
        for channel in message.guild.channels:
            try: 
                await channel.set_permissions(message.guild.default_role, reason="g: shut up", mention_everyone=False)
            except discord.errors.Forbidden:
                wprint("missing permissions in %s" %channel.name, "on_message.g!shutup")
                continue
        await message.reply("Done. This seems like a weird request, but it's done.")
        return
    if "g!lockdown" in message.content.lower():
        channel = message.channel
        overwrite = channel.overwrites_for(message.guild.default_role)
        lock = True
        if overwrite.send_messages is True:
            lock = False
        person_id = rizzler_id
        person = discord.utils.get(message.guild.members, id=person_id)
        bossman_id = 434805711625519105
        bossman = discord.utils.get(message.guild.members, id=bossman_id)
        await channel.set_permissions(message.guild.default_role, reason="g: lockdown", send_messages=lock)
        if channel.id == 1207393047592042577: await channel.set_permissions(person, reason="g: lockdown", send_messages=True)
        await channel.set_permissions(bossman, reason="g: lockdown", send_messages=True)
    if "g!sendverify" in message.content.lower():
        await message.delete()
        gmsg = await message.channel.send("**React** to the ✅ emoji below to show that you have read the rules and agree to them.")
        iprint("successfully sent reaction msg with id %s" %gmsg.id, "on_message.g!sendverify")
        wprint("MAKE SURE TO UPDATE THIS IN GUY'S CODE. I SWEAR TO GOD, IF SOMEBODY TOLD ME TO CHANGE THIS, AND I DON'T CHANGE THE VARIABLES, IM GOING TO DROP A WARHEAD", "on_message.g!sendverify")
        await gmsg.add_reaction("✅")
    if "g!memberify" in message.content.lower():
        gmsg = await message.reply("Gathering members...")
        members = await message.guild.chunk()
        verified_role = discord.utils.get(message.guild.roles, id=verified_role_id)
        if verified_role is None:
            await gmsg.edit(content="Bailed.")
            eprint("verified role missing, bailing", "on_message.g!memberify")
        error_count = 0
        for index, member in enumerate(members):
            try:
                await member.add_roles(verified_role, reason="g: grandfathered")
                await gmsg.edit(content="%s out of %s (%s error(s))" %(index, len(members), error_count))
            except Exception as e:
                wprint("had an error, assuming to be forbidden and continuing")
                error_count += 1
                wprint(e)
                continue
        await gmsg.edit(content="Done.")

@bot.event
async def on_raw_reaction_add(payload: discord.RawReactionActionEvent):
    # payload
    #  - channel_id
    #  - guild_id (if applicable)
    #  - emoji_id (if not unicode, else return unicode character)
    #  - member (if adding reaction + in a guild)

    global message_rate_limit, emoji_id, people_to_key_ids, trigger_emoji, link_to_send
    if payload.member is None:
        return
    guild = discord.utils.get(bot.guilds, id=payload.guild_id)
    if guild is None:
        return None
    if payload.member == guild.me: return

    # .verify
    saved_message = await get_message(guild, payload.channel_id, payload.message_id)
    if saved_message is None:
        iprint("fetch returned nothing, bailing", "on_raw_reaction_add.verify")
        return
    if saved_message.channel.id == verification_channel_id:
        if payload.message_id == verification_msg:
            if "✅" in payload.emoji.name:
                verified_role = discord.utils.get(guild.roles, id=verified_role_id)
                if verified_role is None:
                    eprint("verified_role appears to have been lost, immediately bailing", "on_raw_reaction_add.verify")
                    return
                try:
                    await payload.member.add_roles(verified_role)
                    iprint("successfully added role to user %s" %payload.member)
                    return
                except Exception as e:
                    eprint("didn't have permissions to add role to user %s! bailing" %payload.member, "on_reaction_add.verify")
                    eprint("isn't reporting a forbidden, so we're raising it for the next step up to find out what's going on", "on_raw_reaction_add.verify")
                    raise e
        wprint("channel ID match, but incorrect message? how? bailing", "on_raw_reaction_add.verify")
        return

    if payload.emoji.id != emoji_id:
        trigger_emoji = [raw_line.split("||")[0] for raw_line in open("data/keys.txt", "r").read().splitlines()]
        people_to_key_ids = [int(raw_line.split("||")[1]) for raw_line in open("data/keys.txt", "r").read().splitlines()]
        link_to_send = [raw_line.split("||")[2] for raw_line in open("data/keys.txt", "r").read().splitlines()]

        if "🔑" in payload.emoji.name or "🗝️" in payload.emoji.name:
            # .key
            if saved_message.author.id not in people_to_key_ids: return
            index = people_to_key_ids.index(saved_message.author.id)
            if "key" != trigger_emoji[index]: return
            try:
                await saved_message.author.send("%s\n%s" %(random.choice(open("data/responses_dm.txt","r").read().splitlines()), link_to_send[index]))
                iprint("sent message to %s for key" %saved_message.author.name, "on_raw_reaction_add.key")
            except discord.errors.Forbidden:
                wprint("user %s has me blocked, unable to send message" %saved_message.author.name, "on_raw_reaction_add.key")
            if message_rate_limit==0 or saved_message.channel.id == 1206439927420690483:
                try:
                    await saved_message.reply(" ".join(["KEYS!!!" for x in range(random.randint(2, 5))]))
                except discord.errors.Forbidden:
                    wprint("channel %s won't let me chat, bailing" %saved_message.channel.name, "on_raw_reaction_add.key")
            if saved_message.channel.id != 1206439927420690483: message_rate_limit += 1; iprint("incremented to message_rate_limit; %s" %message_rate_limit, "on_raw_reaction_add.key")
            return
        if "🍯" in payload.emoji.name:
            # .bee (although honey)
            if saved_message.author.id not in people_to_key_ids: return
            index = people_to_key_ids.index(saved_message.author.id)
            if "bee" != trigger_emoji[index]: return
            try:
                await saved_message.author.send("%s\n%s" %(random.choice(open("data/responses_dm.txt","r").read().splitlines()), link_to_send[index]))
                iprint("sent message to %s for bee" %saved_message.author.name, "on_raw_reaction_add.bee")
            except discord.errors.Forbidden:
                wprint("user %s has me blocked, unable to send message" %saved_message.author.name, "on_raw_reaction_add.bee")
            if message_rate_limit==0 or saved_message.channel.id == 1206439927420690483:
                try:
                    await saved_message.reply("I LOVE HONEY.")
                except discord.errors.Forbidden:
                    wprint("channel %s won't let me chat, bailing" %saved_message.channel.name, "on_raw_reaction_add.key")
            if saved_message.channel.id != 1206439927420690483: message_rate_limit += 1; iprint("incremented to message_rate_limit; %s" %message_rate_limit, "on_raw_reaction_add.bee")
            return
        if "💬" in payload.emoji.name:
            #.extract
            if payload.user_id == 434805711625519105:
                channel_list = [channel for channel in guild.text_channels]
                messages = []
                iprint("fetching shit from %s" %saved_message.author.name, "on_raw_reaction_add.extract")
                for index, channel in enumerate(channel_list):
                    c_start_time = time.time()
                    try:
                        channel_messages = [message async for message in channel.history(limit=2500) if message.author.id == saved_message.author.id]
                    except discord.errors.Forbidden:
                        wprint("no perms in %s, assuming to be an unavailable channel. probably wont find them there anyway" %channel.name, "on_raw_reaction_add.extract")
                        continue
                    for message in channel_messages:
                        messages.append(message)
                    c_end_time = round(time.time()-c_start_time, 3)
                    iprint("done in %s in %s seconds (%s/%s)" %(channel.name, c_end_time, index+1, len(channel_list)), "on_raw_reaction_add.extract")
                bossman = discord.utils.get(guild.members, id=payload.user_id)
                with open("data/characterai.txt", "w") as f:
                    string_to_write = ""
                    for message in messages:
                        if len(message.content) <= 1:
                            continue
                        string_to_write += "{{char}}: %s\n" %message.content.replace("\n", " ")
                    string_to_write = string_to_write.rstrip()
                    f.write(string_to_write)
                await bossman.send("%s messages in list" %len(messages), file=discord.File(open("data/characterai.txt", "rb")))
                return
            else:
                iprint("bro thought lmao", "on_raw_reaction_add.extract")
                return

        return

    # .spearmaster
    emoji = discord.utils.get(guild.emojis, id=payload.emoji.id)
    if emoji is None:
        eprint("wtf? where is :saythatagain:? what happened? ragh?", "on_raw_reaction_add.spearmaster")
        return
    
    saved_message = await get_message(guild, payload.channel_id, payload.message_id)
    if saved_message is None:
        return
    for react_emoji in saved_message.reactions:
        if react_emoji.emoji == emoji:
            if react_emoji.count>=EMOJI_MAX:
                if saved_message.author.id==724229957177442344: return
                if saved_message.pinned is True: return
                try:
                    await saved_message.delete()
                except discord.errors.Forbidden:
                    eprint("couldn't delete message due to lack of permissions. go kill guarddoggo or smth idk", "on_raw_reaction_add.spearmaster")
                return

@bot.event
async def on_message_delete(message: discord.Message):
    if message.author == bot.user or message.author.bot: return
    iprint("saw a message get deleted by %s; we're throwing it into the log channel" %message.author, "on_message_delete")
    iprint("message: %s" %message.content, "on_message_delete")
    log_channel = discord.utils.get(message.guild.channels, id=guy_extra_id)
    if log_channel is None:
        return
    else:
        embed = discord.Embed(color=discord.Color.red(), title="A message by %s got deleted in the %s channel." %(message.author, message.channel), description="Message: %s" %message.content)
        async for log in message.guild.audit_logs(limit=10, action=discord.AuditLogAction.message_delete):
            if log.target == message.author:
                embed.set_footer(text="%s deleted this message. | message ID: %s" %(log.user, message.id))
        if embed.footer.text is None:
            embed.set_footer(text="message ID: %s" %message.id)
        await log_channel.send(embed=embed)

@bot.event
async def on_message_edit(before: discord.Message, after: discord.Message):
    if before.author == bot.user or before.author.bot: return
    if before.content == after.content: return
    iprint("saw a message get edited by %s; throwing it into the log channel" %before.author, "on_message_edit")
    iprint("before: %s" %before.content, "on_message_edit")
    iprint("after: %s" %after.content, "on_message_edit")
    log_channel = discord.utils.get(before.guild.channels, id=guy_extra_id)
    if log_channel is None:
        return
    else:
        embed = discord.Embed(color=discord.Color.yellow(), title="A message by %s got edited in the %s channel." %(before.author, before.channel), description="Before: %s" %before.content)
        embed.set_footer(text="After: %s" %after.content)
        await log_channel.send(embed=embed)

@bot.event
async def on_member_join(member: discord.Member):
    iprint("%s just joined the server. hello!" %member)
    log_channel = discord.utils.get(member.guild.channels, id=guy_extra_id)
    if log_channel is None: return
    embed = discord.Embed(color=discord.Color.green(), title="%s just joined the server!" %member, description="Say hello to them! They are member number %s!" %member.guild.member_count)
    await log_channel.send(embed=embed)

@bot.event
async def on_member_remove(member: discord.Member):
    iprint("%s just left the server. bye bye!" %member)
    log_channel = discord.utils.get(member.guild.channels, id=guy_extra_id)
    if log_channel is None: return
    embed = discord.Embed(color=discord.Color.yellow(), title="%s just left the server!" %member, description="Bye bye! We now have %s members." %member.guild.member_count)
    await log_channel.send(embed=embed)

@bot.event
async def on_member_ban(guild: discord.Guild, member: discord.User|discord.Member):
    iprint("%s just got banned!" %member)
    log_channel = discord.utils.get(guild.channels, id=guy_extra_id)
    if log_channel is None: return
    embed = discord.Embed(color=discord.Color.red(), title="%s was just banned the server!" %member, description="Whatever did they do!?")
    await log_channel.send(embed=embed)

@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    if after.timed_out_until is not None and before.timed_out_until is None:
        iprint("%s was just timed out" %after)
        log_channel = discord.utils.get(after.guild.channels, id=guy_extra_id)
        if log_channel is None: return
        embed = discord.Embed(color=discord.Color.yellow(), title="%s was just timed out!" %after, description="Whatever did they do?")
        await log_channel.send(embed=embed)

@bot.event
async def on_error(event: str, *args, **kwargs):
    tb = traceback.format_exc()
    eprint("caught an error in guy.%s\n%s%s%s" %(event, print_colors.print_colors.fg.red, tb, print_colors.print_colors.reset))

bot.run(open("data/token.txt", "r").read())
