

class Cmd():

    """
    Command core


    """

    PERMISSION_PUBLIC  = 0  # Anyone can use this command
    PERMISSION_SPECIAL = 1  # Special roles can use this command + mod + admin
    PERMISSION_MOD     = 2  # Mods roles can use this command + admin
    PERMISSION_ADMIN   = 3  # Only admin is able to use this command

    OPTIONAL = True
    REQUIRED = False

    def __init__(self, logger, obj):
        self.logger = logger
        self.obj    = obj


    def get_cmd_dict(self, prefix='', require_help=True):
        cmd_dict = { attr.replace('cmd_', prefix) : getattr(self, attr)
            for attr in dir(self) 
            if attr.startswith('cmd_') and hasattr(self, attr) 
        }

        if require_help:
            for cmd_name in list(cmd_dict):
                if not type(cmd_dict[cmd_name]) == dict:
                    self.logger.warning('\tCommand "' + str(cmd_name) + '" does not have a help entry; Skipping...')
                    del cmd_dict[cmd_name]
                    continue

                if not cmd_dict[cmd_name]['help']:
                    self.logger.warning('\tCommand "' + str(cmd_name) + '" does not have a valid help entry (missing "help"); Skipping...')
                    del cmd_dict[cmd_name]
                    continue

                if not cmd_dict[cmd_name]['exec']:
                    self.logger.warning('\tCommand "' + str(cmd_name) + '" does not have a valid help entry (missing "exec"); Skipping...')
                    del cmd_dict[cmd_name]
                    continue

        return cmd_dict


    @staticmethod
    def ok(msg=None):
        if msg == None: return { 'status' : 0 }
        else:           return { 'status' : 0, 'msg' : msg }


    @staticmethod
    def err(msg=None):
        if msg == None: return { 'status' : -1 }
        else:           return { 'status' : -1, 'msg' : msg }


    @staticmethod
    def get(kargs, param, default=None):
        return kargs[param] if param in kargs else default


    @staticmethod
    def has_permissions(perm, uid):
        error_msg = 'Command \'permisions\' not implemented'
        #self.logger.error(error_msg)
        raise NotImplementedError(error_msg)


    def cmd_about(self):
        error_msg = 'Command \'about\' not implemented'
        self.logger.error(error_msg)
        raise NotImplementedError(error_msg)


    def get_bot_moderators(self):
        error_msg = '\'get_bot_moderators\' not implemented'
        self.logger.error(error_msg)
        raise NotImplementedError(error_msg)


    def validate_special_perm(self, requestor_id, args):
        error_msg = '\'validate_special\' not implemented'
        self.logger.error(error_msg)
        raise NotImplementedError(error_msg)


    def validate_request(self, cmd_key, args=()):
        perm, requestor_id = cmd_key

        # Check against bot owner
        if requestor_id == admin_user_id: return True
        if perm > CmdCore.PERMISSION_MOD: return False

        # Check against moderator
        bot_moderator_ids = self.get_bot_moderators()
        if requestor_id in bot_moderator_ids: return True
        if perm > CmdCore.PERMISSION_SPECIAL: return False

        # Check against special role
        if self.validate_special_perm(requestor_id, args): return True
        if perm > CmdCore.PERMISSION_PUBLIC: return False
        return True



    class arg():

        def __init__(self, var_types, is_optional, info):
            self.var_types = [ var_types ] if type(var_types) != list else var_types
            self.is_optional = is_optional
            self.info = info


        def arg_text(self):
            opt_text  = '(optional)' if self.is_optional else ''
            var_types = ','.join([ var_type.__name__ for var_type in self.var_types ])
            return f'{var_types} {opt_text} |  {self.info}'



    class metadata():

        def __init__(self, perm=0, info=None, args=None):
            self.info = info
            self.args = args
            self.help = { 
                'info' : self.info, 
                'args' : { name : arg.arg_text() for (name, arg) in self.args.items() }
            }
            self.perm = perm


        def __call__(self, func, *args, **kwargs):
            return { 'perm' : self.perm, 'help' : self.gen_cmd_help, 'args' : self.args, 'exec' : func }

        
        def gen_cmd_help(self):
            args = zip(self.help['args'].keys(), self.help['args'].values())
            args = [ ' : '.join(arg) for arg in args ]

            msg = self.info
            if len(args) > 0: msg += '\n\nargs:' + '\n\t' + '\n\t'.join(args)
            else:             msg += '\n\nargs: None'
            
            return msg