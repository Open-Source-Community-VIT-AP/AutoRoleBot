import discord
from discord.ext import commands
import csv
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents().all()  # Allowing  the bot to access all the information
bot = commands.Bot(command_prefix="==", intents=intents)


@bot.event
async def on_ready():  # Sends the bot is ready message in the console when it is done booting up
    await bot.change_presence(
        status=discord.Status.dnd,
        activity=discord.Activity(
            type=discord.ActivityType.watching, name="you sleep."
        ),
    )
    print("Bot is ready!")


def member_list(ctx):
    memberlist = []  # Refreshes member list everytime command is run
    member_dictionary = {}  # Member and member id key value pair
    server_instance = ctx.message.guild.members  # Makes a server instance
    for member in server_instance:
        memberlist.append(
            member.name + "#" + member.discriminator
        )  # Appends the discord tag in the desired format
        member_dictionary[
            member.name + "#" + member.discriminator
        ] = member.id  # Makes the key value pair
    return memberlist, member_dictionary


def make_dictionary():
    csvFile = "data/participants.csv"
    dictionary = {}
    with open(csvFile, encoding="utf-8") as f:
        csvReader = list(csv.DictReader(f))
        for rows in csvReader:
            team = "team " + str(rows["grp_id"])
            for i in range(1, 5):
                if rows[f"member_{i}"] != "":
                    dictionary[rows[f"member_{i}"]] = team
    return dictionary


@bot.command(name="roles", pass_context=True)
@commands.has_role("Server Admin")  # Making sure only admin can run the command
async def assign_all(ctx):
    async with ctx.typing():  # Typing animation
        memberlist, member_dictionary = member_list(ctx)  # Getting the the information
        dictionary = make_dictionary()
        for member in memberlist:
            if member in dictionary:
                user = ctx.author.guild.get_member(
                    member_dictionary[member]
                )  # Retrieves a discord.Member object
                role = discord.utils.get(
                    ctx.author.guild.roles, name=dictionary[member]
                )  # Retrieves the required role
                await user.add_roles(role)  # Assigns the role
    await ctx.send("Done!")


if __name__ == "__main__":
    bot.run(TOKEN)
