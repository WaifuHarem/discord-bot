from cmd_core import Cmd
from db_client import DbClient



@Cmd.metadata(
    perm = [
        Cmd.perm.BOT_OWNER
    ],
    info = 'Test command and an example',
    args = {
        'str'   : Cmd.arg(str, Cmd.OPTIONAL, 'Optional str arg'),
        'int'   : Cmd.arg(int, Cmd.REQUIRED, 'Required int arg'),
        'float' : Cmd.arg(int, Cmd.OPTIONAL, 'Optional float arg'),
    }
)
async def test(msg, logger, **kargs):
    str_arg = Cmd.get(kargs, 'str')
    int_arg = Cmd.get(kargs, 'int')
    float_arg = Cmd.get(kargs, 'float')

    await msg.channel.send(f'str = {str_arg}   int = {int_arg}   float_arg = {float_arg}')

    DbClient.request(DbClient.REQUEST_NOP, msg.author.id, {})

    return Cmd.ok()