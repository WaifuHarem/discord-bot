import discord

from config import bot_owner_id


class Cmd():

    """
    Command core


    """

    PERM_BOT_OWNER        = None
    PERM_PUBLIC           = discord.Permissions(0)     # Anyone can use this command
    PERM_INVITE           = discord.Permissions(create_instant_invite=True)
    PERM_KICK             = discord.Permissions(kick_members=True)
    PERM_BAN              = discord.Permissions(ban_members=True)
    PERM_ADMIN            = discord.Permissions(administrator=True)
    PERM_MANAGE_CHANNELS  = discord.Permissions(manage_channels=True)
    PERM_MANAGE_SERVER    = discord.Permissions(manage_guild=True)
    PERM_ADD_REACTIONS    = discord.Permissions(add_reactions=True)
    PERM_VIEW_AUDIT       = discord.Permissions(view_audit_log=True)
    PERM_PRIORITY_SPEAKER = discord.Permissions(priority_speaker=True)
    PERM_STREAM           = discord.Permissions(stream=True)
    PERM_READ_MSG         = discord.Permissions(read_messages=True)
    PERM_SEND_MSG         = discord.Permissions(send_messages=True)
    PERM_TTS_MSG          = discord.Permissions(send_tts_messages=True)
    PERM_MANAGE_MSG       = discord.Permissions(manage_messages=True)
    PERM_EMBED_LINKS      = discord.Permissions(embed_links=True)
    PERM_ATTACH_FILES     = discord.Permissions(attach_files=True)
    PERM_READ_MSG_HISTORY = discord.Permissions(read_message_history=True)
    PERM_MENTION_EVERYONE = discord.Permissions(mention_everyone=True)
    PERM_EXTERNAL_EMOJI   = discord.Permissions(external_emojis=True)
    PERM_SERVER_STATS     = discord.Permissions(view_guild_insights=True)
    PERM_CONNECT_VOICE    = discord.Permissions(connect=True)
    PERM_SPEAK_VOICE      = discord.Permissions(speak=True)
    PERM_MUTE_USERS       = discord.Permissions(mute_members=True)
    PERM_DEFEAN_USERS     = discord.Permissions(deafen_members=True)
    PERM_MOVE_USERS       = discord.Permissions(move_members=True)
    PERM_VOICE_ACTIVATION = discord.Permissions(use_voice_activation=True)
    PERM_CHANGE_NICKNAME  = discord.Permissions(change_nickname=True)
    PERM_MANAGE_NICKNAMES = discord.Permissions(manage_nicknames=True)
    PERM_MANAGE_ROLES     = discord.Permissions(manage_roles=True)
    PERM_MANAGE_WEBHOOKS  = discord.Permissions(manage_webhooks=True)
    PERM_MANAGE_EMOJI     = discord.Permissions(manage_emojis=True)

    OPTIONAL = True
    REQUIRED = False

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
    def has_permissions(perms: list, msg: discord.Message):
        if type(perms) != list: perms = [ perms ]
        user_perm = msg.author.permissions_in(msg.channel)

        for perm in perms:
            if perm['id'] == Cmd.PERM_BOT_OWNER:
                if msg.author.id != bot_owner_id:
                    return False
                continue

            if not user_perm.is_superset(perm['id']):
                return False

        return True


    @staticmethod
    def perm_str(perms: list):
        return ','.join([ perm['str'] for perm in perms ])



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



    class perm():

        BOT_OWNER = {
            'id'  : None,
            'str' : 'Bot owner'
        }

        PUBLIC = {
            'id'  : discord.Permissions(0),
            'str' : 'Public'
        }

        INVITE = {
            'id'  : discord.Permissions(create_instant_invite=True),
            'str' : 'Invite'
        }
        
        KICK = {
            'id'  : discord.Permissions(kick_members=True),
            'str' : 'Kick'
        }

        BAN = {
            'id'  : discord.Permissions(ban_members=True),
            'str' : 'Ban'
        }

        ADMIN = {
            'id'  : discord.Permissions(administrator=True),
            'str' : 'Admin'
        }

        MANAGE_CHANNELS = {
            'id'  : discord.Permissions(manage_channels=True),
            'str' : 'Manage channels'
        }

        MANAGE_SERVER = {
            'id'  : discord.Permissions(manage_guild=True),
            'str' : 'Manage server'
        }

        ADD_REACTIONS = {
            'id'  : discord.Permissions(add_reactions=True),
            'str' : 'Add reactions'
        }

        VIEW_AUDIT = {
            'id'  : discord.Permissions(view_audit_log=True),
            'str' : 'View audit'
        }

        PRIORITY_SPEAKER = {
            'id'  : discord.Permissions(priority_speaker=True),
            'str' : 'Priority speaker'
        }

        STREAM = {
            'id'  : discord.Permissions(stream=True),
            'str' : 'Stream'
        }

        READ_MSG = {
            'id'  : discord.Permissions(read_messages=True),
            'str' : 'Read messages'
        }

        SEND_MSG = {
            'id'  : discord.Permissions(send_messages=True),
            'str' : 'Send messages'
        }

        TTS_MSG = {
            'id'  : discord.Permissions(send_tts_messages=True),
            'str' : 'Send TTS messages'
        }

        MANAGE_MSG = {
            'id'  : discord.Permissions(manage_messages=True),
            'str' : 'Manage messages'
        }

        EMBED_LINKS = {
            'id'  : discord.Permissions(embed_links=True),
            'str' : 'Embed links'
        }

        ATTACH_FILES = {
            'id'  : discord.Permissions(attach_files=True),
            'str' : 'Attach files'
        }

        READ_MSG_HISTORY = {
            'id'  : discord.Permissions(read_message_history=True),
            'str' : 'Read message history'
        }

        MENTION_EVERYONE = {
            'id'  : discord.Permissions(mention_everyone=True),
            'str' : 'Mention everyone'
        }

        EXTERNAL_EMOJI = {
            'id'  : discord.Permissions(external_emojis=True),
            'str' : 'External emojis'
        }

        SERVER_STATS = {
            'id'  : discord.Permissions(view_guild_insights=True),
            'str' : 'View server insights'
        }

        CONNECT_VOICE = {
            'id'  : discord.Permissions(connect=True),
            'str' : 'Connect to voice'
        }

        SPEAK_VOICE = {
            'id'  : discord.Permissions(speak=True),
            'str' : 'Speak in voice'
        }

        MUTE_USERS = {
            'id'  : discord.Permissions(mute_members=True),
            'str' : 'Mute users'
        }

        DEFEAN_USERS = {
            'id'  : discord.Permissions(deafen_members=True),
            'str' : 'Defean users'
        }

        MOVE_USERS = {
            'id'  : discord.Permissions(move_members=True),
            'str' : 'Move users'
        }

        VOICE_ACTIVATION = {
            'id'  : discord.Permissions(use_voice_activation=True),
            'str' : 'Use voice activation'
        }

        CHANGE_NICKNAME  = {
            'id'  : discord.Permissions(change_nickname=True),
            'str' : 'Change nickname'
        }

        MANAGE_NICKNAMES = {
            'id'  : discord.Permissions(manage_nicknames=True),
            'str' : 'Manage nicknames'
        }

        MANAGE_ROLES = {
            'id'  : discord.Permissions(manage_roles=True),
            'str' : 'Manage roles'
        }

        MANAGE_WEBHOOKS = {
            'id'  : discord.Permissions(manage_webhooks=True),
            'str' : 'Manage webhooks'
        }

        MANAGE_EMOJI = {
            'id'  : discord.Permissions(manage_emojis=True),
            'str' : 'Manage emoji'
        }