from discord.ext.commands import Bot
import inspect


class CommandParser:

    @staticmethod
    def command(command):
        def wrapper(client: Bot):

            @client.event
            async def on_message(message):
                invoke_command = client.command_prefix + command.__name__

                if message.content.startswith(client.command_prefix + command.__name__):
                    content = message.content[len(invoke_command) + 1:]
                    bare_args = content.split(" ")
                    flags = []
                    params = []
                    args = []

                    for pos in range(len(bare_args)):
                        if bare_args[pos].startswith("--"):
                            flags.append(Flag(bare_args[pos]))
                        elif bare_args[pos].startswith("-"):
                            params.append(Param(bare_args[pos], bare_args[pos + 1])) if pos < len(bare_args) - 1 else lambda: None
                            pos += 1
                        else:
                            args.append(Arg(bare_args[pos]))

                    await command(message, args, params, flags)

        return wrapper


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
