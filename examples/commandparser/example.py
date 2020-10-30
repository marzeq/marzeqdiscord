from marzeqdiscord import commandparser
from discord.ext.commands import Bot
import discord
from typing import List

client = Bot(command_prefix="YOUR DESIRED COMMAND PREFIX")


cmdparser = commandparser.CommandParser()


@client.event
async def on_ready():
    print("Working")


@cmdparser.command
async def example_command(message: discord.Message,
                          args: List[commandparser.Arg],
                          params: List[commandparser.Param],
                          flags: List[commandparser.Flag],
                          required=["aaa", "askhfd"]):
    strargs = []
    strparams = []
    strflags = []
    for arg in args:
        strargs.append(arg.value)
    for param in params:
        strparams.append(param.dict)
    for flag in flags:
        strflags.append(flag.value)

    await message.channel.send(f"Args: {strargs}, Params: {strparams}, Flags: {strflags}")


example_command(client)


client.run("YOUR BOT TOKEN")
