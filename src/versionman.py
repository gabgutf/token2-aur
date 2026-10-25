#!/usr/bin/env python3
from command_parse import add_command
import git
from ruamel.yaml import YAML
from semantic_version import Version
import sys


METADATA_YML = "metadata.yml"

def yaml_loader() -> YAML:
	yaml = YAML()
	yaml.preserve_quotes = True
	yaml.indent(mapping=2, sequence=4, offset=2)
	return yaml

def load_yaml():
	with open(METADATA_YML, 'r') as file:
		return yaml_loader().load(file)

def store_yaml(data):
	with open(METADATA_YML, 'w') as file:
		return yaml_loader().dump(data, file)


def get_version_cmd(args):
	yaml = load_yaml()
	raw_version = yaml["version"]
	version = Version(raw_version)
	release = yaml["release"]

	match args.get:
		case "major":
			print(version.major)
		case "minor":
			print(version.minor)
		case "patch":
			print(version.patch)
		case "semver":
			print(raw_version)
		case "pkgrelease":
			print(release)
		case "full":
			print(f"{raw_version}-{release}")


def modify_version_cmd(args):
	yaml = load_yaml()
	match args.modify:
		case "bump":
			yaml["release"] += 1
			store_yaml(yaml)

		case "set":
			spec = Version(args.version)
			yaml["release"] = int(spec.prerelease[0]) if spec.prerelease else 1
			yaml["version"] = str(spec.truncate("patch"))
			store_yaml(yaml)

	print(f"{yaml['version']}-{yaml['release']}")


def tag_manage_cmd(args):
	repo = git.Repo(".")
	tags = sorted(repo.tags, reverse=True, key=lambda tag: tag.commit.committed_date)

	latest_version = None
	for tag in tags:
		try:
			latest_version = Version(tag.name.removeprefix("v"))
			break
		except:
			pass

	match args.tag:
		case "get":
			if latest_version is None:
				sys.exit(1)
			print(latest_version)

		case "versionchanged":
			yaml = load_yaml()
			current_version = Version(yaml["version"])

			if latest_version is None or current_version != latest_version.truncate("patch"):
				print("true")
				sys.exit(0)

			else:
				print("false")
				sys.exit(1)



COMMANDS = {
	"get": {
		"description": "Get information about the current version",
		"subcommands": {
			"major": "Get MAJOR component",
			"minor": "Get MINOR component",
			"patch": "Get PATCH component",
			"semver": "Get Semver version: X.Y.Z",
			"pkgrelease": "Get Arch Linux package pkgrelease value",
			"full": "Get Semver+pkgrelease value: X.Y.Z-R"
		},
		"run": get_version_cmd
	},
	"modify": {
		"description": "Increase or set the package version. Prints the full modified version",
		"subcommands": {
			"bump": "Increase the pkgrelease version by 1",
			"set": {
				"description": "Set the current version",
				"arguments": {
					"version": {
						"description": "Version spec to set. Either a Semver value (X.Y.Z), or a Semver+pkgrelease value. If only Semver is specified, the pkgrelease will be set to 1",
						"type": str,
					}
				},
			}
		},
		"run": modify_version_cmd
	},
	"tag": {
		"description": "Interacts with the latest Git release tag",
		"subcommands": {
			"get": "Returns the latest release version (no leading 'v'). Empty if none found",
			"versionchanged": f"Checks whether the latest release tag is the same as the one in {METADATA_YML}. Prints true and exits with 0 if changed, or no release was found. Prints false and exits with 0 otherwise"
		},
		"run": tag_manage_cmd
	}
}

parser = add_command(
	prog="versionman",
	description="Allows CI/CD to manage version control",
	commands=COMMANDS
)

args = parser.parse_args()
args.run(args)
