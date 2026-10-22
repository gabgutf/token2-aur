#!/usr/bin/env python3
import functools
import jinja2
import os
import yaml


OUTPUT_PATH = "output/"

def load_yaml(filename: str):
	with open(filename, "r") as file:
		data = yaml.safe_load(file)
	return data if data is not None else {}


def render_template(env: jinja2.Environment, input_name: str, output_name: str, configs) -> None:
	config = functools.reduce(lambda a, b: a | b, configs)

	template = env.get_template(input_name)
	pkgbuild = template.render(**config)
	with open(f"{OUTPUT_PATH}/{output_name}", "w") as file:
		file.write(pkgbuild)


env = jinja2.Environment(
	variable_start_string="[[",
	variable_end_string="]]",
	block_start_string="[%",
	block_end_string="%]",
	comment_start_string="[#",
	comment_end_string="#]",
	keep_trailing_newline=True,
	loader = jinja2.FileSystemLoader("packages/"),
	undefined=jinja2.StrictUndefined
)

os.makedirs(OUTPUT_PATH, exist_ok=True)
global_config = load_yaml("metadata.yml")
pkgbuilds = [filename for filename in os.listdir("packages/") if filename.startswith("PKGBUILD")]

for filename in pkgbuilds:
	render_template(
		env=env,
		input_name=filename,
		output_name=filename.removesuffix(".j2"),
		configs=[global_config]
	)
