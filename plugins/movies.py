import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord import app_commands, ui
from sqlitedict import SqliteDict as DB
import random

import imdb

class Movies(commands.GroupCog, name="movies"):

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ia = imdb.Cinemagoer()
        self.db = DB('db/db.sqlite', tablename='movies')
        super().__init__()

    async def search_movie(self,title):
        movies = self.ia.search_movie(title)
        return movies[0].movieID

    async def find_movie(self,id):
        movie = self.ia.get_movie(id)
        return movie
    
    async def make_embed(self, movie):
        movie_embed  = discord.Embed(title=movie['title'])

        if 'photo_url' in movie:
            movie_embed.set_thumbnail(url=movie['photo_url'])
        else:
            movie_embed.set_thumbnail(url=movie['cover url'])
        obj_genres = movie['genres']
        if isinstance(obj_genres, str):
            genres = obj_genres
        else:
            genres = ', '.join(obj_genres)
        movie_embed.add_field(name="Genres:", value=genres, inline=True)

        if 'taglines' in movie:
            movie_embed.description = movie["taglines"][0]
        if 'directed_by' in movie:
            directed_by = movie['directed_by']
        elif 'director' in movie:
            if len(movie['director']) > 1:
                directed_by = movie['director'][0]['name']
                for director in movie['director']:
                    if directed_by == director['name']:
                        next
                    else:
                        directed_by += f', {director["name"]}'
            else:
                directed_by = movie['director'][0]['name']
            movie_embed.add_field(name="Directed By:", value=directed_by, inline=True)
        if 'plot' in movie: 
            movie_embed.add_field(name="Plot", value=movie['plot'][0])
        return movie_embed


    async def get_movie(self, title: str):
        movieID = await self.search_movie(title)
        movie = await self.find_movie(movieID)
        return movie

    async def add_movie(self,interaction,movie):
        movies = self.db[interaction.guild.id]
        user = interaction.user.id
        if user in movies:
            await interaction.followup.send('Error! You already have a movie added to the queue!')
            return

        if movie.has_key('plot'):
            plot = movie['plot']
        else:
            plot = None
        if movie.has_key('director'):
            if len(movie['director']) > 1:
                directed_by = movie['director'][0]['name']
                for director in movie['director']:
                    if directed_by == director['name']:
                        next
                    else:
                        directed_by += f', {director["name"]}'
            else:
                directed_by = movie['director'][0]['name']
        else:
            directed_by = None
        title = movie['title']
        genres = ", ".join(movie['genres'])
        photo_url = movie['cover url']
        self.ia.update(movie, info='taglines')
        movies[user] = {'plot': plot, 'directed_by': directed_by, 'genres': genres, 'title': title, 'photo_url': photo_url, "movieID": movie.movieID}
        if movie.has_key('taglines'):
            movies[user]['taglines'] = movie['taglines']
        self.db[interaction.guild.id] = movies
        self.db.commit()



    @app_commands.command(name="search", description="Search imdb for a movie by title")
    async def search(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer()
        movie = await self.get_movie(title)
        self.ia.update(movie, info='taglines')
        embed = await self.make_embed(dict(movie))
        await interaction.followup.send(embed=embed)


    @app_commands.command(name="add", description="Add movie to queue")
    async def add(self, interaction: discord.Interaction, title: str):
        await interaction.response.defer()
        movie = await self.get_movie(title)
        await self.add_movie(interaction, movie)
        movie_embed = await self.make_embed(dict(movie))
        await interaction.followup.send(f'Movie {movie["title"]} added to queue!', embed=movie_embed)

    @app_commands.command(name="remove", description="Remove your queued movie")
    async def remove(self, interaction: discord.Interaction):
        movies = self.db[interaction.guild.id]
        title = movies[interaction.user.id]['title']
        del movies[interaction.user.id]
        self.db[interaction.guild.id] = movies
        self.db.commit()
        await interaction.response.send_message(f'Movie {title} removed from queue')

    @app_commands.command(name="list", description="List movies in queue")
    async def list(self, interaction: discord.Interaction):
        await interaction.response.defer()
        movies = self.db[interaction.guild.id]
        # movies_embed = discord.Embed(title="Queued Movies")
        movie_embeds = []
        if len(movies) > 0:
            for user in movies:
                user_obj = self.bot.get_user(user)
                # movie = await self.find_movie(movies[user]['movieID'])
                movie = movies[user]
                embed = await self.make_embed(movie)
                embed.set_author(name=user_obj.name, icon_url=user_obj.avatar.url)
                movie_embeds.append(embed)
            await interaction.followup.send(embeds=movie_embeds)
        else:
            await interaction.followup.send('No movies currently in queue!')

    @app_commands.command(name="pick", description="Pick a random movie from the list for this week")
    async def pick(self, interaction: discord.Interaction):
        await interaction.response.defer()
        movies = self.db[interaction.guild.id]
        user = random.choice(list(movies))
        movie = movies[user]
        del movies[user]
        embed = await self.make_embed(movie)
        self.db[interaction.guild.id] = movies
        self.db.commit()
        await interaction.followup.send(f"This weeks's movie is {movie['title']}, chosen by <@{user}>",embed=embed)



    @search.error
    @add.error
    @remove.error
    @list.error
    @pick.error
    async def movie_error(self, interaction, error):
        await interaction.response.send_message(f'Error {error}', ephemeral=True)

async def setup(bot):
    await bot.add_cog(Movies(bot))