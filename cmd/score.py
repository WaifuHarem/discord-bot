from cmd_core import CmdCore



@CmdCore.metadata(
    perm = CmdCore.PERMISSION_PUBLIC,
    info = '',
    args = {
    }
)
async def score(msg, logger, **kargs):
    pass
    CmdCore.ok()