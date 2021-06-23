from os import path
import nonebot
import bot_config


nonebot.init(bot_config)
# 第一个参数为插件路径，第二个参数为插件前缀（模块的前缀）
nonebot.load_plugins(path.join(path.dirname(__file__), 'bot_plugins'), 'bot_plugins')

# 如果使用 asgi
bot = nonebot.get_bot()
app = bot.asgi

if __name__ == '__main__':
    #nonebot.init(config)
    #nonebot.load_plugins("plugins/sdorica","plugins.sdorica")
    #nonebot.load_plugins("bot_plugins/group","bot_plugins.group")
    # nonebot.load_plugins("bot_plugins/function","bot_plugins.function")
    # nonebot.load_plugins("bot_plugins/helper","bot_plugins.helper")
    # nonebot.load_plugins("bot_plugins/listener","bot_plugins.listener")
    nonebot.load_plugins("bot_plugins/picture","bot_plugins.picture")
    nonebot.load_plugins("bot_plugins/speaker","bot_plugins.speaker")
    nonebot.load_plugins("bot_plugins/user","bot_plugins.user")
    nonebot.run()