# Discord Server Cloner

A Python tool for cloning Discord server structure including roles, channels, and server settings.

## Features

- Clone server roles with permissions, colors, and settings
- Copy all channel types (text, voice, categories, forums, etc.)
- Recreate channel permissions and category structure
- Copy server-level settings (verification level, content filter, etc.)
- Option to delete existing channels in target server
- Rate limit handling with configurable cooldowns

## Requirements

- Python 3.6+
- `requests` library

## Installation

1. Install required dependency:
```bash
pip install requests
