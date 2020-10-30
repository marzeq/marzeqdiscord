from discord.ext.commands import Bot
import discord
import inspect


def get_default_args(func):
    signature = inspect.signature(func)
    return str(signature)[str(signature).find("required"):][10:-2].replace("'", "").split(", ")


class CommandParser:
    @staticmethod
    def command(command):
        required = get_default_args(command)

        def wrapper(client: Bot):

            @client.event
            async def on_message(message: discord.Message):
                invoke_command = client.command_prefix + command.__name__

                if message.content.startswith(client.command_prefix + command.__name__):
                    content = message.content[len(invoke_command) + 1:]
                    bare_args = content.split(" ")
                    flags = []
                    params = []
                    args = []

                    skip = False
                    for pos in range(len(bare_args)):
                        if skip:
                            skip = False
                            continue
                        if bare_args[pos].startswith("--"):
                            flags.append(Flag(bare_args[pos]))
                        elif bare_args[pos].startswith("-"):
                            params.append(Param(bare_args[pos], bare_args[pos + 1]))\
                                if pos < len(bare_args) - 1 and not bare_args[pos + 1].startswith("-") else lambda: None
                            skip = True
                        else:
                            args.append(Arg(bare_args[pos]))
                    args = [] if args[0].value == "" else args

                    if len(required[len(args):]) > 0:
                        raise discord.ext.commands.MissingRequiredArgument(FailRequired(required[0]))

                    await command(message, args, params, flags)

        return wrapper


class FailRequired:
    def __init__(self, missing: str):
        self.missing = missing

    @property
    def name(self):
        return self.missing


class Arg:
    def __init__(self, value):
        self.value = value


class Param:
    def __init__(self, param_name, param_value):
        self.param_name = param_name
        self.param_value = param_value

    @property
    def dict(self):
        return {self.param_name: self.param_value}


class Flag(Arg):
    pass
