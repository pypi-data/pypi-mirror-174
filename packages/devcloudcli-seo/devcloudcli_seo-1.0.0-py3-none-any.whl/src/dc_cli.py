#!/usr/bin/env python3 
# Copyright (C) 2018-2021 Intel Corporation
# SPDX-License-Identifier: Apache-2.0
# Author: Karthik Kumaar <karthikx.kumaar@intel.com>

from typing import (
    List,
)
#from . import dc_utils
import dc_utils
import cmd2
import argparse
import os
import sys
from cmd2 import (
    Bg,
    Fg,
    style,
    Cmd,
    Cmd2ArgumentParser,
    CompletionError,
    CompletionItem,
    ansi,
    with_argparser,
)

DC_TOOLS = [ 'app-services','edge-to-cloud-app-services']
DC_COMMANDS = ['install', 'uninstall']
DC_COMMANDS_WE = ['install', 'uninstall', 'enable', 'disable']
APP_COMMANDS = ['start', 'stop', 'restart']

SUB_TOOLS={
  "app-services":['system-telemetry','cluster-telemetry','docker-telemetry','log-analytics','health-check','kubernetes-dashboard'],  
  "edge-to-cloud-app-services":['seo-reference-implementations'],
}

TOOLS={
  "seo-reference-implementations":['telehealth-remote-monitoring','wireless-network-ready-intelligent-traffic-management','wireless-network-ready-pcb-defect-detection'],

}

# List contains service which are having enable and disable scripts
enable_list = ['openvino-dl-workbench', 'sigopt','tekton','argocd',
'dlstreamer','dlstreamer-pipeline-server','dlstreamer-pipeline-zoo','dlstreamer-pipeline-composer',
'audio-event-detection-sample',
'action-recognition-sample','human-pose-estimation-sample','vehicle-pedestrian-tracking-sample','face-detection-classification-sample','gvapython-sample','metadata-publishing-sample']

enable_list_k8s = ['kind','microk8s','minikube','rancher-k3s','rancher-rke2']

class DC(cmd2.Cmd):
    CUSTOM_CATEGORY = 'My Custom Commands'
    def __init__(self):
        super().__init__(
            multiline_commands=['echo'],
            persistent_history_file='cmd2_history.dat',
            startup_script='scripts/startup.txt',
            include_ipy=True,
            allow_cli_args=False,
            silence_startup_script=True
        )
        """"Set up interactive command line interface."""
        # delete unused commands that are baked-into cmd2 and set some options
        del cmd2.Cmd.do_py
        del cmd2.Cmd.do_edit
        del cmd2.Cmd.do_shortcuts
        del cmd2.Cmd.do_run_pyscript
        del cmd2.Cmd.do_run_script
        del cmd2.Cmd.do_ipy
        del cmd2.Cmd.do_history
        #del cmd2.Cmd.do_shell
        #del cmd2.Cmd.do_set
        #del cmd2.Cmd.do_alias
        del cmd2.Cmd.do_macro
        #del cmd2.Cmd.do_quit
        del cmd2.Cmd.do__relative_run_script
        
        cmd2.Cmd.abbrev = True
        self.allow_cli_args = False  # disable parsing of command-line args by cmd2
        self.allow_redirection = False  # disable redirection to enable right shift (>>) in custom_hash to work
        self.redirector = '\xff'  # disable redirection in the parser as well
        #self.shortcuts.update({'sh': 'show'})  # don't want "sh" to trigger the hidden "shell" command

        # init cmd2 and the history file
        #cmd2.Cmd.__init__(self, persistent_history_file=hist_file, persistent_history_length=200)

        # disable help on builtins
        #self.hidden_commands.append('shell')
        self.hidden_commands.append('exit') 
        self.hidden_commands.append('intro')
        self.hidden_commands.append('echo')

        # Prints an intro banner once upon application startup
        self.intro = style('Welcome to Intel Devcloud! \n An Interactive CLI to Install Devcloud tools & Components', fg=Fg.BLUE, bg=Bg.BLACK, bold=True)

        # Show this as the prompt when asking for input
        self.prompt = style('$>',fg=Fg.GREEN, bold=True)

        # Used as prompt for multiline commands after the first line
        self.continuation_prompt = '... '

        # Allow access to your application in py and ipy via self
        self.self_in_py = True

        # Set the default category name
        self.default_category = 'cmd2 Built-in Commands'

        # Color to output text in with echo command
        self.foreground_color = Fg.CYAN.name.lower()

        # Make echo_fg settable at runtime
        fg_colors = [c.name.lower() for c in Fg]
        self.add_settable(
            cmd2.Settable('foreground_color', str, 'Foreground color to use with echo command', self, choices=fg_colors)
        )

        # For Pyinstaller Binary temp folder
        self.bundle_dir = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))
    
    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_intro(self, _):
        """Display the intro banner"""
        self.poutput(self.intro)

    @cmd2.with_category(CUSTOM_CATEGORY)
    def do_echo(self, arg):
        """Example of a multiline command"""
        fg_color = Fg[self.foreground_color.upper()]
        self.poutput(style(arg, fg=fg_color))

    '''
    eval_parser=cmd2.Cmd2ArgumentParser(description='Obtain the eval command')
    eval_parser.add_argument("Dev-Tools",help="Help for Dev-Tools")

    @cmd2.with_argparser(eval_parser)
    '''
    def do_dc(self, statement: cmd2.Statement):
        """Tab completes first 3 arguments using index_based_complete"""
        #dc_utils.aptGet_uninstall("vim")
        #dc_utils.aptGet_install("vim")
        self.poutput("Args: {}".format(statement.args))
        argsList = statement.args.split(' ')        
        print("length of args:", len(argsList))

        
        if len(argsList)>6:
            self.poutput("Invalid Args: {}".format(statement.args))        
            
        if len(argsList) >= 4:
            typeName=argsList[0]
            toolName=argsList[1]
            subtoolName=argsList[2]
            commandName=argsList[3]        
            print("{0} : {1} : {2} : {3}".format(typeName,toolName,subtoolName,commandName))
            print("cd:",os.getcwd())
            installation_path = self.bundle_dir + "/scripts/" + typeName + '/' + toolName + '/' + subtoolName + '/' + commandName
            self.poutput(installation_path)
            # checking the argList if any command line args given after install
            if len(argsList)>4 and len(argsList)<6:
                dc_utils.processArgs(installation_path,serviceName=argsList[4])
            else:
                dc_utils.processArgs(installation_path,serviceName="")
        
        if len(argsList) == 3:
            typeName=argsList[0]
            toolName=argsList[1]
            commandName=argsList[2]        
            print("{0} : {1} : {2}".format(typeName,toolName,commandName))
            print("cd:",os.getcwd())
            installation_path = self.bundle_dir + "/scripts/" + typeName + '/' + toolName + '/' + commandName
            self.poutput(installation_path)
            # checking the argList if any command line args given after install
            if len(argsList)>3 and len(argsList)<5:
                dc_utils.processArgs(installation_path,serviceName=argsList[3])
            else:
                dc_utils.processArgs(installation_path,serviceName="")
                
    def complete_dc(self, text, line, begidx, endidx) -> List[str]:
        """Completion function for do_index_based"""
        SUB_TOOLS_1=[]
        CMD_TOOLS=[]
        TM_TOOLS=[]
        APP_TOOLS=[]
        CMD_TOOLS_WE=[]
        CMD_TOOLS_WE1=[]
        index_dict={}      
        
        if begidx>3:
            for t in SUB_TOOLS:    
                # print("t:",t)            
                if line.__contains__(t):                    
                    SUB_TOOLS_1=SUB_TOOLS[t]
                    # print("subtools:", SUB_TOOLS[t])
                    CMD_TOOLS = DC_COMMANDS
                    if t == "app-services":
                       APP_TOOLS =APP_COMMANDS                

                for st in TOOLS:
                    if line.__contains__(st):
                        #print(TOOLS[st])
                        TM_TOOLS = TOOLS[st] 

            for k8s_t in SUB_TOOLS_1:
                    if line.__contains__(k8s_t):
                        if k8s_t in enable_list_k8s:
                            CMD_TOOLS_WE1 = DC_COMMANDS_WE  
            
            for et in TM_TOOLS: 
                if line.__contains__(et):               
                    if et in enable_list:
                        CMD_TOOLS_WE = DC_COMMANDS_WE                       

        if len(TM_TOOLS) != 0 and len(CMD_TOOLS_WE) == 0:                
            index_dict = {
                1: DC_TOOLS,  # Tab complete food items at index 1 in command line
                2: SUB_TOOLS_1,  # Tab complete sport items at index 2 in command line
                3: TM_TOOLS,
                4: CMD_TOOLS  # Tab complete using path_complete function at index 3 in command line
                 
            }
        elif len(CMD_TOOLS_WE) != 0:                
            index_dict = {
                1: DC_TOOLS,  # Tab complete food items at index 1 in command line
                2: SUB_TOOLS_1,  # Tab complete sport items at index 2 in command line
                3: TM_TOOLS,
                4: CMD_TOOLS_WE  # Tab complete using path_complete function at index 3 in command line
                 
            }
        elif len(APP_TOOLS) != 0:
            index_dict = {
                1: DC_TOOLS,  # Tab complete food items at index 1 in command line
                2: SUB_TOOLS_1,  # Tab complete sport items at index 2 in command line
                3: APP_TOOLS,  # Tab complete using path_complete function at index 3 in command line
                
            }
        elif len(CMD_TOOLS_WE1) != 0:
            index_dict = {
                1: DC_TOOLS,  # Tab complete food items at index 1 in command line
                2: SUB_TOOLS_1,  # Tab complete sport items at index 2 in command line
                3: CMD_TOOLS_WE1,  # Tab complete using path_complete function at index 3 in command line
                
            }
        else:
            # print("Inside else")
            index_dict = {
                1: DC_TOOLS,  # Tab complete food items at index 1 in command line
                2: SUB_TOOLS_1,  # Tab complete sport items at index 2 in command line
                3: CMD_TOOLS,  # Tab complete using path_complete function at index 3 in command line
                
            }

        return self.index_based_complete(text, line, begidx, endidx, index_dict=index_dict)
        #return self.path_complete(text, line, begidx, endidx)
 

def main():
    app = DC()
    app.cmdloop()

if __name__ == "__main__":
   main()



