from cmd_core import Cmd
from cmd_proc import CmdProc


@Cmd.metadata(
    perm = Cmd.PERMISSION_PUBLIC,
    info = 'Prints help text',
    args = {
        'cmd' : Cmd.arg(str, Cmd.OPTIONAL, 'Command to get help for')
    }
)
async def help(msg, logger, **kargs):
    cmd_name = Cmd.get(kargs, 'cmd')
    if cmd_name == None:
        await msg.channel.send('TODO: Help text')
        return

    await msg.channel.send(CmdProc.get_help(cmd_name))
    Cmd.ok()