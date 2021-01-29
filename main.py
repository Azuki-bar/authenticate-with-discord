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



# def add_new_discord_token():
#     token = input("Please type  discord token >> ").replace(" ", "")
#     with open("SECRET_DATA", "w") as f:
#         dict = json.dumps(f.read())
#         dict[token] = token
if __name__ == '__main__':
    pass
