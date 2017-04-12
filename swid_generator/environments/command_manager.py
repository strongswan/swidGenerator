
import subprocess
import os


class CommandManager(object):

    @staticmethod
    def run_command(command_argumentlist):
        with open(os.devnull, 'w') as devnull:
            subprocess.call(command_argumentlist, stderr=devnull)

    @staticmethod
    def run_command_check_output(command_argumentlist):
        output = subprocess.check_output(command_argumentlist)

        if isinstance(output, bytes):
            output = output.decode('utf-8')
        return output
