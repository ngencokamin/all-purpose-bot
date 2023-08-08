# All Purpose Bot

### A discord bot that does all the thing!*

*definition of all may vary

## Setup

- Clone this source code into a working directory

- Install the requirements using pip:

  ```sh
  make install
  # This will install all the required packages and libraries for using the Bot
  ```

- Set up the local development environment using the following command:

    ```sh
    make setup
    # Builds database and creates .env file
    ```

## Wipe DB

- To wipe the DB, run the following command:
  ```sh
  make wipe-db
  # Note: You will need to run make setup again or the bot will not function correctly
  ```


## Plugins

### Admin

Manage plugins on a per server basis

##### Usage:

`!enable <plugin>`: enables a plugin for the current server

`!disable <plugin>`: disables a plugin for the current server

`!list-plugins`: returns a list of all plugins and their basic functionality

`!sync`: universally sync slash commands to apply new changes

### Debugging

Manage plugins for all instances

##### Usage:

`!reload <plugin>`: reload plugin universally to apply new code changes to running bot

`!load <plugin>`: load disabled/new plugin for running bot

`!unload <plugin>`: universally disable plugin

### Callbacks

Trigger automatic responses to key phrases in messages (supports gif links as responses)

##### Usage:

`/!callback add <trigger> <response>`: takes in what phrase should trigger a callback and what the bot should respond with

`/callback remove <trigger>`: removes the specified callback

`/callback disable <channel name>`: blacklist a channel so callback responses do not fire

`/callback enable <channel name>`: re-enable callbacks in a blacklisted channel

`/list`: returns a list of all existing callbacks and blacklisted channels

### Movie Night

Search for movies on imdb and output info in embeds, add movies with info from imdb to a movie night queue, pick a random movie from the queue to watch

##### Usage:

`/movies search <title>`: search imdb for a movie by title and return a discord embed with movie info

`/movies add <title>`: add movie to the queue with data from imdb (each user can add one at a time)

`/movies remove`: removes the user's current movie selection from the queue

`/movies list`: list movies in queue and which user added them

`/movies pick`: pick a random movie from the queue and return a discord embed with movie info