import os
import time
import logging
import importlib
import re, string
import inspect

import config
from cmd_core import CmdCore


        
class CmdProc():
    """
    Command Processor


    """

    init_done = False
    logger    = logging.getLogger('bot.cmd')
    cmd_dict  = {}

    @staticmethod
    def init():
        if CmdProc.init_done:
            return

        # Load commands
        CmdProc.logger.info('Loading bot commands...')
        CmdProc.load_commands()

        CmdProc.init_done = True


    @staticmethod
    def load_commands():
        CmdProc.logger.info('Loading commands...')

        if not os.path.exists('cmd/'):
            raise Exception('cmd directory doesn\'t exist!')

        cmds = []

        # Get a list of files to import
        for root, dirs, files in os.walk('cmd/'):
            cmds += list([file[:-3] for file in files if file != '__init__.py' and file[-3:] == '.py'])
            CmdProc.logger.info(f'Commands found: {cmds}')

        for cmd in cmds:
            # Import command
            CmdProc.logger.info(f'Importing cmd.{cmd}')
            
            try: module = importlib.import_module(f'cmd.{cmd}')
            except ModuleNotFoundError as e:
                error_msg = f'Cannot load module for command: {cmd}; {e}'
                CmdProc.logger.critical(error_msg)
                raise Exception(CmdProc.logger, error_msg)

            # Load command
            try: CmdProc.cmd_dict[cmd] = getattr(module, cmd)
            except Exception as e:
                error_msg = f'Cannot load command from module: {module}; {e}'
                CmdProc.logger.critical(error_msg)
                raise Exception(CmdProc.logger, error_msg)

        CmdProc.logger.info('Running bot post initialization routines.')


    @staticmethod
    def parse_cmd(cmd):
        cmd_token = '>>'

        # All commands start with a token
        if not cmd.startswith(cmd_token):
            return

        # All commands have a name followed by the token
        try: args = cmd.split(cmd_token)[1]
        except IndexError:
            return

        if not args:
            return

        # Check if command exists
        cmd_name = args.split(' ')[0]
        if cmd_name not in CmdProc.cmd_dict:
            return

        cmd_data = {
            'name' : cmd_name,
            'params' : {       
            }
        }

        # Parse args
        # Note: This has a behavior of skipping anything prior to the first flag
        args = args.split('-')[1:]
        for arg in args:
            params = arg.strip().split(' ')
            flag = params[0].strip()

            cmd_data['params'][flag] = []
            for param in params[1:]:
                cmd_data['params'][flag].append(param)

            # If there is one thing in the list, there is no need for a list
            if len(cmd_data['params'][flag]) == 1:
                cmd_data['params'][flag] = cmd_data['params'][flag][0]

        return cmd_data


    @staticmethod
    async def exec_cmd(cmd_data, msg):
        cmd_name = cmd_data['name']
        uid = msg.author.id

        CmdProc.logger.info(f'uid: {uid}; cmd: {cmd_data["name"]} {cmd_data["params"]}')
        
        # Get called command data
        func = CmdProc.cmd_dict[cmd_data['name']]['exec']
        perm = CmdProc.cmd_dict[cmd_data['name']]['perm']
        args = CmdProc.cmd_dict[cmd_data['name']]['args']

        # Check if user has sufficient permissions to use function
        #if perm > CmdCore.PERMISSION_PUBLIC:
            #if not CmdCore.has_permissions(perm, uid):
            #    return CmdCore.err(f'Insufficient permissions (Permission level {perm})')
        # TODO

        # Check if all required params are included
        req_args = [ arg_name for (arg_name, arg_data) in args.items() if not arg_data.is_optional ]
        for req_arg in req_args:
            if not req_arg in cmd_data['params']:
                await msg.channel.send(f'Missing required arg: {req_arg}')
                return

        # Validate params
        for param_name, param_value in cmd_data['params'].items():
            # Check if param exists in the command
            if param_name not in args:
                await msg.channel.send(f'Command has no -{param_name} arg')
                return
            
            # Check if all provided params match expected type
            type_match = False
            for param_type in args[param_name].var_types:
                try: param_type(param_value)
                except: 
                    print(param_value)
                    continue
                else:
                    type_match = True
                    break

            if not type_match:
                accepted_types = [ var_type.__name__ for var_type in args[param_name].var_types ]
                await msg.channel.send(f'-{param_name} has wrong arg type. Accepted types: {accepted_types}')
                return

        # Build kargs
        ret = await func(msg, CmdProc.logger, **cmd_data['params'])
        if ret == None:
            CmdProc.logger.warn(f'Command "{cmd_data["name"]}" returned a None value. Please make it return a CmdCore.ok or CmdCore.err')
            return

        if ret['status'] == -1:
            msg.channel.send(f'Error executing command: {ret["msg"]}')
            return


    @staticmethod
    def get_help(cmd_name):
        if cmd_name not in CmdProc.cmd_dict:
            return 'Command not found'

        return CmdProc.cmd_dict[cmd_name]['help']()