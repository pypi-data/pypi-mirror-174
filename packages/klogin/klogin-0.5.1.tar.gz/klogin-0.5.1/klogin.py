import sys
import shutil
import argparse
import platformdirs
import configparser
from pathlib import Path
import subprocess as sub
from os import environ as env
from argparse import RawDescriptionHelpFormatter


class SSOSessionError(Exception):
	pass


def resource_path(relative_path):
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = Path(sys._MEIPASS)
	except Exception:
		base_path = Path(__file__).parent.absolute()

	return Path.joinpath(base_path, relative_path)


def load_config():
	config_dir = Path(platformdirs.user_config_dir('klogin'))
	profiles_path = config_dir.joinpath('profiles')
	config = configparser.ConfigParser()
	print(f'loading config from {profiles_path}')
	#p = Path(config_path).expanduser()
	#profiles_path = resource_path('profiles')
	if not profiles_path.exists():
		print('no config found - using default profiles')
		return None
	config.read(profiles_path)
	profiles = {}
	for section in config.sections():
		_section = section.split('profile ')[-1]
		profiles[_section] = {}
		for option in config.options(section):
			profiles[_section][option] = config.get(section, option)
	#print(f"config loaded: {profiles}")
	return profiles


def write_profiles(kconfig):
	if kconfig is None:
		return
	profiles_path = resource_path('profiles')
	profiles = kconfig['profiles']
	awsconfig = configparser.ConfigParser(allow_no_value=True)
	for profile in profiles:
		awsconfig.add_section(f'profile {profile}')
		for key, value in profiles[profile].items():
			awsconfig.set(profile, key, value)
	with open(profiles_path, 'w') as f:
		awsconfig.write(f)


def execute(cmd, capture=True):
	config_dir = Path(platformdirs.user_config_dir('klogin'))
	profiles_path = config_dir.joinpath('profiles')
	#profiles_path = resource_path('profiles')
	env['AWS_CONFIG_FILE'] = env.get('AWS_CONFIG_FILE', str(profiles_path))
	print(f"executing command <{cmd}> with AWS_CONFIG_FILE={env['AWS_CONFIG_FILE']}")
	return sub.run(
		cmd,
		shell=True,
		check=True,
		capture_output=capture,
		env=env
	)


def sso_login(profile):
	command = f'aws sso login --profile {profile}'
	execute(command, capture=False)


def update_kubeconfig(cluster_name, alias, profile):
	command = (
		f'aws eks update-kubeconfig '
		f'--name {cluster_name} '
		f'--profile {profile} '
		f'--alias {alias}'
	)
	try:
		p = execute(command)
		print(p.stdout.strip().decode())
	except sub.CalledProcessError as ex:
		msg = ex.stderr.strip().decode()
		if msg.startswith('Error loading SSO Token:'):
			raise SSOSessionError(msg)
		else:
			print(ex.stderr.decode())
			raise ex


def manage_profiles(command):
	print('manage profiles')
	print(f"command: {command}")
	if command is None:
		print('no profile command given - display profiles overview')
		profiles_path = resource_path('profiles')
		print(f"profiles_path: {profiles_path}")
		with open(profiles_path) as f:
			content = f.read()
		print(f'available profiles:')
		print(content)
	if command == 'add':
		print('add a new profile')
	if command == 'list':
		print('display profiles overview')


def login(cluster_name, cluster_alias, profile, sso_region):
	print(f'login to cluster: {cluster_name}')
	try:
		update_kubeconfig(cluster_name, cluster_alias, profile)
	except SSOSessionError:
		sso_login(f'sso-{sso_region}')
		update_kubeconfig(cluster_name, cluster_alias, profile)


def print_section(section, items):
	print(f"[{section}]")
	for key, value in items:
		print(f'{key} = {value}')


def print_config(config):
	for section in config.sections():
		print_section(section, config.items(section))
		print()


def bootstrap(dry=True):
	print(f"dry: {dry}")
	print('bootstrap')
	aws_config = Path('~/.aws/config').expanduser()
	current_config = configparser.ConfigParser(allow_no_value=True)
	if aws_config.exists():
		current_config.read(aws_config)
	profiles_path = resource_path('profiles')
	baked_config = configparser.ConfigParser()
	baked_config.read(profiles_path)
	for section in baked_config.sections():
		if current_config.has_section(section):
			print_section(section, baked_config.items(section))
			print()
			print_section(section, current_config.items(section))
			print()
			answer = input(f"Overwrite '{section}' [y/n] ? ")
			print()
			if answer.lower() in ['y' 'yes']:
				current_config.add_section(section)
				for key, value in baked_config.items(section):
					current_config.set(section, key, value)
		else:
			print_section(section, baked_config.items(section))
			print()
			answer = input(f"Add '{section}' [y/n] ? ")
			print()
			if answer.lower() in ['y' 'yes']:
				current_config.add_section(section)
				for key, value in baked_config.items(section):
					current_config.set(section, key, value)
	print('----------------------------------------------------------')
	print_config(current_config)
	print('----------------------------------------------------------')
	if not dry:
		answer = input(f"Write config to {aws_config} [y/n] ? ")
		with open(aws_config, 'w') as configfile:
			current_config.write(configfile)
	config_dir = Path(platformdirs.user_config_dir('klogin'))
	#if not config_dir.exists():
	#	print('config_dir does not exist - creating it')
	#	config_dir.mkdir(parents=True)
	#profiles_path = config_dir.joinpath('profiles')
	#shutil.copy(resource_path('profiles'), profiles_path)
	print('bootstrap complete')


def main():
	parser = argparse.ArgumentParser(
		prog = 'klogin',
		description = 'Log in to GenuityScience kubernetes clusters',
		epilog = 'Example usage:\nklogin -c=/home/user/myklogin.yml platform-dev admin',
		formatter_class=RawDescriptionHelpFormatter
	)
	#parser.add_argument('-c', '--config', nargs='?', default='~/klogin.yml')
	cluster = parser.add_argument_group(
		'cluster',
		'''
		Choose a cluster to login to
		Example: klogin platform-dev
		'''
	)
	cluster.add_argument('-r', '--region', nargs='?')
	parser.add_argument("first", nargs='?', help='<cluster-name>/<command>')
	profiles = parser.add_argument_group(
		'profiles',
		'''
		Manage profiles
		Example: klogin profile add
		'''
	)
	profiles.add_argument(
		'-d',
		'--dry',
		nargs='?',
		default=False,
		help='Dry run initialization'
	)
	parser.add_argument("second", nargs='?', help='<role>/<command>')
	args = parser.parse_args()
	#print(f"args: {args}")
	# if no arguments are provided we exit and show the help message
	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)
	if args.first in ['bootstrap', 'init']:
		bootstrap(args.dry)
		sys.exit(0)
	config = load_config()
	if args.first in ['profile', 'profiles']:
		manage_profiles(args.second)
	else:
		cluster_alias = args.first
		role = args.second or 'ro'
		# construct the profile name, <clustername>-<rolename>
		# for cluster platform-dev and role admin: platform-dev-admin 
		# for cluster gor-dev and role ro: gor-dev-ro
		profile = f'{cluster_alias}-{role}'
		#cluster_name = config['clusters'][cluster_alias]['name']
		cluster_name = config[profile]['cluster_name']
		sso_region = config[profile]['sso_region']
		login(cluster_name, cluster_alias, profile, sso_region)


if __name__ == '__main__':
	main()
