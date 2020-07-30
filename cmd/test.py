from cmd_core import CmdCore
from db_client import DbClient



@CmdCore.metadata(
    perm = CmdCore.PERMISSION_ADMIN,
    info = 'Test command and an example',
    args = {
        'str'   : CmdCore.arg(str, CmdCore.OPTIONAL, 'Optional str arg'),
        'int'   : CmdCore.arg(int, CmdCore.REQUIRED, 'Required int arg'),
        'float' : CmdCore.arg(int, CmdCore.OPTIONAL, 'Optional float arg'),
    }
)
async def test(msg, logger, **kargs):
    str_arg = kargs['str'] if 'str' in kargs else None
    int_arg = kargs['int']
    float_arg = kargs['float'] if 'float' in kargs else None

    await msg.channel.send(f'str = {str_arg}   int = {int_arg}   float_arg = {float_arg}')

    DbClient.request(DbClient.REQUEST_NOP, msg.author.id, {})

    CmdCore.ok()