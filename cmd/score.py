from cmd_core import Cmd



@Cmd.metadata(
    perm = Cmd.PERM_PUBLIC,
    info = '',
    args = {
    }
)
async def score(msg, logger, **kargs):
    pass
    return Cmd.ok()