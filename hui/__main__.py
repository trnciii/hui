import sys, traceback
import os

from .home import Home, execute_method
from . import util


def execute(home, cmd):
	if len(cmd)==0: return

	if cmd[0] == 'py':
		code = " ".join(cmd[1:])
		exec('res={}'.format(code), globals(), locals())
		return locals()['res']

	if cmd[0] == 'sh':
		return os.system(' '.join(cmd[1:]))

	elif cmd[0] in ['quit', 'q']:
		exit()

	# util
	elif cmd[0] in util.executable:
		exec('ret = util.{}(*cmd[1:])'.format(cmd[0]), globals(), locals())
		return locals()['ret']

	# device
	elif cmd[0] in home.devices.keys():
		return execute_method(home.devices[cmd[0]], cmd[1:])

	# home
	elif cmd[0] == 'home':
		return execute_method(home, cmd[1:])

	elif cmd[0] in home.executable + home.properties:
		return execute_method(home, cmd)

	# fail
	else:
		return util.terminal_yellow('failed to find device or command.')


def interactive():
	home = Home()
	print(home.status())

	while(True):
		try:
			home.update()

			cmd = input('>>> ').split()
			res = execute(home, cmd)
			if res:
				print(res)

		except Exception:
			print("Exception in user code:")
			print("-"*40)
			traceback.print_exc(file=sys.stdout)
			print("-"*40)

			input('press any key to continue\n')


def main():
	if len(sys.argv)>1:
		print(execute(Home(), sys.argv[1:]))
	else:
		print('running', util.running())
		interactive()


if __name__ == '__main__':
	main()