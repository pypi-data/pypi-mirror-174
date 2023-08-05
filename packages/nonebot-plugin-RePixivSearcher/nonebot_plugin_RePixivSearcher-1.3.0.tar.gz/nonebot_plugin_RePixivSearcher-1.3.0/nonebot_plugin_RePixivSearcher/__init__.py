from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.onebot.v11 import Bot, GROUP
from nonebot.matcher import Matcher
from nonebot.adapters.onebot.v11.event import GroupMessageEvent
from nonebot.adapters.onebot.v11.message import Message, MessageSegment
from nonebot.params import CommandArg, ArgPlainText
from .search import Tag_Search, Search_Artist
from .config import write
from .account import GetVervfi, login__
from .MessageSegment_ import Bot_

import random
import os

path = os.getcwd()

if os.path.exists('data/PixivSearcher') == False:
    os.makedirs('data/PixivSearcher')
    write({'username': 'USERNAME', 'password': 'PASSWORD', 'token': None}, 'account')

login = on_command('login', permission=GROUP, rule=to_me(), priority=0, block=True)
@login.handle()
async def handle_first_receive(matcher: Matcher, args: Message = CommandArg()):
    global verifi
    verifi = GetVervfi().verify
    await login.send(MessageSegment.image(f'file:///{path}/data/PixivSearcher/tmp.png'))
    plain_text = args.extract_plain_text()
    if plain_text:
        matcher.set_arg("_login", args)

@login.got("_login", prompt = "请输入上图验证码")
async def handle_login(login_msg: str = ArgPlainText("_login")):
    result = login__(verifi, login_msg)
    await login.finish(result.accountjson)

search_tag = on_command("搜", permission=GROUP, priority=0, block=True)
@search_tag.handle()
async def search_(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    tag = str(arg).split(' ')
    if tag[0] == '':
        await search_tag.finish('你的标签去哪了')
    if tag[0] != '':
        await search_tag.send('正在搜索，请勿多次发送请求')
        img_json, api = await Tag_Search(tag[0])
        if img_json:
            if api == 'lolicon':
                await _lolicon_img_(bot, event, img_json)
            if api == 'pixivic':
                await _pixivic_img(bot, event, img_json)
        if not img_json:
            await search_tag.finish('很抱歉，此标签没有任何可以找到的图片')

async def _pixivic_img(bot: Bot, event: GroupMessageEvent, data):
    '''预处理Pixivic API img信息并发送img信息'''
    img_list = []
    if len(data) > 3:
        num = random.sample(range(0,len(data)-1), 3)# - 返回一个列表 
    if len(data) <= 3 :
        num = [random.randint(0, len(data)-1)]# - 改之前忘记下面循环的是列表了，太SB了
    for i in num:
        tags = []
        image = MessageSegment.image(f"https://px3.rainchan.win/img/small/{data[i]['id']}")
        for t in data[i]['tags']:
            tags.append(f'{t["name"]}({t["translatedName"]})')
        reply_msg = f'图片ID：{data[i]["id"]}\n标题：{data[i]["title"]}\n作者：{data[i]["artistPreView"]["account"]}\n作者Pixiv UID：{data[i]["artistId"]}\n标签：' + ', '.join(tags) + f'\n由于防止图片无法发出，图片为经过压缩的small版本，如需保存请前往下面链接：\nhttps://pixiv.re/{data[i]["id"]}.jpg\n'
        img_list.append(Bot_.node("SDBot", bot.self_id, reply_msg + image))
    try:
        await Bot_.send_group_forward_message(bot, event.group_id, Bot_.node("SDBot", bot.self_id, img_list))
    except Exception as e:
        await bot.send(event, f'发送失败，错误返回：\n{e}')

async def _lolicon_img_(bot: Bot, event: GroupMessageEvent, data):
    '''预处理Lolicon API img信息并发送img信息'''
    img_list = []
    if len(data) > 3:
        num = random.sample(range(0,len(data)-1), 3)# - 返回一个列表 
    if len(data) <= 3 :
        num = [random.randint(0, len(data)-1)]# - 改之前忘记下面循环的是列表了，太SB了
    for i in num:
        image = MessageSegment.image(f"https://px3.rainchan.win/img/small/{data[i]['pid']}")
        reply_msg = f'图片ID：{data[i]["pid"]}\n标题：{data[i]["title"]}\n作者：{data[i]["author"]}\n作者Pixiv UID：{data[i]["uid"]}\n标签：' + ', '.join(data[i]['tags']) + f'\n由于防止图片无法发出，图片为经过压缩的small版本，如需保存请前往下面链接：\nhttps://pixiv.re/{data[i]["pid"]}.jpg\n'
        img_list.append(Bot_.node("SDBot", bot.self_id, reply_msg + image))
    try:
        await Bot_.send_group_forward_message(bot, event.group_id, Bot_.node("SDBot", bot.self_id, img_list))
    except Exception as e:
        await bot.send(event, f'发送失败，错误返回：\n{e}')

_random = on_command('random',aliases={"来份涩图","随机涩图","来一份涩图","来一份二次元图"}, permission=GROUP, priority=3, block=True)
@_random.handle()
async def random_(bot: Bot, event: GroupMessageEvent):
    reply = MessageSegment.reply(event.message_id)
    await _random.send(reply + '正在随机涩图中，请勿多次发送请求')
    img = MessageSegment.image("https://px3.rainchan.win/random")
    try:
        await Bot_.send_group_forward_message(bot, event.group_id, Bot_.node("SDBot", bot.self_id, img))
    except Exception as e:
        await bot.send(event, f'发送失败，错误返回：\n{e}')

SEARCH_ARTIST = on_command('画师',priority=4, block=True, permission=GROUP)
@SEARCH_ARTIST.handle()
async def ARTIST(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    id = str(arg).split(' ')
    if id[0] == '':
        await SEARCH_ARTIST.send(MessageSegment.reply(event.message_id) + '缺少必要参数：画师ID')
    if id[0] != '':
        if len(id) >= 2:
            await SEARCH_ARTIST.send(f'检索到多余参数：{id[1:]}，将忽略')
        try:
            artist_id = int(id[0])
            await SEARCH_ARTIST.send(MessageSegment.reply(event.message_id) + '正在搜索此画师')
            result = await Search_Artist(artist_id)
            if result:
                await SEARCH_ARTIST.finish(MessageSegment.reply(event.message_id) + f'名称：{result["name"]}\n性别：{result["gender"]}\n生日：{result["birthDay"]}\n所在地：{result["region"]}\n画师主页：https://www.pixiv.net/users/{id[0]}')
        except ValueError:
            await SEARCH_ARTIST.finish(MessageSegment.reply(event.message_id) + '您输入的不是一个数字!')