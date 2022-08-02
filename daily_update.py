#!/bin/python3
from dataclasses import dataclass
import bs4
import requests
from datetime import date
import time
from imessage import send_imessage
from rich.pretty import pprint
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
		return f'💯 {self.author.strip()}\n"{self.text.strip()}"\n'


def get_motivational_quote() -> str:

	base_url = "https://zenquotes.io/api/quotes"
	res = requests.get(base_url)
	res.raise_for_status()

	quote = Quote.json_string_to_quote(res.text)
	return quote


# def get_news_headlines(amount: int) -> List[str]:
#	  return


# def get_top_crypto(amount: int) -> List[str]:
#	return


# def get_top_stocks(amount: int) -> List[str]:
#	  return


@dataclass
class Contact:
	name: str
	number: str


contacts = [
	Contact("Andrew", "7783188920")
]


def today_string():
	day = date.today()
	return f"Today is {day.strftime('%A %B %d, %Y')}"


def send_greeting(contact: Contact):
	message = f"☀️ Good Morning {contact.name} ☀️\n{today_string()}\n\n"
	message += f"Here are your 3 Quotes of the Day:\n\n{get_motivational_quote()}\n{get_motivational_quote()}\n{get_motivational_quote()}"
	send_imessage(contact.number, message)


if __name__ == "__main__":
	with open("state.txt", "r") as file_obj:
		today = today_string()
		if today in file_obj.readlines():
			exit(0)
	
	for contact in contacts:
		send_greeting(contact)

	with open("state.txt", "w") as file_obj:
		file_obj.write(today)
