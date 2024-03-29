import pyotp
import json
import discord
import os
import sys
import pathlib

available_services = {"Discord", "Google"}
send_services = {"Discord"}


class ServiceIsNotFound(Exception):
    pass


class TokenIsNotFound(Exception):
    pass


class AuthData:

    def __init__(self, service, file_address='AUTH_DATA.json'):
        if service not in available_services:
            raise ServiceIsNotFound(f"not found service name is {service}")

        self.file_address = file_address
        self.service = service
        self.p_lib = pathlib.Path(file_address)
        self.auth_key = None
        self.read_key()

    def set_key(self):
        token = input(f"Please type {self.service} key >> ").replace(" ", "")
        self.auth_key = token
        json_data = dict()
        with open(self.file_address, "w") as f:
            try:
                json_data = json.load(f)
            except:
                pass
            json_data[self.service]["Token"] = token
            json.dumps(json_data)

    def read_key(self):

        if not os.path.exists(self.file_address):
            self.p_lib.touch()

        with open(self.file_address, "r") as f:
            try:
                json_data = json.load(f)
                self.auth_key = json_data[self.service]["Token"]
            except KeyError:
                self.auth_key = None
            except json.JSONDecodeError:
                self.auth_key = None

        if self.auth_key is None:
            self.set_key()
        self.auth_key = self.auth_key.replace(" ", "")
        return self.auth_key

    def get_key(self):
        if self.auth_key is None:
            raise TokenIsNotFound
        else:
            return self.auth_key


class Totp(AuthData):

    def __init__(self, service, file_address='AUTH_DATA.json'):
        super(Totp, self).__init__(service, file_address)
        if service not in available_services - send_services:
            raise ServiceIsNotFound

    def first(self):
        # please write first setting
        # add_token and return TOTP code
        self.set_key()
        self.get_token()

    def get_token(self):
        key = self.read_key()
        totp = pyotp.TOTP(key)
        return totp.now()

    def get_token_string(self, message):
        token = self.get_token()
        str_format = f"{message.author.mention} {self.service} token is {token}"
        return str_format

    # def add_new_discord_token():


class DiscordService(AuthData):

    def __init__(self, service, file_address='AUTH_DATA.json'):
        super(DiscordService, self).__init__(service, file_address)
        self.channel_id = None

    def get_channel_id(self):
        if self.channel_id is None:
            with open(self.file_address, "r") as f:
                try:
                    json_data = json.load(f)
                    self.channel_id = json_data['Discord']["ChannelID"]
                except KeyError:
                    self.channel_id = None
                except json.JSONDecodeError:
                    self.channel_id = None
        return self.channel_id


#     token = input("Please type  discord token >> ").replace(" ", "")
#     with open("SECRET_DATA", "w") as f:
#         dict = json.dumps(f.read())
#         dict[token] = token
if __name__ == '__main__':
    proxy = None
    if "HTTP_PROXY" in os.environ:
        proxy = os.environ["HTTP_PROXY"]
    client = discord.Client(proxy=proxy)

    google_instance = Totp("Google", file_address="AUTH_DATA/AUTH_DATA.json")
    discord_instance = DiscordService("Discord",
                                      file_address="AUTH_DATA/AUTH_DATA.json")

    if discord_instance.auth_key is None:
        print("Discord totp is not found")
        print("So start initialized")
        print(discord_instance.set_key())

    if google_instance.auth_key is None:
        print("Google totp is not found")
        print("So start initialized")
        print(google_instance.first())

    @client.event
    async def on_ready():
        print("login success")

    @client.event
    async def on_message(message):
        channel_id = discord_instance.get_channel_id()
        channel = client.get_channel(channel_id)
        if channel is None:
            raise TokenIsNotFound('channel_id not found')

        if message.author.bot:
            return
        if message.content == '/google':
            send_text = google_instance.get_token_string(message)
            await channel.send(send_text)

    client.run(discord_instance.get_key())
