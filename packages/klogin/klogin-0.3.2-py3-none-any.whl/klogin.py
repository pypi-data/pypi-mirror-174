import sys
import yaml
import argparse
import configparser
from pathlib import Path
import subprocess as sub
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


def load_config(config_path):
	print(f'loading config from {config_path}')
	p = Path(config_path).expanduser()
	if not p.exists():
		print('no config found - using default profiles')
		return None
	with open(p.expanduser()) as f:
		config = yaml.safe_load(f.read())
	print(f"config loaded: {config}")
	return config


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


def execute(cmd):
	profiles_path = resource_path('profiles')
	print(f'executing command <{cmd}> with AWS_CONFIG_FILE={profiles_path}')
	sub.run(
		cmd,
		shell=True,
		check=True,
		capture_output=True,
		env={
			'AWS_CONFIG_FILE': profiles_path
		}
	)


def sso_login(profile):
	command = f'aws sso login --profile {profile}'
	execute(command)


def update_kubeconfig(cluster_name, alias, profile):
	command = (
		f'aws eks update-kubeconfig '
		f'--name {cluster_name} '
		f'--profile {profile} '
		f'--alias {alias}'
	)
	try:
		execute(command)
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


def login(cluster_name, cluster_alias, profile, region):
	print(f'login to cluster: {cluster_name}')
	try:
		update_kubeconfig(cluster_name, cluster_alias, profile)
	except SSOSessionError:
		sso_login(f'login-{region}')


def main():
	parser = argparse.ArgumentParser(
		prog = 'klogin',
		description = 'Log in to GenuityScience kubernetes clusters',
		epilog = 'Example usage:\nklogin -c=/home/user/myklogin.yml platform-dev admin',
		formatter_class=RawDescriptionHelpFormatter
	)
	parser.add_argument('-c', '--config', nargs='?', default='~/klogin.yml')
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
	parser.add_argument("second", nargs='?', help='<role>/<command>')
	args = parser.parse_args()
	print(f"args: {args}")
	# if no arguments are provided we exit and show the help message
	if len(sys.argv) == 1:
		parser.print_help(sys.stderr)
		sys.exit(1)
	config = load_config(args.config)
	#write_profiles(config)
	if args.first in ['profile', 'profiles']:
		manage_profiles(args.second)
	else:
		cluster_alias = args.first
		role = args.second or 'ro'
		# construct the profile name, <clustername>-<rolename>
		# for cluster platform-dev and role admin: platform-dev-admin 
		# for cluster gor-dev and role ro: gor-dev-ro
		profile = f'{cluster_alias}-{role}'
		if config:
			cluster_name = config['clusters'][cluster_alias]['name']
			region = config['clusters'][cluster_alias]['region']
		else:
			cluster_name = cluster_alias + '-eks-cluster'
			region = args.region
		login(cluster_name, cluster_alias, profile, region)


if __name__ == '__main__':
	main()
