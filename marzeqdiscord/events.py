from discord.ext.commands import Bot

class Events:
    @staticmethod
    def on_nitro_event(event):
        def wrapper(client: Bot):
            @client.event
            async def on_member_update(before, after):
                if before.premium_since is None and after.premium_since is not None:
                    await event(after)
        return wrapper
