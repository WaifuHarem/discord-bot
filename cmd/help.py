from cmd_core import CmdCore



@CmdCore.metadata(
    perm = CmdCore.PERMISSION_PUBLIC,
    info = 'Prints help text',
    args = {
    }
)
async def help(msg, logger, **kargs):
    await msg.channel.send('TODO')
    CmdCore.ok()