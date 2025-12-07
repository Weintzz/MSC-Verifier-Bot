import discord
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands
import os

load_dotenv()
GUILD_ID = discord.Object(id=int(os.getenv('GUILD_ID')))


class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged in as {self.user}!')
        
        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} command(s)')
        except Exception as e:
            print(e)

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        print(f'{message.author} : {message.content}')
        
        if message.content == "hello":
            await message.channel.send(f"hi")


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=discord.Intents.all())

@client.tree.command(name="verify", description="verifies your membership", guild=GUILD_ID)
async def verifyMember(interaction: discord.Interaction, msc_id: str, student_number: str, email: str):
    await interaction.response.send_message(f"Confirm: \nMSC ID: {msc_id}\nStudent Number: {student_number}\nEmail: {email}",
    ephemeral=True)


client.run(os.getenv('BOT_TOKEN'))