import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from flask import Flask 
from threading import Thread
import logging
import datetime

logging.basicConfig(level=logging.INFO)
load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True

app = Flask('')

@app.route('/')
def home():
    return "✅ Bot is running."

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"<a:Verify:1382696460696555630> Logged in as {bot.user}")

OLD_ROLE_ID = 1382389547664539740  # Old role to be removed

# Verify command for boys
@bot.command(name="vb")
@commands.has_permissions(manage_roles=True)
async def verify_boy(ctx, member_id: int):
    member = ctx.guild.get_member(member_id)
    if not member:
        await ctx.send("❌ Member not found.")
        return

    role = ctx.guild.get_role(1382389524524564521)  # Verified role for boys (change to your role ID)
    if not role:
        await ctx.send("❌ Verified role not found.")
        return

    old_role = ctx.guild.get_role(OLD_ROLE_ID)
    if old_role in member.roles:
        await member.remove_roles(old_role)

    await member.add_roles(role)

    dm_embed = discord.Embed(
        title=f"<a:Verify:1382696460696555630> Verified in 🥂 {ctx.guild.name}",
        description=f"✅ You have been **Verified** in the server 🥂 **{ctx.guild.name}**.",
        color=0x2ecc71
    )
    dm_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty)
    try:
        await member.send(embed=dm_embed)
    except discord.HTTPException:
        await ctx.send("⚠️ I couldn't send a DM to this user.")

    log_embed = discord.Embed(
        title="🟢 Successfully Verified (Boy)",
        color=0xa365c2,
        timestamp=ctx.message.created_at
    )
    log_embed.add_field(name="👤 Member Details:", value=member.mention, inline=True)
    log_embed.add_field(name="🧑‍💻 Verified By:", value=f"{ctx.author.mention} / {ctx.author.id}", inline=True)
    log_embed.add_field(name="📅 Server Join Time:", value=discord.utils.format_dt(member.joined_at, style='R') if member.joined_at else "Unknown", inline=True)
    log_embed.add_field(name="🕒 Verification Time:", value=discord.utils.format_dt(datetime.datetime.utcnow(), style='R'), inline=True)
    log_embed.add_field(name="📋 User Information:", value="Unspecified Info", inline=True)
    log_embed.add_field(name="🔗 Command Used In:", value=f"{ctx.channel.mention} `• {ctx.command}`", inline=False)
    log_embed.set_footer(text=f"Verified By : {ctx.author.name} • {ctx.message.created_at.strftime('%m/%d/%Y %I:%M %p')}")
    log_embed.set_thumbnail(url=member.display_avatar.url)

    logs_channel = bot.get_channel(1382389657878134878)  # Logs channel
    if logs_channel:
        await logs_channel.send(embed=log_embed)

    await ctx.send(f"<a:Verify:1382696460696555630> {member.mention} has been verified and given the role.")

# Verify command for girls
@bot.command(name="vg")
@commands.has_permissions(manage_roles=True)
async def verify_girl(ctx, member_id: int):
    member = ctx.guild.get_member(member_id)
    if not member:
        await ctx.send("❌ Member not found.")
        return

    female_role = ctx.guild.get_role(1382389520661614614)  # Verified Female role
    verified_role = ctx.guild.get_role(1382389524524564521)  # General Verified role
    if not female_role or not verified_role:
        await ctx.send("❌ One or more roles not found.")
        return

    old_role = ctx.guild.get_role(OLD_ROLE_ID)
    if old_role in member.roles:
        await member.remove_roles(old_role)

    await member.add_roles(verified_role, female_role)

    dm_embed = discord.Embed(
        title=f"<a:Verify:1382696460696555630> Verified in 🥂 {ctx.guild.name}",
        description=f"✅ You have been **Verified** in the server 🥂 **{ctx.guild.name}**.",
        color=0xe91e63  # Pink color
    )
    dm_embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else discord.Embed.Empty)
    try:
        await member.send(embed=dm_embed)
    except discord.HTTPException:
        await ctx.send("⚠️ I couldn't send a DM to this user.")

    log_embed = discord.Embed(
        title="🟣 Successfully Verified (Girl)",
        color=0xe91e63,
        timestamp=ctx.message.created_at
    )
    log_embed.add_field(name="👤 Member Details:", value=member.mention, inline=True)
    log_embed.add_field(name="🧑‍💻 Verified By:", value=f"{ctx.author.mention} / {ctx.author.id}", inline=True)
    log_embed.add_field(name="📅 Server Join Time:", value=discord.utils.format_dt(member.joined_at, style='R') if member.joined_at else "Unknown", inline=True)
    log_embed.add_field(name="🕒 Verification Time:", value=discord.utils.format_dt(datetime.datetime.utcnow(), style='R'), inline=True)
    log_embed.add_field(name="📋 User Information:", value="Unspecified Info", inline=True)
    log_embed.add_field(name="🔗 Command Used In:", value=f"{ctx.channel.mention} `• {ctx.command}`", inline=False)
    log_embed.set_footer(text=f"Verified By : {ctx.author.name} • {ctx.message.created_at.strftime('%m/%d/%Y %I:%M %p')}")
    log_embed.set_thumbnail(url=member.display_avatar.url)

    logs_channel = bot.get_channel(1382389657878134878)
    if logs_channel:
        await logs_channel.send(embed=log_embed)

    await ctx.send(f"<a:Verify:1382696460696555630> {member.mention} has been verified (girl) and given the roles.")


# Clear messages command
@bot.command(name="clear")
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    deleted = await ctx.channel.purge(limit=amount)
    await ctx.send(f"<a:Verify:1382696460696555630> Deleted {len(deleted)} messages.", delete_after=5)

# Copy roles command
@bot.command(name="copyroles")
@commands.has_permissions(manage_roles=True)
async def copyroles(ctx, member: discord.Member, target: discord.Member):
    roles_to_copy = [role for role in member.roles if role != ctx.guild.default_role]
    try:
        await target.add_roles(*roles_to_copy)
        await ctx.send(f"<a:Verify:1382696460696555630> Roles from {member.mention} copied to {target.mention}.")
    except discord.Forbidden:
        await ctx.send("❌ I don't have enough permissions to add roles.")
    except Exception as e:
        await ctx.send(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    keep_alive()
    try:
        bot.run(os.getenv("BOT_TOKEN"))
    except Exception as e:
        print(f"❌ Bot failed to run: {e}")
