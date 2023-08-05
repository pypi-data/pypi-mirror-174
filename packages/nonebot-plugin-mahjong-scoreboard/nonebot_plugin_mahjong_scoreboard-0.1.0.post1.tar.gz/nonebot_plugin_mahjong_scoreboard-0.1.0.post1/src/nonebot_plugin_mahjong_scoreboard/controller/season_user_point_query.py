from nonebot import on_command
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Bot
from nonebot.internal.matcher import Matcher

from nonebot_plugin_mahjong_scoreboard.controller.general_handlers import require_unary_at
from nonebot_plugin_mahjong_scoreboard.controller.interceptor import general_interceptor
from nonebot_plugin_mahjong_scoreboard.controller.mapper.season_user_point_mapper import map_season_user_point, \
    map_season_user_points
from nonebot_plugin_mahjong_scoreboard.controller.utils import send_group_forward_msg
from nonebot_plugin_mahjong_scoreboard.errors import BadRequestError
from nonebot_plugin_mahjong_scoreboard.service import season_user_point_service
from nonebot_plugin_mahjong_scoreboard.service.group_service import get_group_by_binding_qq
from nonebot_plugin_mahjong_scoreboard.service.season_service import get_season_by_id
from nonebot_plugin_mahjong_scoreboard.service.season_user_point_service import get_season_user_point_rank, \
    count_season_user_point
from nonebot_plugin_mahjong_scoreboard.service.user_service import get_user_by_binding_qq

# ========== 查询PT ==========
query_season_point = on_command("查询PT", aliases={"查询pt", "PT", "pt"}, priority=5)

require_unary_at(query_season_point, "user_id",
                 decorator=general_interceptor(query_season_point))


@query_season_point.handle()
@general_interceptor(query_season_point)
async def query_season_point(event: GroupMessageEvent, matcher: Matcher):
    user_id = matcher.state.get("user_id", event.user_id)

    group = await get_group_by_binding_qq(event.group_id)
    user = await get_user_by_binding_qq(user_id)

    if group.running_season_id is not None:
        season = await get_season_by_id(group.running_season_id)
        sup = await season_user_point_service.get_season_user_point(season, user)
        if sup is None:
            raise BadRequestError("你还没有参加过对局")

        rank = await get_season_user_point_rank(sup)
        total = await count_season_user_point(season)

        msg = await map_season_user_point(sup, rank, total)
        await matcher.send(msg)
    else:
        raise BadRequestError("当前没有运行中的赛季")


# ========== 查询榜单 ==========
query_season_ranking = on_command("查询榜单", aliases={"榜单"}, priority=5)


@query_season_ranking.handle()
@general_interceptor(query_season_ranking)
async def query_season_ranking(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    group = await get_group_by_binding_qq(event.group_id)

    if group.running_season_id is not None:
        season = await get_season_by_id(group.running_season_id)
        sups = await season_user_point_service.get_season_user_points(season)

        msgs = await map_season_user_points(season, sups)
        if len(msgs) == 1:
            await matcher.send(msgs[0])
        else:
            await send_group_forward_msg(bot, event.group_id, msgs)
    else:
        raise BadRequestError("当前没有运行中的赛季")
