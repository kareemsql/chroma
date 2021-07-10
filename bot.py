# gtx v1, made with love for Chroma.
#Copyright 2021, kareemsql, All rights reserved.

import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import random
import os
import pickle
import sys
import traceback
import re
import aiohttp
import logging

bot = commands.Bot(command_prefix='gtx ')

bot.remove_command('help')

bot.load_extension("cogs.fun")

@bot.event
async def on_ready():
    print ("gtx help | chroma <3")
    print ("running stable, user " + bot.user.name)
    game = discord.Game("gtx help | @chromagrp")
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.event
async def on_member_join(member):
    mention=member.mention
    guild=member.guild
    channel = bot.get_channel(725389930607673384)
    embed = discord.Embed(name="chroma | new member", color=0xF98B88)
    embed.set_author(name="chroma | new member")
    embed.add_field(name="c:", value="**welcome to the chroma discord <3 **" +member.mention, inline=True)
    embed.set_footer(text="gtx beta | by kareem <3", icon_url="https://scontent-iad3-1.cdninstagram.com/v/t51.2885-19/83646915_193095065216493_3896196118190489600_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_ohc=-A5Yap2f_LYAX-yl-CL&oh=799ce9f16b7e0a20c7931b8c23b8da2c&oe=5F1F4DF0")
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    mention=member.mention
    guild=member.guild
    channel = bot.get_channel(725389930607673384)
    embed = discord.Embed(name="chroma | member left", color=0xF98B88)
    embed.set_author(name="chroma | member left")
    embed.add_field(name="c:", value=member.mention +" **has left the chroma discord.** :c", inline=True)
    embed.set_footer(text="gtx beta | by kareem <3", icon_url="https://scontent-iad3-1.cdninstagram.com/v/t51.2885-19/83646915_193095065216493_3896196118190489600_n.jpg?_nc_ht=scontent-iad3-1.cdninstagram.com&_nc_ohc=-A5Yap2f_LYAX-yl-CL&oh=799ce9f16b7e0a20c7931b8c23b8da2c&oe=5F1F4DF0")
    await channel.send(embed=embed)

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban (ctx, member:discord.User=None, reason =None):
    if member == None :                                
        embed=discord.Embed(title="**ban:** incorrect usage", description='''**command:** ban
**information:** permanently restrict them from accessing the server.
**usage:** gtx ban <mention user or ID> <reason>
**example:** gtx ban @roni ♡#0008 bullying.'''.format(member, ctx.message.author), color=0xff00f6)
        await ctx.channel.send(embed=embed)
        
    if  member == ctx.message.author:
        embed=discord.Embed(title="action failed!", description=":x: **you can't ban yourself!**".format(member, ctx.message.author), color=0xff00f6)
        await ctx.channel.send(embed=embed)
        return
    if reason == None:
        reason = "unspecificed"
    message = f"sorry to say you've been banned from **{ctx.guild.name}** for: {reason}. :("
    await member.send(message)
    await ctx.guild.ban(member)
    embed=discord.Embed(title="**request complete.**", description=f'''**ban suceeded.**

**{member}** has been removed from the server :|'''.format(member, ctx.message.author), color=0xace5ee)
    await ctx.channel.send(embed=embed)
    
@bot.command()
async def urmomlolxd(ctx):
    embed = discord.Embed(name="Red", color=0xFF0000)
    embed.set_author(name="Red")
    embed.add_field(name="React for color.", value="React to this message to get the specified color.", inline=True)
    embed.set_footer(text="gtx help | by kareem <3", icon_url="https://cdn.discordapp.com/attachments/764957763813245001/764968076667781160/83646915_193095065216493_3896196118190489600_n.jpg")
    await ctx.send(embed=embed)

@bot.command()
@commands.has_permissions(kick_members=True)
async def kick (ctx, member:discord.User=None, reason =None):
    if member == None :                                
        embed=discord.Embed(title="**kick:** incorrect usage", description='''**command:** kick
**information:** permanently restrict them from accessing the server.
**usage:** gtx kick <mention user or ID> <reason>
**example:** gtx kick @roni ♡#0008 calm down.'''.format(member, ctx.message.author), color=0xff00f6)
        await ctx.channel.send(embed=embed)
        
    if  member == ctx.message.author:
        embed=discord.Embed(title="action failed!", description=":x: **you can't kick yourself!**".format(member, ctx.message.author), color=0xff00f6)
        await ctx.channel.send(embed=embed)
        return
    if reason == None:
        reason = "unspecified."
    message = f"sorry to say you've been kicked from **{ctx.guild.name}** for: {reason}. :("
    await member.send(message)
    await ctx.guild.kick(member)
    embed=discord.Embed(title="**request complete.**", description=f'''**kick complete.**

**{member}** has been kicked from the server.'''.format(member, ctx.message.author), color=0xace5ee)
    await ctx.channel.send(embed=embed)

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h":3600, "s":1, "m":60, "d":86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for v, k in matches:
            try:
                time += time_dict[k]*float(v)
            except KeyError:
                raise commands.BadArgument("{} is an invalid time-key! h/m/s/d are valid!".format(k))
            except ValueError:
                raise commands.BadArgument("{} is not a number!".format(v))
        return time

@bot.command()
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member:discord.Member, *, time:TimeConverter = None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.add_roles(role)
    await ctx.send(("Muted {} for {}s" if time else "Muted {}").format(member, time))
    return
    if time:
        await asyncio.sleep(time)
        await member.remove_roles(role)

@mute.error
async def mute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="mute: incorrect usage", description='''**command:** gtx mute
**information:** send someone to the quiet corner, enjoy the total silence.
**usage:** gtx mute <mention user or ID> <time> <reason>
**example:** gtx mute roni ♡#0008 30m spamming.''')
        await ctx.channel.send(embed=embed)

@bot.command()
@commands.has_permissions(manage_roles=True)
async def unmute(ctx, member:discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    await member.remove_roles(role)
    await ctx.send(("user {} has been unmuted!").format(member))

@unmute.error
async def unmute_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        embed=discord.Embed(title="mute: incorrect usage", description='''**command:** gtx mute
**information:** self explanatory :))
**usage:** gtx unmute <mention user or ID>
**example:** gtx ummute roni ♡#0008''')
        await ctx.channel.send(embed=embed)

@bot.command()
async def ball(ctx):
   await ctx.channel.send(random.choice(["it is certain. :8ball:",
                                         "it is decidedly so. :8ball:",               
                                         "without a doubt. :8ball:",
                                         "yes, definitely. :8ball:",
                                         "you may rely on it. :8ball:",
                                         "as I see it, yes. :8ball:",
                                         "most likely. :8ball:",
                                         "outlook good. :8ball:",
                                         "yes. :8ball:",
                                         "signs point to yes. :8ball:",
                                         "reply hazy, try again. :8ball:",
                                         "ask again later. :8ball:",
                                         "better not tell you now. :8ball:",
                                         "cannot predict now. :8ball:",
                                         "concentrate and ask again. :8ball:",
                                         "don't count on it. :8ball:",
                                         "my reply is no. :8ball:",
                                         "my sources say no. :8ball:",
                                         "outlook not so good. :8ball:",
                                         "very doubtful. :8ball:"]))

@bot.command(pass_context = True)
async def bsay(ctx, *args):
    mesg = ' '.join(args)
    await bot.delete_message(ctx.message)
    return await ctx.message.send(mesg)
                         
@bot.command()
async def edits(ctx):
   await ctx.channel.send(random.choice([" https://streamable.com/qclxc8 ",
                                         " https://streamable.com/ouct5g ",               
                                         " https://streamable.com/sbeme1 ",
                                         " https://streamable.com/gkfhgh ",
                                         " https://streamable.com/0zq8u4 ",
                                         " https://streamable.com/8imyo0 ",
                                         " https://streamable.com/9dbnid ",
                                         " https://streamable.com/oty6cn ",
                                         " https://streamable.com/a3birp ",
                                         " https://streamable.com/1na9ad ",
                                         " https://streamable.com/4sbwys ",
                                         " https://streamable.com/63ro8a ",
                                         " https://streamable.com/urnbik ",
                                         " https://streamable.com/dhk4l9 ",
                                         " https://streamable.com/a6gp4c ",
                                         " https://streamable.com/fyexl3 ",
                                         " https://streamable.com/okpt6n ",
                                         " https://streamable.com/mrqbfk ",
                                         " https://streamable.com/3pmyhg ",
                                         " https://streamable.com/rywbna ",
                                         " https://streamable.com/1vhyoq ",
                                         " https://streamable.com/mh88yc ",
                                         " https://streamable.com/bafi3x ",
                                         " https://streamable.com/77u48v ",
                                         " https://streamable.com/yhx474 ",
                                         " https://streamable.com/zuqopr ",
                                         " https://streamable.com/by5cml ",
                                         " https://streamable.com/yoswut ",
                                         " https://streamable.com/fgzaiy ",
                                         " https://streamable.com/30gmg3 ",
                                         " https://streamable.com/gc5ola ",
                                         " https://streamable.com/ialivc ",
                                         " https://streamable.com/wblbu4 ",
                                         " https://streamable.com/uxhzsy ",
                                         " https://streamable.com/vd2drv ",
                                         " https://streamable.com/kxkta3 ",
                                         " https://streamable.com/0qrmk2 ",
                                         " https://streamable.com/j2rci5 ",
                                         " https://streamable.com/y9febt ",
                                         " https://streamable.com/ondg4f ",
                                         " https://streamable.com/x21jh4 ",
                                         " https://streamable.com/2x2s7u ",
                                         " https://streamable.com/l1dx6t ",
                                         " https://streamable.com/jhuly0 ",
                                         " https://streamable.com/ugsa9y ",
                                         " https://streamable.com/9zpfii ",
                                         " https://streamable.com/7facw0 ",
                                         " https://streamable.com/z0593e ",
                                         " https://streamable.com/zaok0h ",
                                         " https://streamable.com/oa7zru ",
                                         " https://streamable.com/4vpnlo ",
                                         " https://streamable.com/vt6493 ",
                                         " https://streamable.com/iikri3 ",
                                         " https://streamable.com/bzfq19 ",
                                         " https://streamable.com/3hgq2o ",
                                         " https://streamable.com/yurepi ",
                                         " https://streamable.com/p2rg68 ",
                                         " https://streamable.com/imon4r ",
                                         " https://streamable.com/14ys2w ",
                                         " https://streamable.com/nkfz5e ",
                                         " https://streamable.com/8snot7 ",
                                         " https://streamable.com/tfkkna ",
                                         " https://streamable.com/klcc8c ",
                                         " https://streamable.com/rmah9t ",
                                         " https://streamable.com/hb8cvs ",
                                         " https://streamable.com/muvu6y ",
                                         " https://streamable.com/2c7wh4 ",
                                         " https://streamable.com/t541dq ",
                                         " https://streamable.com/yroqkv ",
                                         " https://streamable.com/7e8a48 ",
                                         " https://streamable.com/57jxu6 ",
                                         " https://streamable.com/kywht5 ",
                                         " https://streamable.com/bjtcl4 ",
                                         " https://streamable.com/20m5ui ",
                                         " https://streamable.com/7lcyag ",
                                         " https://streamable.com/xx52ek ",
                                         " https://streamable.com/jalrs7 ",
                                         " https://streamable.com/6i9ao8 ",
                                         " https://streamable.com/ffbmex ",
                                         " https://streamable.com/ssfivn ",
                                         " https://streamable.com/ng9ryq ",
                                         " https://streamable.com/46it8b ",
                                         " https://streamable.com/6cxp4r ",
                                         " https://streamable.com/x64n0a ",
                                         " https://streamable.com/c7123a ",
                                         " https://streamable.com/0dog74 ",
                                         " https://streamable.com/fxj5h6 ",
                                         " https://streamable.com/c05f4u ",
                                         " https://streamable.com/xvklx7 ",
                                         " https://streamable.com/0xsvkt ",
                                         " https://streamable.com/umhq4w ",
                                         " https://streamable.com/mla9yz ",
                                         " https://streamable.com/rxjwte ",
                                         " https://streamable.com/wl6o2v ",
                                         " https://streamable.com/7tkh5o ",
                                         " https://streamable.com/v3wzhy ",
                                         " https://streamable.com/hq1ce1 ",
                                         " https://streamable.com/j1wpou ",
                                         " https://streamable.com/ypxoph ",
                                         " https://streamable.com/0xtm8o ",
                                         " https://streamable.com/m0rs71 ",
                                         " https://streamable.com/j6ksvc ",
                                         " https://streamable.com/zc7bpd ",
                                         " https://streamable.com/31ztz8 ",
                                         " https://streamable.com/14rdga ",
                                         " https://streamable.com/7h1ku2 ",
                                         " https://streamable.com/downte ",
                                         " https://streamable.com/5x5jbi ",
                                         " https://streamable.com/oeby8o ",
                                         " https://streamable.com/96gw5k ",
                                         " https://streamable.com/jlrgdb ",
                                         " https://streamable.com/ddmucd ",
                                         " https://streamable.com/f02o8s ",
                                         " https://streamable.com/buhksh ",
                                         " https://streamable.com/xre4vg ",
                                         " https://streamable.com/xj4wjy ",
                                         " https://streamable.com/hfd29l ",
                                         " https://streamable.com/24vnd6 ",
                                         " https://streamable.com/yww2co ",
                                         " https://streamable.com/g0ft8b ",
                                         " https://streamable.com/lmpwdj ",
                                         " https://streamable.com/fabkr1 ",
                                         " https://streamable.com/lkz0uy ",
                                         " https://streamable.com/k4o3ja ",
                                         " https://streamable.com/2xhnim ",
                                         " https://streamable.com/9n6m9k ",
                                         " https://streamable.com/d3r9n9 ",
                                         " https://streamable.com/omxotd ",
                                         " https://streamable.com/ml783j ",
                                         " https://streamable.com/xtcz7h ",
                                         " https://streamable.com/5fg239 ",
                                         " https://streamable.com/nuvfvg ",
                                         " https://streamable.com/f74ar3 ",
                                         " https://streamable.com/sv7b92 ",
                                         " https://streamable.com/7rpioi ",
                                         " https://streamable.com/8lpjo9 ",
                                         " https://streamable.com/fty0uf ",
                                         " https://streamable.com/lqu8e2 ",
                                         " https://streamable.com/djq8w3 ",
                                         " https://streamable.com/zc1tns ",
                                         " https://streamable.com/6ktpk3 ",
                                         " https://streamable.com/ure0c5 ",
                                         " https://streamable.com/cdat5k ",
                                         " https://streamable.com/yrh3c7 ",
                                         " https://streamable.com/bvljis ",
                                         " https://streamable.com/nwsj4e ",
                                         " https://streamable.com/ufngk7 ",
                                         " https://streamable.com/yo6ng1 ",
                                         " https://streamable.com/kefmvg ",
                                         " https://streamable.com/silafn ",
                                         " https://streamable.com/38ha0x ",
                                         " https://streamable.com/0nxeyc ",
                                         " https://streamable.com/0e4gr5 ",
                                         " https://streamable.com/caa927 ",
                                         " https://streamable.com/hlu6ap ",
                                         " https://streamable.com/l38tez ",
                                         " https://streamable.com/q7k900 ",
                                         " https://streamable.com/66scn2 ",
                                         " https://streamable.com/cv9xap ",
                                         " https://streamable.com/ve9u86 ",
                                         " https://streamable.com/fe2yff ",
                                         " https://streamable.com/i0yz4g ",
                                         " https://streamable.com/lepzei ",
                                         " https://streamable.com/gknc8r ",
                                         " https://streamable.com/thbzsx ",
                                         " https://streamable.com/ib30bt ",
                                         " https://streamable.com/cwtxmz ",
                                         " https://streamable.com/9skry4 ",
                                         " https://streamable.com/zhqla7 ",
                                         " https://streamable.com/yieto5 ",
                                         " https://streamable.com/2lmt4e ",
                                         " https://streamable.com/wfimro ",
                                         " https://streamable.com/dntmp6 ",
                                         " https://streamable.com/087qlf ",
                                         " https://streamable.com/ljr8aa ",
                                         " https://streamable.com/xiciw0 ",
                                         " https://streamable.com/ar9yu8 ",
                                         " https://streamable.com/bsv5zy ",
                                         " https://streamable.com/031y5e ",
                                         " https://streamable.com/g9i6xc ",
                                         " https://streamable.com/ztsyei ",
                                         " https://streamable.com/5vicnh ",
                                         " https://streamable.com/p83pq6 ",
                                         " https://streamable.com/tbh953 ",
                                         " https://streamable.com/c978xp ",
                                         " https://streamable.com/5xxxrs ",
                                         " https://streamable.com/mqq8fw ",
                                         " https://streamable.com/m0t0y7 ",
                                         " https://streamable.com/6nhwtt ",
                                         " https://streamable.com/5mfx9w ",
                                         " https://streamable.com/massq9 ",
                                         " https://streamable.com/8krd65 ",
                                         " https://streamable.com/1ymdkq ",
                                         " https://streamable.com/tkp38m ",
                                         " https://streamable.com/7r2lct ",
                                         " https://streamable.com/041mi8 ",
                                         " https://streamable.com/xdnua7 ",
                                         " https://streamable.com/nubvbp ",
                                         " https://streamable.com/p5a7hu ",
                                         " https://streamable.com/9crfnl ",
                                         " https://streamable.com/cww27q ",
                                         " https://streamable.com/apm1b9 ",
                                         " https://streamable.com/jei8zl ",
                                         " https://streamable.com/93mba9 ",
                                         " https://streamable.com/ppgcs7 ",
                                         " https://streamable.com/7si6rb ",
                                         " https://streamable.com/7xh900 ",
                                         " https://streamable.com/kytqeo ",
                                         " https://streamable.com/ombt6d ",
                                         " https://streamable.com/qts0aq ",
                                         " https://streamable.com/1nzrua ",
                                         " https://streamable.com/wktlvs ",
                                         " https://streamable.com/duj1te ",
                                         " https://streamable.com/fasu4o ",
                                         " https://streamable.com/q2iyx7 ",
                                         " https://streamable.com/xmh00m ",
                                         " https://streamable.com/e631hq ",
                                         " https://streamable.com/dz9gbs ",
                                         " https://streamable.com/bn5fgh ",
                                         " https://streamable.com/kkh9y5 ",
                                         " https://streamable.com/zj346q ",
                                         " https://streamable.com/uhjwmb ",
                                         " https://streamable.com/m2x57p ",
                                         " https://streamable.com/xtieyl ",
                                         " https://streamable.com/ecy0g5 ",
                                         " https://streamable.com/dcn8ph ",
                                         " https://streamable.com/0nud8f ",
                                         " https://streamable.com/jj7d4j ",
                                         " https://streamable.com/utd3gj ",
                                         " https://streamable.com/2syf8t ",
                                         " https://streamable.com/7s0fet ",
                                         " https://streamable.com/46vz4a ",
                                         " https://streamable.com/8tachl ",
                                         " https://streamable.com/13zj9i ",
                                         " https://streamable.com/r6kryd ",
                                         " https://streamable.com/7mn5c5 ",
                                         " https://streamable.com/qm7gno ",
                                         " https://streamable.com/tgebsc ",
                                         " https://streamable.com/4jxmve ",
                                         " https://streamable.com/8ufcxl ",
                                         " https://streamable.com/mrfxjb ",
                                         " https://streamable.com/7wrelc ",
                                         " https://streamable.com/cnkl3o ",
                                         " https://streamable.com/h3hk02 ",
                                         " https://streamable.com/d934kl ",
                                         " https://streamable.com/ev1nvq ",
                                         " https://streamable.com/47fmlq ",
                                         " https://streamable.com/acbjyj ",
                                         " https://streamable.com/1gj4j6 ",
                                         " https://streamable.com/zd4qas ",
                                         " https://streamable.com/humlsm ",
                                         " https://streamable.com/lohw30 ",
                                         " https://streamable.com/a7esiv ",
                                         " https://streamable.com/ea4c29 ",
                                         " https://streamable.com/29d3g5 ",
                                         " https://streamable.com/uu9a2t ",
                                         " https://streamable.com/jzsx93 ",
                                         " https://streamable.com/wen13s ",
                                         " https://streamable.com/snr3fa ",
                                         " https://streamable.com/x0h9ss ",
                                         " https://streamable.com/6xuo3f ",
                                         " https://streamable.com/4l00kl ",
                                         " https://streamable.com/4h66ew ",
                                         " https://streamable.com/lcnw6t ",
                                         " https://streamable.com/8sr8eo ",
                                         " https://streamable.com/6nsdkw ",
                                         " https://streamable.com/8iqv6o ",
                                         " https://streamable.com/7rofje ",
                                         " https://streamable.com/zd5m2o ",
                                         " https://streamable.com/o3qj1s ",
                                         " https://streamable.com/h6dhb1 ",
                                         " https://streamable.com/ex7jjj ",
                                         " https://streamable.com/ijjj4o ",
                                         " https://streamable.com/6ptww8 ",
                                         " https://streamable.com/rowueq ",
                                         " https://streamable.com/ym0523 ",
                                         " https://streamable.com/94o3e5 ",
                                         " https://streamable.com/vtu6jv ",
                                         " https://streamable.com/89i3hv ",
                                         " https://streamable.com/ol96ez ",
                                         " https://streamable.com/9gu9ew ",
                                         " https://streamable.com/ucpbvi ",
                                         " https://streamable.com/dbgt7x ",
                                         " https://streamable.com/xbb45c ",
                                         " https://streamable.com/giuohw ",
                                         " https://streamable.com/128hh2 ",
                                         " https://streamable.com/mya7d8 ",
                                         " https://streamable.com/53s4de ",
                                         " https://streamable.com/94cbv6 ",
                                         " https://streamable.com/d28ltg ",
                                         " https://streamable.com/u93igj ",
                                         " https://streamable.com/mxpa5p ",
                                         " https://streamable.com/g6np0i ",
                                         " https://streamable.com/vvehnq ",
                                         " https://streamable.com/bohpd0 ",
                                         " https://streamable.com/h3egtm ",
                                         " https://streamable.com/2xapu7 ",
                                         " https://streamable.com/o0bgz1 ",
                                         " https://streamable.com/rrutxh ",
                                         " https://streamable.com/myeaxe ",
                                         " https://streamable.com/gf6h94 ",
                                         " https://streamable.com/h17rk9 ",
                                         " https://streamable.com/12u2o7 ",
                                         " https://streamable.com/d4jk4c ",
                                         " https://streamable.com/ymlycx ",
                                         " https://streamable.com/xlbbtw ",
                                         " https://streamable.com/53vmp7 ",
                                         " https://streamable.com/aqxfeb ",
                                         " https://streamable.com/8g64th ",
                                         " https://streamable.com/ys9gfp ",
                                         " https://streamable.com/xi88w8 ",
                                         " https://streamable.com/th9mwq ",
                                         " https://streamable.com/otn7mh ",
                                         " https://streamable.com/f7xzrk ",
                                         " https://streamable.com/ema92v ",
                                         " https://streamable.com/xsjbkq ",
                                         " https://streamable.com/lbm05h ",
                                         " https://streamable.com/yt1x28 ,"]))

@bot.command()
async def coinflip(ctx):
    await ctx.channel.send(random.choice(["**heads! :coin:**","**tails! :coin:**"]))

@bot.command()
async def choose(ctx, *choices: str):
    await ctx.send(random.choice(choices))

@choose.error
async def choose_error(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        await ctx.channel.send(":warning: please input your choices and try again!")
        
@bot.command()
async def transition(ctx):
    await ctx.channel.send(random.choice(["CC flo motion",
                                          "flo motion + tile rotation",
                                          "griddler + warp zoom",
                                          "griddler",
                                          "griddler + flo motion",
                                          "warp zoom",
                                          "middle tile rotation",
                                          "hexagon spin",
                                          "skew",
                                          "time displace rotation",
                                          "timeslice",
                                          "tile scramble",
                                          "split-screen lide",
                                          "shatter",
                                          "inside cube rotation",
                                          "card wipe",
                                          "cube split",
                                          "tile rotation",
                                          "wipe rings (+turb)",
                                          "wipe blinds",
                                          "zoom w/ wave warp",
                                          "hexagon tile spin",
                                          "middle cc griddler",
                                          "circle rotation",
                                          "mirror stretch",
                                          "3D tunnel",
                                          "torn paper tranisiton",
                                          "wipe overlay",
                                          "3D flip",
                                          "3D diagonal flip",
                                          "VR reorient",
                                          "cube rotatiton",
                                          "3D thin-cube Flip",
                                          "pixel Sorter",
                                          "spin with Timeslice",
                                          "displacement Map",
                                          "luma key",
                                          "cc Split",
                                          "vortex spin",
                                          "middle tile scramble",
                                          "scale wipe",
                                          "corner spin",
                                          "cube shatter",
                                          "side tile rotation",
                                          "side hexagon tile rotation",
                                          "pop-Up",
                                          "pop-up with Timeslice",
                                          "mask Transition",
                                          "person Mask Slide",
                                          "ink Splash",
                                          "think of your own ideas lol."]))
                                          
@bot.command(pass_context=True)
async def serverinfo(ctx):
    embed = discord.Embed(name="{}'s info".format(ctx.message.guild.name), color=0x00ffff)
    embed.set_author(name="server information")
    embed.add_field(name="name", value=ctx.message.guild.name, inline=True)
    embed.add_field(name='owner', value=ctx.message.guild.owner, inline=False)
    embed.add_field(name="server id", value=ctx.message.guild.id, inline=True)
    embed.add_field(name="role coumt", value=len(ctx.message.guild.roles), inline=True)
    embed.add_field(name="member count", value=len(ctx.message.guild.members))
    embed.add_field(name="verification level", value=len(ctx.message.guild.verification_level))
    embed.add_field(name="boost amount", value=ctx.message.guild.premium_subscription_count)
    embed.set_thumbnail(url=ctx.message.guild.icon_url)
    embed.set_footer(text=f"requested by: {ctx.message.author}", icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)

@bot.command(pass_context=True)
async def boostinfo(ctx):
    embed = discord.Embed(name="{}'s boosting info".format(ctx.message.guild.name), color=0xffff00)
    embed.set_author(name=f"stats: {ctx.message.guild.name}")
    embed.add_field(name="total boosts", value=ctx.message.guild.premium_subscription_count)
    embed.add_field(name="server boost level", value=ctx.message.guild.premium_tier)
    embed.set_thumbnail(url="https://discordemoji.com/assets/emoji/7485_server_boost.png")
    embed.set_footer(text=f"requested by: {ctx.message.author}", icon_url=ctx.author.avatar_url)
    await ctx.channel.send(embed=embed)

@bot.command()
async def botinfo(ctx):
    embed = discord.Embed(name="bot info", color=0x7289da)
    embed.set_author(name="gtx | info")
    embed.add_field(name="bot version", value="BETA v0.07", inline=True)
    embed.add_field(name="developed by", value="kareem#0007", inline=True)
    embed.add_field(name="discord.py version", value="unknown", inline=True)
    embed.add_field(name="prefix", value="gtx", inline=True)
    embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/764908896259145759/764973785228247070/wp4733405.jpg")
    embed.set_footer(text="made with discord.py | Made with <3 for Chroma", icon_url="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1024px-Python-logo-notext.svg.png")
    await ctx.channel.send(embed=embed)

@bot.command()
async def help(ctx):
    await ctx.send("in work")

bot.run("put ur token here")
