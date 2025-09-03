from typing import Optional
from datetime import datetime
import logging

import json
import requests
from . import InputSource
from common import Notification, NotificationLevel

GITHUB_PREFIX = "https://github.com/"

BODY_FORMAT = """New version: {version}
Published on {date}
By {author}"""

@InputSource
class Github:
	def is_url_valid(url: str) -> bool:
		# Accepted url: https://github.com/[^/]+/[^/]+
		if not url.startswith(GITHUB_PREFIX):
			return False
		url = url[len(GITHUB_PREFIX):]
		elts = url.split('/')
		if len(elts) != 2:
			return False
		return len(elts[0]) > 0 and len(elts[1]) > 0

	def get_name(url: str) -> str:
		url = url[len(GITHUB_PREFIX):]
		elts = url.split('/')
		return elts[1]

	def get_release(url: str, last_update: datetime) -> Optional[Notification]:
		url = url.replace('https://github.com', 'https://api.github.com/repos') + '/releases?per_page=1&page=1'
		resp = requests.request("GET", url, headers = {
			'X-GitHub-Api-Version': '2022-11-28',
			'Accept': 'application/vnd.github+json'
		})

		if resp.status_code != 200:
			logging.warning(f"Received an error {resp.status_code}: {resp.body}")
			return None
		
		encoded_json = '{"elts": %s}' % resp.content.decode("utf-8")
		releases = json.loads(encoded_json).get("elts", [])
		if len(releases) != 1:
			logging.warning("No new releases")
			return None
		
		release = releases[0]
		release_date = release.get("published_at")
		if release_date:
			release_date = datetime.fromisoformat(release_date)
			if release_date < last_update:
				return None
			release_date = release_date.strftime("%d-%m-%y %H:%M")
		else:
			release_date = ""
		
		return Notification(
			title = "",
			body=BODY_FORMAT.format(
				version = release.get("tag_name", "[ERROR]"),
				author = release.get("author", {}).get("login", ""),
				date = release_date
			),
			level = NotificationLevel.LOW,
			cmd_on_click =
				["/bin/sh", "-c", "firefox", release["html_url"]]
				if "html_url" in release else []
		)
