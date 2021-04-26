import discord

class MyClient(discord.Client):
    async def on_message(self, message):
        if message.author == self.user:
            return

        if message.content == 'helo':
            await message.channel.send('jaj tveci lmao')

client = MyClient()
client.run('ODM2MzM3NzUyOTE5NjM4MDI3.YIciOg.6l0m_pDUMblWnlaBYbA-n-pSxP4')
