#!/bin/python3
from dataclasses import dataclass
import bs4
import requests
from datetime import date
import time
from imessage import send_imessage
from rich.pretty import pprint
from typing import List, Dict, Optional, Union, Any
import os
import json


# Crontab Used: 0 6 * * * cd ~/Programming/Daily-Update-Message && /Library/Frameworks/Python.framework/Versions/3.8/bin/python3 daily_update.py >> daily_update.txt 2>&1


def get_weather_string(location: str) -> str:
    """

    :param location:
    :return:
    """

    weather_url = f"https://www.theweathernetwork.com/ca/weather/british-columbia/{location.replace(' ', '-')}"


@dataclass
class Quote:
    text: str
    author: str

    @staticmethod
    def json_string_to_quote(json_string: str) -> "Quote":
        json_data = json.loads(json_string)
        if isinstance(json_data, list):
            json_data = json_data[0]
        if not isinstance(json_data, dict):
            print(f"[bold red]ERROR[/] Incorrect data type of: {json_data}")
            exit(1)
        return Quote(
            text=json_data['q'],
            author=json_data['a']
        )

    def __repr__(self):
        return f'"{self.text.strip()}"\n{self.author.strip()}\n'


def get_motivational_quote() -> str:

    base_url = "https://zenquotes.io/api/quotes"
    res = requests.get(base_url)
    res.raise_for_status()

    quote = Quote.json_string_to_quote(res.text)
    return quote


# def get_news_headlines(amount: int) -> List[str]:
#     return


# def get_top_crypto(amount: int) -> List[str]:
#   return


# def get_top_stocks(amount: int) -> List[str]:
#     return


@dataclass
class Contact:
    name: str
    number: str


def today_string():
    day = date.today()
    return f"Today is {day.strftime('%A %B %d, %Y')}"


def send_greeting(contact: Contact):
    message = f"Good Morning {contact.name}\n{today_string()}\n\n"
    message += f"{get_motivational_quote()}\n{get_motivational_quote()}\n{get_motivational_quote()}"
    send_imessage(contact.number, message)


def get_contacts() -> List[Contact]:
    contacts_fp = "contacts.json"

    def _warning(msg: str):
        print(f"[orange]WARNING[/] {msg}")
        print("\nRe-run the program when this warning is fixed.")
        exit(1)

    if not os.path.isfile(contacts_fp):
        with open(contacts_fp, "w") as f:
            f.write("{\n\n}")
        _warning(f"Could not find '{contacts_fp}' file.\n\nCopying template file to '{contacts_fp}'.\nAdd your contacts by key=name, value=number as a Dictionary object in the file.")

    with open(contacts_fp, "r") as contacts_file:
        contacts_text = contacts_file.read()
        dict_contacts = json.loads(contacts_text)

    contacts = list(map(lambda pair: Contact(pair[0], pair[1]), dict_contacts.items()))

    if not contacts:
        _warning(f"No contacts found in '{contacts_fp}' file.\nAdd your contacts by key=name, value=number as a Dictionary object in the file.")

    return contacts


def check_state():
    state_file = "state.txt"
    if not os.path.isfile(state_file):
        with open(state_file, "w") as f:
            f.write("")

    with open(state_file, "r") as file_obj:
        today = today_string()
        if today in file_obj.readlines():
            exit(0)

    
def update_state():
    today = today_string()
    with open("state.txt", "w") as file_obj:
        file_obj.write(today)


def main():

    # Check if we have already notified the contacts
    check_state()

    # Send Greeting to all contacts
    for contact in get_contacts():
        send_greeting(contact)

    # Save state that we have already notified the contacts
    update_state()


if __name__ == "__main__":
    main()

