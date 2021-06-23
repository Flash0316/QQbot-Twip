import json
#import random
#from random import randint

import nonebot
from nonebot import (CommandSession, MessageSegment, NoticeSession,
                     RequestSession, get_bot, on_command, on_notice,
                     on_request)
from nonebot import permission as perm
from nonebot.permission import *
from bot_config import GROUP_USE


@on_command('参数传递测试', aliases=('参数传递测试'), only_to_me=False, shell_like=True)
async def _(session: CommandSession):
    group_id = str(session.event.group_id)
    if group_id not in GROUP_USE:
        session.finish()
    arrNo1 = str(session.argv[0]).strip()
    # strip()去除首尾空格
    # strip(‘0’)去除首位0字符
    arrNo2 = str(session.argv[1])  # 第二个参数无需使用strip()方法
    session.finish(f'你输入的两个参数分别为\n{arrNo1}\n{arrNo2}')


@on_command('锁定用户', aliases=('锁定用户'), only_to_me=False, shell_like=True)
async def _(session: CommandSession):
    group_id = str(session.event.group_id)
    if group_id not in GROUP_USE:
        session.finish()
    findUseId = str(session.get('key_findUseId', prompt=f'输入你想搜索的用户QQ号'))
    # 获取所有群的信息
    group_list = await session.bot.get_group_list()

    msg = '这个人在以下几个群：\n'
    for group in group_list:
        group_id = str(group['group_id'])
        group_member_list = await session.bot.get_group_member_list(group_id=group_id)
        for item in group_member_list:
            if str(item['user_id']) == findUseId:
                msg +='群名：'+ group['group_name'] + '\n群号：' + str(group['group_id']) + '\n\n'
    msg += '─────────'
    await session.send(at_sender=True, message=f'{msg}')
    
