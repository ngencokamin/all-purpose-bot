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

### Callbacks

Trigger automatic responses to key phrases in messages (supports gif links as responses)

##### Usage:

`!callback add <trigger> <response>`: takes in what phrase should trigger a callback and what the bot should respond with

`!callback remove <trigger>`: removes the specified callback

`!callback list`: returns a list of all existing callbacks