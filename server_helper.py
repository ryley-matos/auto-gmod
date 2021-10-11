import docker
import os
import time
import discord
from dotenv import load_dotenv
import asyncio
from playwright.async_api import async_playwright

load_dotenv()

config = {
    'LUA_TEMPLATE_PATH': 'lua_template.lua',
    'LUA_OUTPUT_PATH': 'workshop.lua',
    'GET_WORKSHOP_ARRAY_PATH': 'get_workshop_array.js',
    'STEAM_COLLECTION_URL': f'https://steamcommunity.com/sharedfiles/filedetails/?id={os.environ["STEAM_COLLECTION"]}',
    **os.environ
}

f = open(config['GET_WORKSHOP_ARRAY_PATH'], 'r')
GET_WORKSHOP_ARRAY = f.read()
f.close()

f = open(config['LUA_TEMPLATE_PATH'], 'r')
LUA_TEMPLATE = f.read()
f.close()

docker_client = docker.from_env()
PORTS = {
    "27015/tcp": '27015',
    '27015/udp': '27015'
}

discord_client = discord.Client()

running_container = None

async def generate_workshop_script():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto(config['STEAM_COLLECTION_URL'])
        item_list = await page.evaluate(GET_WORKSHOP_ARRAY)
        lua_output = LUA_TEMPLATE.format(item_list=item_list).replace('\\', '')

        f = open(config['LUA_OUTPUT_PATH'], 'w')
        f.write(lua_output)
        f.close()
        await browser.close()

async def add_to_collection(workshop_id):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(f'https://steamcommunity.com/login/home/?goto=sharedfiles%2Ffiledetails%2F%3Fid%3D{workshop_id}')
        await page.fill('id=input_username', config['STEAM_USERNAME'])
        await page.fill('id=input_password', config['STEAM_PASSWORD'])
        await page.click('xpath=//*[@id="login_btn_signin"]/button')

        await page.wait_for_url(f'https://steamcommunity.com/sharedfiles/filedetails/?id={workshop_id}')
        titleHandle = await page.query_selector('.workshopItemTitle')
        title = await titleHandle.inner_text()

        await page.click('id=AddToCollectionBtn')
        await page.wait_for_selector(f'id={config["STEAM_COLLECTION"]}')
        await page.check(f'id={config["STEAM_COLLECTION"]}')
        await page.click('body > div.newmodal > div.newmodal_content_border > div > div.newmodal_buttons > div.btn_green_steamui.btn_medium')

        await browser.close()
        return title

async def start_server():
    global running_container
    await generate_workshop_script()
    print('building image...')
    [image, buildLogsGenerator] = docker_client.images.build(path='.', buildargs=config, quiet=False)
    print('image built!')
    image_id = image.short_id
    running_container = docker_client.containers.run(image_id, ports=PORTS, detach=True)
    print('server starting!')

def stop_server():
    global running_container
    running_container.kill()
    running_container.wait()
    running_container = None

async def restart_server():
    stop_server()
    await start_server()

@discord_client.event
async def on_ready():
    print('listening for commands...')

@discord_client.event
async def on_message(message):
    if message.channel.name != 'ttt':
        return
    if message.content.startswith('!start_server'):
        if (running_container):
            await message.channel.send('Server is already running, try restarting instead')
            return
        await start_server()
        await message.channel.send(f'Server starting (container id: {running_container.short_id})')
    if message.content.startswith('!restart_server'):
        stop_server()
        await start_server()
        await message.channel.send(f'Restarting server (container id: {running_container.short_id})')
    if message.content.startswith('!add_mod'):
        [_, workshop_id] = message.content.split(' ')
        title = await add_to_collection(workshop_id)
        await message.channel.send(f'Added mod: {title}')
    if message.content.startswith('!mods'):
        await message.channel.send(f'Workshop Collection: {config["STEAM_COLLECTION_URL"]}')
        


async def main():
    await discord_client.start(config['DISCORD_TOKEN'])

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())