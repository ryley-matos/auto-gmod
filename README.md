# auto-gmod
### Collection of scripts and docker containers for running and managing a garry's mod server.
## Setup
### Enviroment
Create a .env with the following variables: `STEAM_AUTH_KEY (required to host collection)` and `STEAM_COLLECTION (id of the steam collection to host)`

You can verify you've done this correctly by running `source .env && docker-compose build && docker-compose up` and attempting to connect to the server through the client. Server startup is about 5 minutes once the image is built and running. Looking into how to cut this time down.

### Server Helper
Its recommended to setup a virtualenv to install dependencies
```
python3 -m venv ./venv
. ./venv/bin/activate
```
Then install dependencies `pip install -r requirements.txt`
#### server_helper.generate_workshop_script
- Requires .env vars `STEAM_COLLECTION`
- Uses playwright to collect a list of workshop items in a collection and outputs `workshop.lua (script used by gmod to force client downloads)` 
- Can be run standalone by running the command below
```
python -c 'import asyncio; import server_helper; asyncio.run(server_helper.generate_workshop_script())'
```
#### server_helper.add_to_collection
❗❗❗Important❗❗❗ This function requires your steam username and password. It is highly recommended not to use this function unless you perform an audit of the code yourself. Furthermore, this functionality will not work with steam guard enabled, so it is also recommended to create a **SEPERATE STEAM ACCOUNT** and host your workshop collection there.
- Requires .env vars `STEAM_USERNAME` and `STEAM_PASSWORD`
- Uses playwright to add a specific workshop item by id to a collection. Mainly used in conjuction with generate_workshop_script
- Can be run standalone by running the command below
```
python -c 'import asyncio; import server_helper; asyncio.run(server_helper.add_to_collection({steam workshop id here})'
```
#### Discord bot
- Requires .env vars `DISCORD_TOKEN`
- Commands
  - !start_server
  - !restart_server
  - !add_mod {steam workshop id}
- Can be run with the command below
```
python server_helper.py
```
