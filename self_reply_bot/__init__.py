__version__ = "0.1.0"
import discord
import os
from discord.ext import commands

bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


def snowflake_to_dict(snowflake):
    return {
        "timestamp": (snowflake >> 22),
        "iw": (snowflake & 0x3E0000) >> 17,
        "ip": (snowflake & 0x1F000) >> 12,
        "incr": snowflake & 0xFFF,
    }


def dict_to_snowflake(snowflake):
    return (
        snowflake["timestamp"] << 22
        | snowflake["iw"] << 17
        | snowflake["ip"] << 12
        | snowflake["incr"]
    )


@bot.command()
async def run(ctx: commands.Context):
    l1 = await ctx.send(
        reference=discord.MessageReference(
            message_id=ctx.message.id, channel_id=ctx.channel.id
        ),
        content="test test test",
    )
    l2 = await ctx.send(
        reference=discord.MessageReference(
            message_id=ctx.message.id, channel_id=ctx.channel.id
        ),
        content="test test test",
    )
    od = snowflake_to_dict(l1.id)
    nd = snowflake_to_dict(l2.id)
    print(l1.id)
    print(dict_to_snowflake(od))
    print(l1.id == dict_to_snowflake(od))
    diff = {
        "timestamp": nd["timestamp"] - od["timestamp"],
        "iw": nd["iw"] - od["iw"],
        "ip": nd["ip"] - od["ip"],
        "incr": nd["incr"] - od["incr"],
    }
    print(diff)


bot.run(os.getenv("TOKEN"))
