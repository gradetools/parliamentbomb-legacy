import os
import logging
import subprocess
import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv
import json
load_dotenv()
logging.basicConfig(level=logging.WARNING)
intents = nextcord.Intents.all()
bot = commands.Bot(intents=intents)
logger = logging.getLogger('nextcord')
logger.setLevel(logging.WARNING)
handler = logging.FileHandler(filename='nextcord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

def load_json_to_dict(nix_file_path):
        output = subprocess.check_output(['nix-instantiate', '--eval', '--json', "--verbose" , "--strict" , nix_file_path])
        output = json.loads(output)
        return output

def format_json(input_json):
        json_output = json.loads(input_json)
        formatted_output = json.dumps(json_output, indent=4)
        return formatted_output
    
def load_lockfile(lockfile_path):
    with open(lockfile_path, 'r') as f:
        lockfile = json.load(f)
        return lockfile
@bot.event # ready sequence duh
async def on_ready():
    print(f"Ready, using {bot.user}")
    
lockfile = load_lockfile("server.lock")
nameofserver = load_json_to_dict("server.nix")
class Server:
    def __init__(self):
        self.name = nameofserver["serverName"]
        self.channels = nameofserver["channels"]
        self.icon = nameofserver["serverIcon"]
        self.roles = dict(nameofserver["roles"])
        self.id = int(lockfile["id"])
        self.guild = None
    class Roles:
        def __init__(self):
            pass
        def permissions(self):
            self.permissions = lockfile["id"]
    class Channels:
        def __init__(self):
            pass
        class Permissions:
    def get_name(self):
        return self.name
    def get_channels(self):
        return self.channels
    def roletype(self):
        return type(self.roles)
    def get_roles(self):
        return self.roles
    def get_id(self):
        return self.id
    async def rebuild(self,bot):
        self.guild = bot.get_guild(self.id)

pbts = Server()
print(pbts.roles)
last_user = None

        for channel in guild.text_channels:
            channel_name = channel.name.replace(' ', '_').lower()
            filename = os.path.join(guild_dir, f'{channel_name}.json')

            with open(filename, 'a', encoding='utf-8') as file:
                async for message in channel.history(limit=None):
                    data = {
                        'author': message.author.name,
                        'content': message.content,
                        'message_id': message.id,
                        'author_id': message.author.id,
                        'channel': str(message.channel),
                        'mentions': [mention.name for mention in message.mentions]
                    }
                    file.write(json.dumps(data, indent=4))
                    file.write("\n")


@bot.slash_command(description="Log all past messages")
async def log_past_messages(interaction: nextcord.Interaction):
    await interaction.send("Logging all past messages...")
    await log_all_past_messages()

@bot.slash_command(description="getunixtime")
async def get_unix_time(interaction: nextcord.Interaction):
    unixtime = requests.get("https://worldtimeapi.org/api/timezone/America/Edmonton")
    unixtimeformat = unixtime.json()
    unixtime_value = unixtimeformat["unixtime"]
    await interaction.send(f"time: {unixtime_value}")

@bot.slash_command(guild_ids=[1112507308661030992])
async def summary(interaction: nextcord.Interaction, password: str):
    if password != "balls123":
        await interaction.send("no wrong lol")

@bot.slash_command(description="rebuild")
async def rebuild(interaction: nextcord.Interaction):
    pbts = Server()
    pbtsid = pbts.get_id()  
    print(pbtsid)
    roles = pbts.roles
    print(type(roles))
    for role in roles:
        guild = interaction.guild
        if role in guild.roles:
            print("role exists! skipping!")
            break
        await guild.create_role(name=role)
        print("role created " + role)
    await interaction.send("finished rebuilding", ephemeral=True)
    


token = os.environ.get("TOKEN")
bot.run(token)
