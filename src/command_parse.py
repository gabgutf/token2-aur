#!/usr/bin/env python3
import argparse

def add_command_parser(parser, name, command_spec):
	if isinstance(command_spec, str):
		parser.add_parser(name, help=command_spec)
		return

	this_parser = parser.add_parser(
		name,
		help=command_spec["description"]
	)
	if "run" in command_spec:
		this_parser.set_defaults(run=command_spec["run"])

	for argument_name, argument_spec in command_spec.get("arguments", {}).items():
		extra_args = {"required": True} if argument_spec.get("required", False) else {}
		this_parser.add_argument(
			argument_name,
			help=argument_spec["description"],
			type=argument_spec["type"],
			**extra_args
		)

	if "subcommands" in command_spec:
		this_subparsers = this_parser.add_subparsers(dest=name, required=True)
		for subcommand_name, subcommand_spec in command_spec.get("subcommands", {}).items():
			add_command_parser(
				this_subparsers,
				subcommand_name,
				subcommand_spec
			)


def add_command(prog, description, commands):
	parser = argparse.ArgumentParser(prog=prog, description=description)

	if commands:
		subparsers = parser.add_subparsers(required=True)
		for name, spec in commands.items():
			add_command_parser(subparsers, name, spec)

	return parser
