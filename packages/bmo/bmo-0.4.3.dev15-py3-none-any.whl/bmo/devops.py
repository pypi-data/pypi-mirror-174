"""
Development Operations.
Main class.
"""

__author__ = "Dilawar Singh"
__email__ = "dilawar@subcom.tech"

import typing as T
import logging
import platform
import bmo.common


class DevOps:
    def __init__(self, system: T.Optional[str] = None, arch: T.Optional[str] = None):
        """Initialize DevOps class.

        Parameters
        ----------
            platform : if not `None` then check if the current platform is the same.
            arch: architecture. If not `None` then check if the current arch is the same.

        """
        super(DevOps, self).__init__()
        self.system = system
        if self.system is not None:
            assert (
                self.system == platform.system()
            ), f"{self.system} and {platform.system()} do not match"

        self.arch = arch
        if self.arch is not None:
            assert (
                self.arch == platform.architecture()
            ), f"{self.arch} != {platform.architecture()}"
        logging.info(f"{self.system}, {self.arch}")

    def run(self, cmd: str):
        """Execute a given command.

        Parameters
        ----------
            cmd : given command. The first word must be the same of executable.
        """
        import subprocess

        command = cmd.split(" ")
        executable = command[0]
        assert (
            bmo.common.find_program(executable) is not None
        ), f"{executable} not found"
        return subprocess.check_call(command)
