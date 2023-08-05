from nonebot.adapters.onebot.v11 import Bot

class Bot_:
    async def send_group_forward_message(
        bot: Bot,
        group_id: int,
        message: list
        ):
        '''发送群转发信息

            参数：
                bot: Bot参数
                group_id: 群号
                message: 经过node后的信息

            注：
                如果需要发送多条消息，请将返回的值加入到列表中同时发送

        '''
        await bot.call_api("send_group_forward_msg", **{"group_id": group_id, "messages": message})

    def node(
        display_name: str, 
        bot_id: int, 
        content: str
        ) -> dict:
        '''构建消息合并转发，需配合send_group_forward_msg/send_private_forward_msg使用

            参数：
                display_name: 合并消息内显示的机器人名称
                bot_id: 机器人的qq号
                content: 要发送的消息

            注：
                如果需要发送多条消息，请将返回的值加入到列表中同时发送
        '''
        return {"type":"node","data":{"name": display_name, "uin": bot_id,"content": content}}