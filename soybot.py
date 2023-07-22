#!/usr/bin/env python3

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.	If not, see <https://www.gnu.org/licenses/>.

import discord
import textwrap
import random
import string
from os import listdir, remove
from os.path import isfile
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

intents = discord.Intents.default()
intents.message_content = True

fontsize = 100
fnt = ImageFont.truetype("FreeMono.otf", fontsize)


class MyClient(discord.Client):
	async def on_ready(self):
		print("Logged in and ready")

	def getfiles(self):
		return sorted(
			[f[:-4] for f in listdir(None) if isfile(f) and f.endswith(".png")]
		)

	async def soy(self, wojak, text, message: discord.Message, ref):
		if not wojak in self.getfiles():
			return

		img = Image.open(wojak + ".png")
		draw = ImageDraw.Draw(img)

		lines = textwrap.wrap(text, width=img.width / 1.5 / fontsize)
		offset = 0
		toffset = len(lines) * fontsize / 2
		for line in lines:
			w = draw.textlength(line, font=fnt)
			draw.text(
				(img.width * 0.69 - w / 2, img.height / 2 - toffset + offset),
				line,
				0,
				font=fnt,
			)
			offset += fontsize

		filename = (
			"/tmp/"
			+ "".join(random.choices(string.ascii_uppercase + string.digits, k=16))
			+ ".png"
		)
		img.save(filename)
		f = open(filename, "rb")

		if ref is None:
			await message.channel.send(file=discord.File(f, filename=wojak + ".png"))
		else:
			await message.channel.send(
				file=discord.File(f, filename=wojak + ".png"), reference=ref
			)
			f.close()
			remove(filename)

	async def on_message(self, message: discord.Message):
		if message.author == self.user:
			return

		if message.clean_content == ">?":
			s = "```\n"
			for f in self.getfiles():
				s += f + "\n"
			s += "```"
			await message.channel.send(s)
			return

		if not message.content.startswith(">"):
			return

		wojak = message.content[1:].split(" ")[0]

		text = ""
		replied = None

		if " " in message.content:
			text = message.clean_content[1 + len(wojak) :]
		elif message.reference is None:
			async for msg in message.channel.history(limit=10):
				if msg == message:
					continue
				elif msg.author != self.user and msg.content != "":
					text = msg.clean_content
					break
		else:
			replied = await message.channel.fetch_message(message.reference.message_id)
			text = replied.clean_content

		await self.soy(wojak, text, message, replied)


client = MyClient(intents=intents)
f = open("token", "r")
token = f.read()
f.close()
client.run(token)
