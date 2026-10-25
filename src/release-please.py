#!/usr/bin/env python3

# WARNING:
# This script relies on parsing unstable CLI output, which may change between
# releases!
# Keep this in mind when updating release-please.

from command_parse import add_command
import os
import re
import subprocess
import sys
from typing import Tuple


MASTER_BRANCH_NAME="master"

def release_please(*args) -> Tuple[str, str]:
	process = subprocess.run([
		"npx", "release-please",
		"--repo-url", REPO_URL,
		"--token", GH_TOKEN,
		*args
	], capture_output=True)

	stdout, stderr = (process.stdout.decode("utf-8"), process.stderr.decode("utf-8"))

	if process.returncode != 0:
		print("Error running release-please:", file=sys.stderr)
		print(f"STDOUT:\n{stdout}", file=sys.stderr)
		print(f"STDERR:\n{stderr}", file=sys.stderr)
		sys.exit(process.returncode)

	return (stdout, stderr)


def pr_cmd(args):
	match args.pr:
		case "update":
			release_please("release-pr","--release-as", args.version)

		case "branch":
			print(f"release-please--branches--{MASTER_BRANCH_NAME}")


def release_cmd(args):
	match args.release:
		case "shouldcreate":
			release_regex = re.compile("^✔ Would tag ([0-9]+) releases:$")
			stdout, _ = release_please("github-release", "--dry-run")
			created_releases_strings = [
				int(match.group(1))
				for line in stdout.splitlines()
				if (match := release_regex.match(line))
			]
			release_count = created_releases_strings[0] if len(created_releases_strings) == 1 else None

			if release_count is None:
				print("Error: unable to match release count", file=sys.stderr)
				sys.exit(1)

			print("true" if release_count != 0 else "false")
			sys.exit(0 if release_count != 0 else 1)

		case "create":
			release_please("github-release")



COMMANDS = {
	"pr": {
		"description": "Manages release PRs",
		"subcommands": {
			"update": {
				"description": "Creates or updates the release PR",
				"arguments": {
					"version": {
						"description": "Full release version",
						"type": str,
					}
				},
			},
			"branch": "Returns the branch of the PR release"
		},
		"run": pr_cmd
	},
	"release": {
		"description": "Manages release creation",
		"subcommands": {
			"shouldcreate": "Prints true and returns 0 if a release is ready to be created. Prints false and returns 1 otherwise",
			"create": "Creates a release if one is staged"
		},
		"run": release_cmd
	},
}

REPO_URL = os.environ["GIT_REPO_URL"]
GH_TOKEN = os.environ["GITHUB_TOKEN"]

parser = add_command(
	prog="release-please",
	description="Manages release-please through a simpler CLI. Requires GIT_REPO_URL and GH_TOKEN to be set as environment variables.",
	commands=COMMANDS
)

args = parser.parse_args()
args.run(args)
