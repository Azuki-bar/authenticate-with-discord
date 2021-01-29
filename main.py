import pyotp
import json
import discord

available_services = ("Discord", "Google")


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
        self.token = None
        self.set_token()

    def set_token(self):
        token = input(f"Please type {self.service} token >> ").replace(" ", "")
        self.token = token
        with open(self.file_address, "w") as f:
            json_data = json.load(f)
            json_data[self.service] = token
            json.dumps(json_data)

    # @property
    def get_token(self):
        if self.token is None:
            raise TokenIsNotFound
        else:
            return self.token


# def add_new_discord_token():
#     token = input("Please type  discord token >> ").replace(" ", "")
#     with open("SECRET_DATA", "w") as f:
#         dict = json.dumps(f.read())
#         dict[token] = token
if __name__ == '__main__':
    pass
