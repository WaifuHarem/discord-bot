from cmd_core import Cmd
from db_client import DbClient



@Cmd.metadata(
    perm = [
        Cmd.perm.MANAGE_ROLES
    ],
    info = '',
    args = {
    }
)
async def silence(msg, logger, **kargs):

    return Cmd.ok()