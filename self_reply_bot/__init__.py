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
        "timestamp": (snowflake >> 22) + 1420070400000,
        "iw": (snowflake & 0x3E0000) >> 17,
        "ip": (snowflake & 0x1F000) >> 12,
        "incr": snowflake & 0xFFF,
    }


worker_id_bits = 5
data_center_id_bits = 5
max_worker_id = -1 ^ (-1 << worker_id_bits)
max_data_center_id = -1 ^ (-1 << data_center_id_bits)
sequence_bits = 12
worker_id_shift = sequence_bits
data_center_id_shift = sequence_bits + worker_id_bits
timestamp_left_shift = sequence_bits + worker_id_bits + data_center_id_bits
sequence_mask = -1 ^ (-1 << sequence_bits)


def dict_to_snowflake(snowflake):
    return (
        (abs(snowflake["timestamp"] - 1420070400000) << timestamp_left_shift)
        | abs(snowflake["iw"]) << data_center_id_shift
        | abs(snowflake["ip"]) << worker_id_shift
        | abs(snowflake["incr"])
    )


@bot.command()
async def run(ctx: commands.Context):
    l1 = await ctx.send(
        content="test test test",
    )
    l2 = await ctx.send(
        content="test test test",
    )
    for i in range(0, 300):
        od = snowflake_to_dict(l1.id)
        nd = snowflake_to_dict(l2.id)
        diff = {
            "timestamp": nd["timestamp"] - od["timestamp"],
            "iw": nd["iw"] - od["iw"],
            "ip": nd["ip"] - od["ip"],
            "incr": nd["incr"] - od["incr"],
        }
        print("l1/l2: " + str(diff))
        pd = {
            "timestamp": nd["timestamp"] + diff["timestamp"],
            "iw": 2,
            "ip": nd["ip"] + diff["ip"],
            "incr": nd["incr"] + diff["incr"],
        }
        print("l2: " + str(snowflake_to_dict(l2.id)))
        print("pd: " + str(pd))
        pred_id = dict_to_snowflake(pd)
        l1 = l2
        l2 = await ctx.send(
            content=f"https://discord.com/channels/{ctx.guild.id}/{ctx.channel.id}/{pred_id}"
        )
        if l2.id == pred_id:
            l2 = await ctx.send(
                reference=discord.MessageReference(
                    message_id=ctx.message.id, channel_id=ctx.channel.id
                ),
                content="IT WORKS THE PREVIOUS UNEDITED MESSAGE LINKS TO ITSELF",
            )
            break
        else:
            nd = snowflake_to_dict(l2.id)
            od = snowflake_to_dict(pred_id)
            print(l2.id)
            print(pred_id)
            print(
                "l2/pred: "
                + str(
                    {
                        "timestamp": nd["timestamp"] - od["timestamp"],
                        "iw": nd["iw"] - od["iw"],
                        "ip": nd["ip"] - od["ip"],
                        "incr": nd["incr"] - od["incr"],
                    }
                )
            )


bot.run(os.getenv("TOKEN"))
