
import subprocess
import os


class CommandManager(object):

    @staticmethod
    def run_command(command_argumentlist, working_directory=os.getcwd()):
        """
        Executes a command. No output expected.
        :param command_argumentlist: Command-Arguments
        :param working_directory: The working directory of the command.
        """
        with open(os.devnull, 'w') as devnull:
            subprocess.call(command_argumentlist, stderr=devnull, cwd=working_directory)

    @staticmethod
    def run_command_check_output(command_argumentlist):
        """
        Exectues a command. Output expected.
        :param command_argumentlist: Command-Arguments
        :return: Console-Output of the command.
        """
        output = subprocess.check_output(command_argumentlist)

        if isinstance(output, bytes):
            output = output.decode('utf-8')
        return output
