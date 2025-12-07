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
            print(f'Synced {len(synced)} command(s)') #confirmation lang na nag sync ung commands sa server
        except Exception as e:
            print(e)


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=discord.Intents.all()) #required talaga ung command prefix para gumana ung slash commands

@client.tree.command(name="verify", description="verifies your membership", guild=GUILD_ID) #initializes the slash command 'verify'
async def verifyMember(interaction: discord.Interaction, msc_id: str, student_number: str, email: str): #ginagawa nyang required maglagay ng parameters sa slash command
    if not msc_id.startswith("MSC"):
        await interaction.response.send_message(f"Your MSC ID: {msc_id} is invalid.", ephemeral=True)
        return
    if len(student_number) != 10 or not student_number.isnumeric():
        print(len(student_number))
        await interaction.response.send_message(f"Your Student Number {student_number} is invalid.", ephemeral=True)
        return
    if "@" not in email or ".com" not in email:
        await interaction.response.send_message(f"Your email {email} is invalid.", ephemeral=True)
        return

    await interaction.response.send_message(f"Confirm: \nMSC ID: {msc_id}\nStudent Number: {student_number}\nEmail: {email}",
    ephemeral=True) #ephemeral = True, ibigsabihin sarili lang makakakita


client.run(os.getenv('BOT_TOKEN'))