#!/bin/python3
import bs4
import requests
from Typing import List, Tuple, Dict, Any

from imessage import send_imessage


def get_weather_string(location: str) -> str:
	"""
	
	:param location: 
	:return: 
	"""

	weather_url = f"https://www.theweathernetwork.com/ca/weather/british-columbia/{location.replace(' ', '-')}"

	

if __name__ == "__main__":

	
