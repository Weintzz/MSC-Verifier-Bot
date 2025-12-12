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

        # One time only welcome message

        """guild = self.get_guild(int(os.getenv("GUILD_ID")))  # Fetch the guild object
            channel = guild.get_channel(int(os.getenv("VERIFY_CHANNEL_ID")))
            await channel.send("🚀 Welcome, please use /verify to verify your membership. 🚀")"""

        try:
            synced = await self.tree.sync(guild=GUILD_ID)
            print(f'Synced {len(synced)} command(s)') #confirmation lang na nag sync ung commands sa server
        except Exception as e:
            print(e)


intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix="!", intents=discord.Intents.all()) #required talaga ung command prefix para gumana ung slash commands

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    VERIFY_CHANNEL_ID = int(os.getenv("VERIFY_CHANNEL_ID"))

    if message.channel.id == VERIFY_CHANNEL_ID:
        # Check if the message is not a valid slash command
        if not message.content == "/verify":
            await message.delete()  # delete spam or any other message except valid slash commands

    await client.process_commands(message)  # Para gumana pa ung ibang commands


@client.tree.command(name="verify", description="verifies your membership", guild=GUILD_ID) #initializes the slash command 'verify'
async def verifyMember(interaction: discord.Interaction, msc_id: str, student_number: str, email: str): #ginagawa nyang required maglagay ng parameters sa slash command

    conn = sqlconnector.initialize()
    exists = sqlconnector.check_multiple(conn, msc_id, username)
    username = interaction.user

    if sqlconnector.verify(conn, msc_id, student_number, email) and not exists:
        sqlconnector.add_user(conn, msc_id, student_number, username)
        
        member = interaction.guild.get_member(interaction.user.id)
        logs_channel = interaction.guild.get_channel(int(os.getenv("LOGS_CHANNEL_ID")))
        
        await interaction.response.send_message("You are now verified!", ephemeral=True)   

        await logs_channel.send(
            f"{interaction.user.mention} has been verified\n"
            f"MSC ID: {msc_id}\n"
            f"Student Number: {student_number}\n"
            f"Email: {email}")
        

        ROLE_ID = int(os.getenv("VERIFIED_ROLE_ID")) #.env variable for Member Role
        UNVERIFIED_ROLE_ID = int(os.getenv("UNVERIFIED_ROLE_ID")) #.env variable for Unverified Role

        add_role = interaction.guild.get_role(ROLE_ID)
        remove_role = interaction.guild.get_role(UNVERIFIED_ROLE_ID) #gets both roles' ID
        await member.remove_roles(remove_role) #adds Member role and removes Unverified role
        await member.add_roles(add_role)


    elif exists == 3:
        await interaction.response.send_message("You are already verified", ephemeral=True)
    elif exists == 2:
        await interaction.response.send_message("MSC ID is already verified with different discord account. Use /update to change your information", ephemeral=True)
    elif exists == 1:
        await interaction.response.send_message("Discord account is already verified with different MSC ID. Use /update to change your information", ephemeral=True)
    else:
        await interaction.response.send_message("Verification failed, credentials are not found in the system.", ephemeral=True)
    

client.run(os.getenv('BOT_TOKEN'))