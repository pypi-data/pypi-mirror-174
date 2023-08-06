from typing import Any, List
from .object import Object
import datetime


class Resource(Object):
    def __init__(self, **kwargs) -> Any:
        self.title = kwargs.get('title')
        self.alias = kwargs.get('alias') or ''
        self.level = kwargs.get('level')
        self.id = kwargs.get('id')
        self.hot = kwargs.get('hot')
        self.category = kwargs.get('category')
        self.genre = kwargs.get('genre')
        self.year = kwargs.get('year')
        self.episode = kwargs.get('episode')
        self.director = kwargs.get('director')
        self.actor = kwargs.get('actor')
        self.creator_type_str = kwargs.get('creator_type_str')
        self.str1 = kwargs.get('str1')


class Title(Object):
    def __init__(self, caption: str, resource: List[Resource]) -> Any:
        self.caption = caption
        self.resource = resource

    


class Cover(Object):
    def __init__(self, **kwargs) -> None:
        self.id = kwargs.get('id')
        self.src = kwargs.get('src')
        self.url = kwargs.get('url') or ''
        self.key = kwargs.get('key') or ''
        self.sign = kwargs.get('sign') or ''
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.size = kwargs.get('size')
        uploadTime = kwargs.get('uploadTime')
        if(uploadTime):
            self.uploadTime = datetime.datetime.strptime(
                uploadTime, '%Y-%m-%dT%H:%M:%S.%fZ')+datetime.timedelta(hours=8)
        else:
            self.uploadTime = None
            
    def in20hour(self):
        if(not self.uploadTime):
            return False
        else:
            return self.uploadTime > datetime.datetime.now()-datetime.timedelta(hours=20)


class Video(Object):
    _id: str
    name: str
    category: str
    md5: str
    src: str
    status: str
    width: int
    height: int
    duration: float
    size: int
    url: str
    key: str
    hash: str
    rate: int
    ext: str
    sign: str
    childStatus: str
    title: Title
    covers: List[Cover]

    def __init__(self, **kwargs) -> None:
        self._id = kwargs.get('_id')
        self.name = kwargs.get('name')
        self.category = kwargs.get('category')
        self.md5 = kwargs.get('md5')
        self.src = kwargs.get('src')
        self.status = kwargs.get('status')
        self.width = kwargs.get('width')
        self.height = kwargs.get('height')
        self.duration = kwargs.get('duration')
        self.size = kwargs.get('size')
        self.url = kwargs.get('url')
        self.key = kwargs.get('key')
        self.hash = kwargs.get('hash')
        self.rate = kwargs.get('rate')
        self.ext = kwargs.get('ext')
        self.sign = kwargs.get('sign')
        self.childStatus = kwargs.get('childStatus')
        self.title = Title(**kwargs.get('title'))
        self.covers = [Cover(**c) for c in kwargs.get('covers')]
        uploadTime = kwargs.get('uploadTime')
        if(uploadTime):
            self.uploadTime = datetime.datetime.strptime(
                uploadTime, '%Y-%m-%dT%H:%M:%S.%fZ')+datetime.timedelta(hours=8)
        else:
            self.uploadTime = None
            
    def in20hour(self):
        if(not self.uploadTime):
            return False
        else:
            return self.uploadTime > datetime.datetime.now()-datetime.timedelta(hours=20)
