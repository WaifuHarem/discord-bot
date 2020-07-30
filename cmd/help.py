from cmd_core import CmdCore
from cmd_proc import CmdProc


@CmdCore.metadata(
    perm = CmdCore.PERMISSION_PUBLIC,
    info = 'Prints help text',
    args = {
        'cmd' : CmdCore.arg(str, CmdCore.OPTIONAL, 'Command to get help for')
    }
)
async def help(msg, logger, **kargs):
    cmd_name = kargs['cmd'] if 'cmd' in kargs else None
    if cmd_name == None:
        await msg.channel.send('TODO: Help text')
        return

    await msg.channel.send(CmdProc.get_help(cmd_name))
    CmdCore.ok()