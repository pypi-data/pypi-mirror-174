#!/usr/local/bin/python
# coding: utf-8

import sys
from neolabci.version import __version__
from neolabci.report_app import ReportApplication
from neolabci.commands.run_finish import RunFinishCommand
from neolabci.commands.run_report import RunReportCommand
from neolabci.commands.run_test import RunTestCommand
from neolabci.commands.init_template import InitTemplateCommand
from neolabci.commands.run_all import RunAllCommand
from neolabci.commands.check_config import CheckConfigCommand
from neolabci.commands.show_config import ShowConfigCommand
from neolabci.commands.run_notify import RunNotifyCommand
from neolabci.commands.test_connect import TestConnectCommand
from neolabci.commands.run_upload import RunUploadCommand

YAML_CONFIGURE_FILE = '.neolab-ci.yml'
RESULT_TEMP_FILE = '.neolab-ci-result.temp.yml'

COMMANDS = [
    RunTestCommand, RunReportCommand, RunFinishCommand, InitTemplateCommand,
    CheckConfigCommand, ShowConfigCommand, RunAllCommand, RunNotifyCommand,
    TestConnectCommand, RunUploadCommand
]

def main():
    print('Neolab CI Report Tool', __version__)
    app = ReportApplication()
    app.config(YAML_CONFIGURE_FILE, RESULT_TEMP_FILE)
    for command in COMMANDS:
        app.register_command(command)
    app.run()
    sys.exit(0)

if __name__ == '__main__':
    main()
