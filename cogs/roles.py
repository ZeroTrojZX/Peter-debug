import discord
from discord.ext import commands
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from utils.variables import admin
from utils.functions import parse_color
import pymongo
from pymongo.errors import PyMongoError

load_dotenv()
mongo = MongoClient(os.getenv("MONGODB_URL"))
main_db = mongo["AAT"]
roles_db = main_db["roles"]

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group()
    async def custom(self, ctx: commands.Context):
        return

    @custom.command(name="register", description="Registers a custom role to a user")
    async def register(self, ctx: commands.Context, role: discord.Role, member: discord.Member):
        if any(r.id in admin for r in ctx.author.roles):
            try:
                roles_db.insert_one({"user_id": member.id, "role_id": role.id})
                embed = discord.Embed(title="<:Check:1490727471761457335> Registered", description=f"{role.mention} has been registered for {member.mention}", color=discord.Color.green())
                await ctx.send(embed=embed)
            except PyMongoError as exc:
                embed = discord.Embed(title="<:Cross:1490727525356278064> Failed to Register", description=f"I have recieved an error. (`{exec}`)", color=discord.Color.red())
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="<:Cross:1490727525356278064> Lack of Permissions", description=f"You do not have permisson to execute this command.", color=discord.Color.red())
            await ctx.send(embed=embed, ephemeral=True)
    
    @custom.command(name="create", description="Creates a custom role")
    async def create(self, ctx: commands.Context, name: str):
        if ctx.author.premium_since is None and not ctx.author.guild_permissions.administrator:
            embed = discord.Embed(title="<:Cross:1490727525356278064> Not Allowed", description=f"You are not allowed to create a custom role as you are not a server booster.", color=discord.Color.red())
            await ctx.send(embed=embed, ephemeral=True) 
            return
        info = roles_db.find_one({"user_id": ctx.author.id})
        if info:
            embed = discord.Embed(title="<:Cross:1490727525356278064> Role Limit", description=f"You are only allowed to have 1 custom role at this time.", color=discord.Color.red())
            await ctx.send(embed=embed, ephemeral=True)
            return
        
        role = await ctx.guild.create_role(name=name)
        positions = {role: 154}
        await ctx.guild.edit_role_positions(positions)
        await ctx.author.add_roles(role)
        roles_db.insert_one({"user_id": ctx.author.id, "role_id": role.id})
        embed = discord.Embed(title="<:Check:1490727471761457335> Role Created", description=f"I have succesfully created {role.mention}", color=discord.Color.green())
        await ctx.send(embed=embed, ephemeral=True)


    @custom.command(name="color", description="Modifys the color of a custom role")          
    async def color(self, ctx: commands.Context, color: str):
        info = roles_db.find_one({"user_id": ctx.author.id})
        if info:
            try:
                role_color =  parse_color(color)
            except:
                await ctx.send("Invalid hex code.")
                return
            role_id = int(info["role_id"])
            role = ctx.guild.get_role(role_id)
            if role is None:
                await ctx.send('couldnt fetch role')
                return
            await role.edit(color=role_color)
            embed = discord.Embed(title="<:Check:1490727471761457335> Color Changed", description=f"Succesfully changed role color to `{color}`", color=discord.Color.green())
            await ctx.send(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(title="<:Cross:1490727525356278064> No Role", description=f"You do not currently have any custom role registered.", color=discord.Color.red())
            await ctx.send(embed=embed, ephemeral=True)

    @custom.command(name="name", description="Modifys the name of a custom role")          
    async def name(self, ctx: commands.Context, name: str):
        info = roles_db.find_one({"user_id": ctx.author.id})
        if info:
            role_id = int(info["role_id"])
            role = ctx.guild.get_role(role_id)
            if role is None:
                await ctx.send('couldnt fetch role')   
                return
            await role.edit(name=name)
            embed = discord.Embed(title="<:Check:1490727471761457335> Name Changed", description=f"Succesfully changed role name to `{name}`", color=discord.Color.green())
            await ctx.send(embed=embed, ephemeral=True)     
        else:
            embed = discord.Embed(title="<:Cross:1490727525356278064> No Role Found", description=f"You do not currently have any custom role registered.", color=discord.Color.red())
            await ctx.send(embed=embed, ephemeral=True)
    
    @custom.command(name="icon", description="Modifys the icon of a custom role")
    async def icon(self, ctx: commands.Context, icon: discord.Attachment):
        info = roles_db.find_one({"user_id": ctx.author.id})
        if info:
            role_id = int(info["role_id"])
            role = ctx.guild.get_role(role_id)
            if role is None:
                await ctx.send('couldnt fetch role')   
                return            
            image_bytes = await icon.read()
            if not icon.content_type or not icon.content_type.startswith("image/"):
                await ctx.send("❌ Please upload a valid image file.", ephemeral=True)
                return
            await role.edit(display_icon=image_bytes)
            embed = discord.Embed(title="<:Check:1490727471761457335> Icon Changed", description=f"Succesfully changed role icon.", color=discord.Color.green())
            embed.set_thumbnail(url=icon.url)
            await ctx.send(embed=embed, ephemeral=True)     
        else:
            embed = discord.Embed(title="<:Cross:1490727525356278064> No Role Found", description=f"You do not currently have any custom role registered.", color=discord.Color.red())
            await ctx.send(embed=embed, ephemeral=True)                     



async def setup(bot):
    await bot.add_cog(Roles(bot))