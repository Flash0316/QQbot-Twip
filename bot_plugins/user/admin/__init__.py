import json
import random
from typing import Tuple

from bot_config import GROUP_USE, ban_suer_id
from nonebot import (CommandSession, MessageSegment, NoticeSession,
                     RequestSession, get_bot, on_command, on_notice,
                     on_request)
from nonebot import permission as perm
from nonebot.permission import *
from .db import *


@on_command('admin_search', aliases=('开发者模式-搜索'), permission=perm.SUPERUSER, only_to_me=False)
async def admin_search(session: CommandSession):
    sql = str(session.get('name', prompt='请输入你想执行的搜索类SQL'))
    try:
        msg = str(sql_dql(sql))
    except:
        msg = f"[Syntax Error]"
    await session.send(msg)


@on_command('admin_update', aliases=('开发者模式-修改'), permission=perm.SUPERUSER, only_to_me=False)
async def admin_update(session: CommandSession):
    sql = str(session.get('name', prompt='请输入你想执行的执行类SQL'))
    try:
        msg = str(sql_dml(sql))
    except:
        msg = f"[Syntax Error]"
    await session.send(msg)