#!/usr/bin/env python3
import discord
import textwrap
import random
import string
from os import listdir, remove
from os.path import isfile
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

fontsize = 100
fnt = ImageFont.truetype("/usr/share/fonts/gnu-free/FreeMono.otf", fontsize)


class MyClient(discord.Client):

	async def on_ready(self):
		self.files = sorted([f[:-4] for f in listdir(None)
							 if isfile(f) and f.endswith(".png")])
		print("Logged in and ready")

	async def on_message(self, message: discord.Message):
		if message.author == self.user:
			return

		if message.clean_content == "wojaks?":
			s = "```\n"
			for f in self.files:
				s += f + "\n"
			s += "```"
			await message.channel.send(s)
			return

		if not message.clean_content.startswith(">"):
			return
		wojak = message.clean_content[1:]
		if wojak not in self.files:
			await message.channel.send("Wojak not found")
			return

		text = ""
		replied = None
		if message.reference is None:
			async for msg in message.channel.history(limit=10):
				if msg == message:
					continue
				elif msg.author != self.user and msg.content != "":
					text = msg.clean_content
					break
		else:
			replied = await message.channel.fetch_message(message.reference.message_id)
			text = replied.clean_content

		img = Image.open(wojak + ".png")
		draw = ImageDraw.Draw(img)

		lines = textwrap.wrap(text, width=img.width / 1.5 / fontsize)
		offset = 0
		toffset = len(lines) * fontsize / 2
		for line in lines:
			w, _ = draw.textsize(line, font=fnt)
			draw.text((img.width * 0.69 - w / 2, img.height / 2 - toffset + offset), line, 0, font=fnt)
			offset += fontsize

		filename = "/tmp/" + \
			''.join(random.choices(string.ascii_uppercase + string.digits, k=16)) + ".png"
		img.save(filename)
		f = open(filename, "rb")
		if replied is None:
			await message.channel.send(file=discord.File(f, filename=wojak + ".png"))
		else:
			await message.channel.send(file=discord.File(f, filename=wojak + ".png"), reference=replied)
		await message.delete()
		f.close()
		remove(filename)


client = MyClient()

f = open("token", "r")
token = f.read()
f.close()
client.run(token)
