import pyotp
import json
import discord

available_services = {"Discord", "Google"}
send_services = {"Discord"}


class ServiceIsNotFound(Exception):
    pass


class TokenIsNotFound(Exception):
    pass


class AuthData:
    def __init__(self, service, file_address='AUTH_DATA'):
        if service not in available_services:
            raise ServiceIsNotFound(f"not found service name is {service}")

        self.file_address = file_address
        self.service = service
        self.auth_key = None
        self.read_key()

    def set_key(self):
        token = input(f"Please type {self.service} key >> ").replace(" ", "")
        self.auth_key = token
        with open(self.file_address, "w") as f:
            json_data = json.load(f)
            json_data[self.service] = token
            json.dumps(json_data)

    def read_key(self):
        with open(self.file_address, "r") as f:
            json_data = json.load(f)
            try:
                self.auth_key = json_data[self.service]
            except KeyError:
                self.auth_key = None
        if self.auth_key is None:
            self.set_key()
        return self.auth_key

    def get_key(self):
        if self.auth_key is None:
            raise TokenIsNotFound
        else:
            return self.auth_key


class Totp(AuthData):
    def __init__(self, service, file_address='AUTH_DATA'):
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
        return totp

    def get_token_string(self):
        token = self.get_token()
        str_format = f"{self.service} token is {token}"
        return str_format
    # def add_new_discord_token():


#     token = input("Please type  discord token >> ").replace(" ", "")
#     with open("SECRET_DATA", "w") as f:
#         dict = json.dumps(f.read())
#         dict[token] = token
if __name__ == '__main__':
    client = discord.Client()
    discord_instance = AuthData("Discord")
    google_instance = Totp("Google")
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
        pass


    @client.event
    async def on_message(message):
        if message.author.bot:
            return
        if message.content == '/google':
            await message.channel.send(google_instance.get_token_string())


    client.run(discord_instance.get_key)
