from sqlitedict import SqliteDict as DB
import os

def build_plugins(servers):
    plugins_table = DB('db/db.sqlite', tablename='plugins', autocommit=True)
    if servers:
        plugins = []
        for filename in os.listdir("./plugins"):
            print(filename)
            if filename.endswith(".py"):
                # cut off the .py from the file name
                plugins.append(filename[:-3])
                print(filename)
        for server in servers:
            server_plugins = {}
            for plugin in plugins:
                 server_plugins[plugin] = True
            plugins_table[server.id] = server_plugins
    plugins_table.close()

def build_callbacks(servers):
    callbacks_table = DB('db/db.sqlite', tablename='callbacks', autocommit=True)
    if servers:
        for server in servers:
            callbacks_table[server.id] = {}
    callbacks_table.close()

def build_movies(servers):
    movies_table = DB('db/db.sqlite', tablename='movies', autocommit=True)
    if servers:
        for server in servers:
            movies_table[server.id] = {}
    movies_table.close()

def build_all(servers=None):
    build_plugins(servers)
    build_callbacks(servers)
    build_movies(servers)

if __name__ == "__main__":
    build_all(servers=None)