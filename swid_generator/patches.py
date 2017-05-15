

import subprocess
import inspect


def py26_check_output(*popenargs, **kwargs):
    """
    This function is an ugly hack to monkey patch the backported `check_output`
    method into the subprocess module.

    Taken from https://gist.github.com/edufelipe/1027906.

    """
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get('args')
        if cmd is None:
            cmd = popenargs[0]
        error = subprocess.CalledProcessError(retcode, cmd)
        error.output = output
        raise error
    return output

"""
def unicode(*popenargs, **kwargs):

    all_builtin_classes = inspect.getmembers(builtins, inspect.isclass)

    unicode_declaration = [cls for class_member in ]
    # Python 2.6 compatibility
    if 'unicode' not in dir(subprocess):
        # Ugly monkey patching hack ahead
        subprocess.check_output = py26_check_output
"""