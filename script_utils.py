#
# Utils for package managment
#
import re
import subprocess

from argparse import ArgumentParser

def get_args(cmd_args, _description=None):
	"""
	Gets & processes some defined command line args. Should be modular, let's see how it works.
	In:
		> cmd_args (list) - list of lists with mandatory
		columns "long" (name), "short" (name), "action", "dest", "help", in that order.
		> _description (str) - optional, a description of the script this function is called in.
	Out:
		> args (list) - list of parsed args
	"""
	parser = ArgumentParser(description=_description)
	dests = []
	for arg in cmd_args:
		_long, _short, _action, _dest, _help = arg
		parser.add_argument(_long, _short,
				action=_action,
				dest=_dest,
				help=_help)
		dests.append(_dest)
	args = parser.parse_args()
	return [getattr(args, dest) for dest in dests]


def get_config(config_file):
	"""
	Gets & processes confid from file if supplied.
	In:
		> config_file (str or path object) - path to config file
	Out:
		> cfgs (list) - a list of parsed config options
	"""
	cfgs = []
	for line in open(config_file, 'r'):
		option = line.strip().split('=')[1].strip()
		try:
			option = eval(option) # Do this to convert 'True' to a Bool
		except:
			pass
		cfgs.append(option)
	return cfgs


def grep_tstamp(run_log_path):
	"""
	Gets time and date from run log of phantom run and returns them as variables.
	In:
		> run_log_path (str or path) - path to run_log file
	Out:
		> time (str) - time string
		> date (str) - date string
	"""
	grep_pattern = r'Run finished on'
	grep_command = ['grep', '-e', grep_pattern, run_log_path]
	result = subprocess.run(grep_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

	if result.stdout:
		re_pattern = r"([0-9]{2}\/[0-9]{2}\/[0-9]{4}) at ([0-9]{2}:[0-9]{2}:[0-9]{2}\.[0-9])"
		match = re.search(re_pattern, result.stdout)
		if match:
			date = match.group(1)
			time = match.group(2)
			return date, time
	else:
		print("Timestamp not found in file, please check your run log.")
		return None, None
