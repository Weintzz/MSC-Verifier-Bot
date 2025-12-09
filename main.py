import sqlconnector
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
    
   

    conn = sqlconnector.initialize()
    if sqlconnector.verify(conn, msc_id, student_number, email):
        await interaction.response.send_message("You are now verified!", ephemeral=True)
        member = interaction.guild.get_member(interaction.user.id)
        ROLE_ID = int(os.getenv("ROLE_ID")) #sa gatekeep lang tong role id na to
        role = interaction.guild.get_role(ROLE_ID)
        await member.add_roles(role)
    else:
        await interaction.response.send_message("Verification failed. Wrong Credentials.", ephemeral=True)
    

client.run(os.getenv('BOT_TOKEN'))