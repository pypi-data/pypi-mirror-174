import requests
from .get_header import get_simple_header
from .config import read

async def Tag_Search(tag) -> dict:
    '''
    传入需要搜索的tag，返回列表
    '''
    token = read('account')['token']
    if token:
        url = f'https://pix.ipv4.host/illustrations?keyword={tag}&page=1&pageSize=16&searchType=original&illustType=illust&minWidth=1280&minHeight=720&xRestrict=0'
        headers = get_simple_header()
        headers['authorization'] = token
        res_json = requests.get(url, headers=headers)
        if res_json.status_code == 200:
            return res_json.json().get("data"), 'pixivic'
        if res_json.status_code != 200:
            token_overdue = True
    if not token or token_overdue == True:
        result = dict(requests.get(url = f"https://api.lolicon.app/setu/v2?size=original&tag={tag}&num=20").json())
        if not result.get("error"):
            return result.get("data"), 'lolicon'

async def Search_Artist(artistId):
    res_json = requests.get(f'https://pix.ipv4.host/artists/{artistId}')
    if res_json.status_code == 200:
        return res_json.json().get("data")