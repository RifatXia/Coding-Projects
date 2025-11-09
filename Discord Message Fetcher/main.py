#!/usr/bin/env python3
"""
Discord Message Fetcher
A simple script to fetch messages from a Discord channel and save them to a text file.
"""

import os
import sys
import argparse
import re
import requests
from datetime import datetime
from dotenv import load_dotenv


def load_environment():
    """load environment variables from .env file."""
    load_dotenv()
    token = os.getenv('DISCORD_TOKEN')
    channel_id = os.getenv('CHANNEL_ID')
    
    if not token:
        print("Error: DISCORD_TOKEN not found in .env file")
        print("Please create a .env file with your Discord token")
        print("See README.md for instructions")
        sys.exit(1)
    
    if not channel_id:
        print("Error: CHANNEL_ID not found in .env file")
        print("Please add CHANNEL_ID to your .env file")
        print("See README.md for instructions")
        sys.exit(1)
    
    return token, channel_id


def fetch_messages(channel_id, token, limit=100):
    """
    fetch messages from a discord channel.
    
    args:
        channel_id (str): the discord channel id
        token (str): discord user token
        limit (int): number of messages to fetch (default: 100, max: 100 per request)
    
    returns:
        list: list of message objects
    """
    url = f"https://discord.com/api/v10/channels/{channel_id}/messages"
    headers = {
        "Authorization": token,
        "Content-Type": "application/json"
    }
    
    all_messages = []
    remaining = limit
    last_message_id = None
    
    print(f"Fetching messages from channel {channel_id}...")
    
    while remaining > 0:
        # discord api allows max 100 messages per request
        fetch_limit = min(remaining, 100)
        params = {"limit": fetch_limit}
        
        if last_message_id:
            params["before"] = last_message_id
        
        try:
            response = requests.get(url, headers=headers, params=params)
            
            if response.status_code == 200:
                messages = response.json()
                
                if not messages:
                    print("No more messages to fetch")
                    break
                
                all_messages.extend(messages)
                remaining -= len(messages)
                last_message_id = messages[-1]['id']
                
                print(f"Fetched {len(all_messages)} messages so far...")
                
                # if we got fewer messages than requested, we've reached the end
                if len(messages) < fetch_limit:
                    break
                    
            elif response.status_code == 401:
                print("Error: Invalid Discord token")
                print("Please check your DISCORD_TOKEN in the .env file")
                sys.exit(1)
            elif response.status_code == 403:
                print("Error: Access forbidden - you don't have permission to access this channel")
                sys.exit(1)
            elif response.status_code == 404:
                print("Error: Channel not found - please check the channel ID")
                sys.exit(1)
            else:
                print(f"Error: HTTP {response.status_code}")
                print(response.text)
                sys.exit(1)
                
        except requests.exceptions.RequestException as e:
            print(f"Network error: {e}")
            sys.exit(1)
    
    return all_messages


def format_message(message):
    """
    format a message object into a readable string.
    
    args:
        message (dict): discord message object
    
    returns:
        str: formatted message string
    """
    author = message.get('author', {})
    username = author.get('username', 'Unknown')
    timestamp = message.get('timestamp', '')
    content = message.get('content', '')
    
    # parse timestamp
    try:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S UTC')
    except:
        formatted_time = timestamp
    
    # format message
    formatted = f"[{formatted_time}] {username}: {content}"
    
    # add attachments info if present
    attachments = message.get('attachments', [])
    if attachments:
        formatted += "\n  Attachments:"
        for att in attachments:
            formatted += f"\n    - {att.get('filename', 'file')}: {att.get('url', '')}"
    
    # add embeds info if present
    embeds = message.get('embeds', [])
    if embeds:
        formatted += "\n  Embeds: " + str(len(embeds)) + " embed(s)"
    
    return formatted


def extract_links(messages):
    """
    extract all links from messages.
    
    args:
        messages (list): list of message objects
    
    returns:
        list: list of unique urls found in messages
    """
    # regex pattern to match urls
    url_pattern = re.compile(
        r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    )
    
    links = []
    
    for message in messages:
        # extract links from message content
        content = message.get('content', '')
        found_urls = url_pattern.findall(content)
        links.extend(found_urls)
        
        # extract attachment urls
        attachments = message.get('attachments', [])
        for att in attachments:
            url = att.get('url', '')
            if url:
                links.append(url)
        
        # extract embed urls
        embeds = message.get('embeds', [])
        for embed in embeds:
            # embed url
            if 'url' in embed and embed['url']:
                links.append(embed['url'])
            # embed image url
            if 'image' in embed and 'url' in embed['image']:
                links.append(embed['image']['url'])
            # embed thumbnail url
            if 'thumbnail' in embed and 'url' in embed['thumbnail']:
                links.append(embed['thumbnail']['url'])
            # embed video url
            if 'video' in embed and 'url' in embed['video']:
                links.append(embed['video']['url'])
    
    # return unique links while preserving order
    seen = set()
    unique_links = []
    for link in links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)
    
    return unique_links


def save_links(links, output_file):
    """
    save extracted links to a text file.
    
    args:
        links (list): list of urls
        output_file (str): output file path
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Extracted Links\n")
            f.write(f"Total links: {len(links)}\n")
            f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            for link in links:
                f.write(link + "\n")
        
        print(f"Successfully saved {len(links)} links to {output_file}")
        
    except IOError as e:
        print(f"Error saving links file: {e}")
        sys.exit(1)


def save_messages(messages, output_file):
    """
    save messages to a text file.
    
    args:
        messages (list): list of message objects
        output_file (str): output file path
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"Discord Messages Export\n")
            f.write(f"Total messages: {len(messages)}\n")
            f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # messages are returned newest first, so reverse for chronological order
            for message in reversed(messages):
                f.write(format_message(message) + "\n\n")
        
        print(f"\nSuccessfully saved {len(messages)} messages to {output_file}")
        
    except IOError as e:
        print(f"Error saving file: {e}")
        sys.exit(1)


def main():
    """main function to run the discord message fetcher."""
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Fetch messages from a Discord channel')
    parser.add_argument('-l', '--limit', type=str, default='100',
                        help='Number of messages to fetch (default: 100, use "all" to fetch all messages)')
    parser.add_argument('-o', '--output', type=str, default='messages.txt',
                        help='Output file name (default: messages.txt)')
    parser.add_argument('--extract-links', action='store_true',
                        help='Extract all links and save to links.txt')
    
    args = parser.parse_args()
    
    print("=" * 80)
    print("Discord Message Fetcher")
    print("=" * 80)
    
    # load discord token and channel id from environment
    token, channel_id = load_environment()
    
    # parse limit argument (can be a number or "all")
    limit_str = args.limit.lower()
    if limit_str == 'all':
        limit = float('inf')  # infinite limit to fetch all messages
        limit_display = "All available messages"
    else:
        try:
            limit = int(args.limit)
            if limit <= 0:
                print("Error: Number of messages must be greater than 0")
                sys.exit(1)
            limit_display = str(limit)
        except ValueError:
            print(f"Error: Invalid limit value '{args.limit}'. Use a number or 'all'")
            sys.exit(1)
    
    output_file = args.output
    # ensure .txt extension
    if not output_file.endswith('.txt'):
        output_file += '.txt'
    
    print(f"\nChannel ID: {channel_id}")
    print(f"Messages to fetch: {limit_display}")
    print(f"Output file: {output_file}\n")
    
    # fetch and save messages
    try:
        messages = fetch_messages(channel_id, token, limit)
        
        if messages:
            save_messages(messages, output_file)
            
            # extract and save links if requested
            if args.extract_links:
                print("\nExtracting links...")
                links = extract_links(messages)
                if links:
                    save_links(links, 'links.txt')
                else:
                    print("No links found in messages")
        else:
            print("No messages were fetched")
        
        print("\nDone!")
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(0)


if __name__ == "__main__":
    main()
