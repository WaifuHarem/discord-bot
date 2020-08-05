from cmd_core import Cmd



@Cmd.metadata(
    perm = [
        Cmd.perm.ADMIN
    ],
    info = 'Kills the bot',
    args = {
    }
)
async def die(msg, logger, **kargs):
    logger.info('Bot shutting down')
    await msg.channel.send('owh noe')
    exit(0)