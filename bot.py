import discord
from dotenv import load_dotenv
from discord import app_commands
from discord.ext import commands
from discord import Webhook
import aiohttp
import asyncio
import json
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
#model = AutoModel.from_pretrained('/home/user/.cache/huggingface/hub/models--databricks--dolly-v2-7b/snapshots/97611f20f95e1d8c1e914b85da55cc3937c31192')
# instruct_pipeline = pipeline(model="databricks/dolly-v2-7b", torch_dtype=torch.bfloat16, trust_remote_code=True, device_map="auto")
with open('setting.json','r',encoding='utf8') as jfile:
  setting = json.load(jfile)
with open('./setting/world_config.json','r',encoding='utf8') as jfile:
  world_config = json.load(jfile)


bot = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(bot)

@bot.event
async def on_ready():
    await tree.sync()
    print("Ready!")

@tree.command(name = "restart")
async def restart(i: discord.Interaction):
    with open('webhook_url.json','r',encoding='utf8') as jfile:
        webhook_url = json.load(jfile)
    with open('world.json','r',encoding='utf8') as jfile:
        world = json.load(jfile)
    with open('./setting/world_config.json','r',encoding='utf8') as jfile:
        world_config = json.load(jfile)

    await i.response.send_message(f'正在重新設置')
    
    for w in webhook_url:
        webhook = await i.guild.webhooks()
        for x in webhook:
            if str(w) == str(webhook.url):
                async with aiohttp.ClientSession() as session:
                    webhook = Webhook.from_url(w, session=session)
                    await webhook.delete(reason="restart")
                    del webhook_url[str(i.guild.id)]

    #刪除頻道
    for g in world:
        if str(g) == str(i.guild_id):
            for w in world[str(i.guild_id)]["world"]:
                for x in world[str(i.guild_id)]["world"][w]:
                    for y in world[str(i.guild_id)]["world"][w][x]:
                        ID = world[str(i.guild_id)]["world"][w][x][y]
                        try:
                            channel = bot.get_channel(ID)
                            await channel.delete()
                        except:
                            pass
    
    world[str(i.guild_id)]={}
    world[str(i.guild_id)]["world"] = world_config

    #新增頻道
    for w in world_config:
        text = f"{i.guild.name}_{w}"
        category = await i.guild.create_category_channel(name=text)
        world[str(i.guild_id)]["world"][w]["category"][text]=category.id
        world_config = world_config[w]
        for x in world_config:
            if x == "channel":
                for y in world_config[x]:
                    channel = await i.guild.create_text_channel(name=y,category=category)
                    world[str(i.guild_id)]["world"][w][x][y]=channel.id
            if x == "voicechannel":
                for y in world_config[x]:
                    channel = await i.guild.create_voice_channel(name=y,category=category)
                    world[str(i.guild_id)]["world"][w][x][y]=channel.id

    webhook = await i.guild.get_channel(world[str(i.guild_id)]["world"]["start_world"]["channel"]["start"]).create_webhook(name="NPC")
    webhook_url[str(i.guild.id)] = str(webhook.url)
    
    with open('webhook_url.json','w',encoding='utf8') as jfile:
        json.dump(webhook_url,jfile,indent=4)
    with open('world.json','w',encoding='utf8') as jfile:
        json.dump(world,jfile,indent=4)
    await i.edit_original_response(content=f'設定已重置')

temporary_channels = []
temporary_categories = []

#學習重點
@bot.event
async def on_voice_state_update(member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
    possible_channel_name = f"{member.nick}'s area"
    pn = f"{member.nick}發呆" 
    if str(member.nick) == "None":
        pn = f"{member.name}發呆" 
    if after.channel:
        if after.channel.name == "發呆":
            temp_channel = await after.channel.clone(name=pn)
            await member.move_to(temp_channel)
            temporary_channels.append(temp_channel.id)
        # if after.channel.name == 'teams':
        #     temporary_category = await after.channel.guild.create_category(name=possible_channel_name)
        #     await temporary_category.create_text_channel(name="text")
        #     temp_channel = await temporary_category.create_voice_channel(name="voice")
        #     await member.move_to(temp_channel)
        #     temporary_categories.append(temp_channel.id)


    if before.channel:
        if before.channel.id in temporary_channels:
            if len(before.channel.members) == 0:
                await before.channel.delete()
        if before.channel.id in temporary_categories:
            if len(before.channel.members) == 0:
                for channel in before.channel.category.channels:
                    await channel.delete()
                await before.channel.category.delete()

@tree.command(name = "clear")
@app_commands.describe(num="你想要刪除的行數")
async def clear(i: discord.Integration,num:int):
    await i.response.send_message(f"即將刪除{num}則訊息",ephemeral=True)
    await i.channel.purge(limit=num)
    await i.edit_original_response(content=f'已刪除{num}則訊息')
    await asyncio.sleep(2)
    await i.delete_original_response()
    

@tree.command(name = "test")
@app_commands.describe(text="test")
async def test(i: discord.Interaction,text:str):
    with open('webhook_url.json','r',encoding='utf8') as jfile:
        webhook_url = json.load(jfile)

    print(i.response.is_done())

    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url[str(i.guild.id)], session=session)
        await webhook.send(content=text,username="test_bot")

@tree.command(name = "add_twitchstreamer")
@app_commands.describe(twitch_id="twitch_id")
async def add_twitchstreamer(i: discord.Integration,twitch_id:str):
    with open('twitch_id.json','r',encoding='utf8') as jfile:
        tid = json.load(jfile)
    tid[str(twitch_id)] = twitch_id
    with open('twitch_id.json','w',encoding='utf8') as jfile:
        json.dump(tid,jfile,indent=4)
    await i.response.send_message(f"已添加{twitch_id}進列表",ephemeral=True)

#poker

    
bot.run(TOKEN)

