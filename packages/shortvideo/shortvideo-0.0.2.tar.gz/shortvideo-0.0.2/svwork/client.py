import asyncio
import datetime
import configparser
import os
import platform
from typing import Any, List, Tuple

from .method import Method, ainput
from .utils import ainput, idle
from .video import Title, Video, Cover

version = '1.0.0'


class Client(Method):
    appid: str
    appsecret: str
    host: str
    workdir: str

    def __init__(self):
        self.appid = ''
        self.appsecret = ''
        self.host = ''
        self.workdir = 'files'
        self.version = version

    async def query(self, url: str, action: str, **kwargs):
        res = await super().query(url, action, **kwargs)
        if res.code == 401:
            print(res.msg)
            await idle(exit=True)

        return res

    async def transport(self):
        res = await self.query('/api/client', 'video')
        if(res.code == 401):
            return
        if(not res.success or not res.data):
            if res.msg:
                print(res.msg)
                await asyncio.sleep(10)
            elif not res.data:
                seconds = res.data if isinstance(res.data, int) else 10
                next = datetime.datetime.now()+datetime.timedelta(seconds=seconds)
                print(
                    f'\r暂无任务，{seconds}秒后({next.strftime("%H:%M:%S")})将再次读取...', end=' ')
                await asyncio.sleep(seconds)
            else:
                await asyncio.sleep(10)
            return

        app_id = res.data.get('app_id')
        app_token = res.data.get('app_token')
        video = Video(**res.data.get('video'))
        print(f'\n{video.name}')

        file_list = []
        async def down2up_video():
            if video.src and video.in20hour():
                return True

            res = await self.query('/api/client', 'token', app_id=app_id, app_token=app_token, module='upload_video')
            if not res.success:
                print('获取upload_video_token失败')
                return False

            filepath = os.path.join(self.workdir, video.name+'.mp4')
            file_list.append(filepath)

            success = True if os.path.exists(filepath) else await self.download(filepath, video.src, lambda p, s, t: print("\r \t视频下载进度：%d%%(%d/%d)" % (p, s, t), end=" "))
            if not success:
                print('下载失败')
                return False

            url = res.data.get('url')
            key = res.data.get('key')
            token = res.data.get('token')
            res = await self.upload(
                url, key, token, filepath, 'video/mp4',
                lambda p, s, t: print(
                    "\r \t视频上传进度：%d%%(%d/%d)" % (p, s, t), end=" ")
            )

            if res.success:
                video.duration = res.data.get('duration')
                video.ext = res.data.get('ext')
                video.hash = res.data.get('hash')
                video.height = res.data.get('height')
                video.key = res.data.get('key')
                video.rate = res.data.get('rate')
                video.sign = res.data.get('sign')
                video.size = res.data.get('size')
                video.url = res.data.get('url')
                video.width = res.data.get('width')
                await self.query(f'/api/client', 'update', _id=video._id, data=res.data)
                print('完成')
                return True
            else:
                print(f'失败：{res.msg}')
                return False

        async def down2up_cover(c: Cover):
            if c.src and c.in20hour():
                return True

            res = await self.query('/api/client', 'token', app_id=app_id, app_token=app_token, module='upload_cover')
            if not res.success:
                print('获取upload_cover_token失败')
                return False

            filepath = os.path.join(self.workdir, f'{video.name}{c.id}.jpg')
            file_list.append(filepath)

            success = True if os.path.exists(filepath) else await self.download(filepath, c.src, lambda p, s, t: print(f"\r \t封面{c.id}下载进度：%d%%(%d/%d)" % (p, s, t), end=" "))
            if not success:
                print('下载失败')
                return False

            url = res.data.get('url')
            key = res.data.get('key')
            token = res.data.get('token')
            res = await self.upload(
                url, key, token, filepath, 'image/jpeg',
                lambda p, s, t: print(
                    f"\r \t封面{c.id}上传进度：%d%%(%d/%d)" % (p, s, t), end=" ")
            )
            if(res.success):
                c.key = res.data.get('key')
                c.width = res.data.get('width')
                c.height = res.data.get('height')
                c.sign = res.data.get('sign')
                c.url = res.data.get('url')
                await self.query(f'/api/client', 'update', _id=video._id, coverid=c.id, data=res.data)
                print('完成')
                return True
            else:
                print(f'失败：{res.msg}')
                return False

        success = await down2up_video()
        if success:
            for c in video.covers:
                if not await down2up_cover(c):
                    success = False
                    break

        await self.query(f'/api/client', 'update', _id=video._id, data={'childStatus': 'uploaded' if success else 'failure'})
        if success:
            for _path in file_list:
                if os.path.exists(_path):
                    os.remove(_path)

    async def __read_config(self):

        config = configparser.ConfigParser()
        if not os.path.exists("config.ini"):
            config.add_section("settings")
            config.set("settings", "version", version)
            config.set("settings", "host", "http://127.0.0.1:8011")
            config.set("settings", "workdir", "files")
            config.write(open("config.ini", "w"))

        config.read("config.ini")

        def get(name: str, default: Any = ''):
            return config.get('settings', name, fallback=default)

        def set(name: str, value: Any):
            config.set('settings', name, value)

        if(get('version') != self.version):
            set('version', self.version)
            config.write(open("config.ini", "w"))

        self.host = get('host')

        while(True):
            is_save = False
            self.appid = get('appid')
            if not self.appid:
                self.appid = await ainput("请输入AppID：")
                if not self.appid:
                    continue
                set('appid', self.appid)
                is_save = True

            self.appsecret = get('appsecret')
            if not self.appsecret:
                self.appsecret = await ainput("请输入AppSecret：")
                if not self.appsecret:
                    continue
                set('appsecret', self.appsecret)
                is_save = True

            if is_save:
                config.write(open("config.ini", "w"))
            break

    async def start(self):

        await self.__read_config()
        if not os.path.exists(self.workdir):
            os.mkdir(self.workdir)

        async def check():
            res = await self.query('/api/client', 'check')
            if not res.success:
                print(res.msg)
            return res.success

        async def exit():
            pass

        def text():
            sysstr = platform.system()
            os.system('cls' if sysstr == 'Windows' else 'clear')
            options = [
                f'\n短视频工作平台之客户端(版本：{version})\n',
                '1、开始执行任务',
                '2、修改AppSecret',
                f'3、修改服务器地址（{self.host}）',
                '4、退出程序',
                '\n请选择相应操作的序号：'
            ]
            return '\n'.join(options)

        async def show():
            value = await ainput(text())
            while value not in ['1', '2', '3', '4']:
                value = await ainput(text())

            if value == '1':
                print('\n要中断程序，请同时按下 ctrl+c\n')
                await idle(self.transport)

            elif value == '2':
                appSecret = await ainput("请输入新的AppSecret（0则返回）：")
                while not appSecret or len(appSecret) != 32:
                    if appSecret == '0':
                        break
                    if len(appSecret) != 32:
                        print('AppSecret应该是32位长度的字符串')
                    appSecret = await ainput("请输入新的AppSecret（0则返回）：")

                if appSecret != '0':
                    oldValue = self.appsecret
                    self.appsecret = appSecret
                    if await check():
                        config = configparser.ConfigParser()
                        config.read("config.ini")
                        config.set('settings', 'appsecret', appSecret)
                        config.write(open("config.ini", "w"))
                        print('AppSecret修改完成')
                    else:
                        self.appsecret = oldValue
                    await asyncio.sleep(3)

                await show()

            elif value == '3':
                host = await ainput("请输入新的服务器地址（0则返回）：")
                while not host or not host.startswith('http'):
                    if host == '0':
                        break
                    if not host.startswith('http'):
                        print('服务器地址应该以http开头')
                    host = await ainput("请输入新的服务器地址（0则返回）：")

                if host != '0':
                    oldValue = self.host
                    self.host = host
                    if await check():
                        config = configparser.ConfigParser()
                        config.read("config.ini")
                        config.set('settings', 'host', host)
                        config.write(open("config.ini", "w"))
                        print('服务器地址修改完成')
                    else:
                        self.host = oldValue
                    await asyncio.sleep(3)

                await show()

            elif value == '4':
                pass

        await show()
