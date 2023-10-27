#
# Utils for package managment
#

def get_args(cmd_args):
	"""Gets some defined command line args. Should be modular, let's see how it works.
	In:
		> cmd_args (dct) - dict of args with mandatory
		columns "action", "dest", "help", "required", in that order.
	Out:
		> args (*list) - unpacked list of parsed args
	"""
	from argparse import ArgumentParser

	_action, _dest, _help, _required = args.keys()
	parser = argparse.ArgumentParser(
			action=_action,
			dest=_dest,
			help=_help,
			required=_required)
	args = parser.parse_args()

	return *[_arg for _arg in args]
