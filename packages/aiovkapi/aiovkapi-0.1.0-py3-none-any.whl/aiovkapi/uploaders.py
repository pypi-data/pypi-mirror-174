# Original VKBottle
# https://github.com/vkbottle/vkbottle/tree/bea5e5cd5363e70fbd5b2bd3a1835328502064e4/vkbottle/tools/dev/uploader
# License: https://github.com/vkbottle/vkbottle/blob/bea5e5cd5363e70fbd5b2bd3a1835328502064e4/LICENSE

import abc
import io
import typing

import aiofiles

from . import APIError

if typing.TYPE_CHECKING:
    from .api import API

    Bytes = typing.Union[bytes, io.BytesIO]

__all__ = (
    'AudioUploader',
    'DocWallUploader',
    'DocMessagesUploader',
    'VoiceMessageUploader',
    'GraffitiUploader',
    'PhotoToAlbumUploader',
    'PhotoWallUploader',
    'PhotoFaviconUploader',
    'PhotoMessageUploader',
    'PhotoChatFaviconUploader',
    'PhotoMarketUploader',
    'VideoUploader',
)


class BaseUploader(abc.ABC):

    def __init__(
            self,
            api: "API",
            generate_attachment_strings: bool = True,
            with_name: typing.Optional[str] = None
    ):
        self._api = api
        self.generate_attachment_strings = generate_attachment_strings
        self.with_name = with_name

    @abc.abstractmethod
    async def get_server(self, **kwargs) -> dict:
        pass

    @property
    @abc.abstractmethod
    def attachment_name(self) -> str:
        pass

    async def upload_files(self, upload_url: str, files: dict) -> dict:
        return await self._api.session.post(upload_url, data=files)

    def get_bytes_io(self, data: "Bytes", name: str = None) -> io.BytesIO:
        bytes_io = data if isinstance(data, io.BytesIO) else io.BytesIO(data)
        bytes_io.seek(0)
        bytes_io.name = name or self.attachment_name
        return bytes_io

    async def get_owner_id(self, upload_params: dict) -> int:
        if "group_id" in upload_params:
            return upload_params["group_id"]
        if "user_id" in upload_params:
            return upload_params["user_id"]
        if "owner_id" in upload_params:
            return upload_params["owner_id"]
        try:
            return (await self._api.method("groups.getById"))[0]["id"]
        except APIError:
            return (await self._api.method("users.get"))[0]["id"]

    @staticmethod
    def generate_attachment_string(
            attachment_type: str, owner_id: int, item_id: int, access_key: typing.Optional[str] = None
    ) -> str:
        return f"{attachment_type}{owner_id}_{item_id}{('_' + access_key) if access_key else ''}"

    @staticmethod
    async def read(file_source: typing.Union[str, "Bytes"]) -> "Bytes":
        if isinstance(file_source, str):
            async with aiofiles.open(file_source, "rb") as file:
                return await file.read()
        return file_source

    def __repr__(self) -> str:
        return f"<Uploader {self.__class__.__name__} with api {self._api!r}"


class AudioUploader(BaseUploader):
    NAME = "audio.mp3"

    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("audio.getUploadServer")

    async def upload(
            self, artist: str, title: str, file_source: typing.Union[str, "Bytes"], **params
    ) -> typing.Union[str, dict]:
        server = await self.get_server()
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file})

        audio = (
            await self._api.method(
                "audio.save",
                artist=artist,
                title=title,
                **uploader,
                **params
            )
        )
        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                "audio", await self.get_owner_id(params), audio["id"], audio.get("access_key")
            )
        return audio

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME


class DocUploader(BaseUploader, abc.ABC):
    NAME = "doc.txt"

    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("docs.getUploadServer", **kwargs)

    async def upload(
            self, title: str, file_source: typing.Union[str, "Bytes"], **params
    ) -> typing.Union[str, dict]:
        server = await self.get_server(**params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data, name=title)

        uploader = await self.upload_files(server["upload_url"], {"file": file})

        doc = (
            await self._api.method(
                "docs.save",
                title=title,
                **uploader,
                **params
            )
        )
        doc_type = doc["type"]

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                doc_type,
                doc[doc_type]["owner_id"],
                doc[doc_type]["id"],
                doc[doc_type].get("access_key"),
            )
        return doc

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME


class DocWallUploader(DocUploader):
    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("docs.getWallUploadServer", **kwargs)


class DocMessagesUploader(DocUploader):
    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("docs.getMessagesUploadServer", **kwargs)


class VoiceMessageUploader(DocUploader):
    async def get_server(self, **kwargs) -> dict:
        return await self._api.method(
            "docs.getMessagesUploadServer",
            type="audio_message",
            **kwargs
        )


class GraffitiUploader(DocUploader):
    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("docs.getMessagesUploadServer", type="graffiti", **kwargs)


class PhotoUploader(BaseUploader, abc.ABC):
    NAME = "picture.jpg"

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME


class PhotoToAlbumUploader(PhotoUploader):
    async def upload(
            self,
            album_id: int,
            paths_like: typing.Union[typing.List[typing.Union[str, "Bytes"]], str, "Bytes"],
            **params
    ) -> typing.Union[str, typing.List[typing.Union[str, dict]]]:
        if not isinstance(paths_like, list):
            paths_like = [paths_like]

        server = await self.get_server(album_id=album_id, **params)
        files = {}

        for i, file_source in enumerate(paths_like):
            data = await self.read(file_source)
            files[f"file{i + 1}"] = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], files)
        photos = await self._api.method("photos.save", album_id=album_id, **uploader, **params)

        if self.generate_attachment_strings:
            return [
                self.generate_attachment_string(
                    "photo", photo["owner_id"], photo["id"], photo.get("access_key")
                )
                for photo in photos
            ]
        return photos

    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("photos.getUploadServer", **kwargs)


class PhotoWallUploader(PhotoUploader):
    async def upload(self, file_source: typing.Union[str, "Bytes"], **params) -> typing.Union[str, typing.List[dict]]:
        server = await self.get_server(**params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        photos = await self._api.method("photos.saveWallPhoto", **uploader, **params)

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                "photo", photos[0]["owner_id"], photos[0]["id"], photos[0].get("access_key")
            )
        return photos

    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("photos.getWallUploadServer")


class PhotoFaviconUploader(PhotoUploader):
    async def upload(self, file_source: typing.Union[str, "Bytes"], **params) -> typing.Union[str, dict]:
        owner_id = await self.get_owner_id(params)
        server = await self.get_server(owner_id=owner_id)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        photo = await self._api.method("photos.saveOwnerPhoto", **uploader, **params)

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                "wall", owner_id, photo["post_id"], photo.get("access_key")
            )
        return photo

    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("photos.getOwnerPhotoUploadServer", **kwargs)


class PhotoMessageUploader(PhotoUploader):
    async def upload(self, file_source: typing.Union[str, "Bytes"], **params) -> typing.Union[str, typing.List[dict]]:
        server = await self.get_server(**params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        photo = await self._api.method("photos.saveMessagesPhoto", **uploader, **params)

        if self.generate_attachment_strings:
            return self.generate_attachment_string(
                "photo", photo[0]["owner_id"], photo[0]["id"], photo[0].get("access_key")
            )
        return photo

    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("photos.getMessagesUploadServer", **kwargs)


class PhotoChatFaviconUploader(PhotoUploader):
    async def upload(self, chat_id: int, file_source: typing.Union[str, "Bytes"], **params) -> str:
        server = await self.get_server(chat_id=chat_id, **params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"photo": file})
        return uploader["response"]

    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("photos.getChatUploadServer", **kwargs)


class PhotoMarketUploader(PhotoUploader):
    async def upload(self, file_source: typing.Union[str, "Bytes"], **params) -> dict:
        server = await self.get_server(**params)
        data = await self.read(file_source)
        file = self.get_bytes_io(data)

        uploader = await self.upload_files(server["upload_url"], {"file": file})
        return await self._api.method("photos.saveMarketPhoto", **uploader, **params)

    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("photos.getMarketUploadServer", **kwargs)


class VideoUploader(BaseUploader):
    NAME = "video.mp4"

    @property
    def attachment_name(self) -> str:
        return self.with_name or self.NAME

    async def upload(
            self,
            file_source: typing.Optional[typing.Union[str, "Bytes"]] = None,
            group_id: typing.Optional[int] = None,
            **params,
    ) -> typing.Union[str, typing.List[dict], dict]:
        server = await self.get_server(group_id=group_id)
        assert (
                file_source is not None or "link" in params
        ), "file_source or link to video must be set"

        if "link" in params and not file_source:
            return await self._api.session.get(server["upload_url"])

        data = await self.read(file_source)
        file = self.get_bytes_io(data)
        video = await self.upload_files(server["upload_url"], {"video_file": file})

        if self.generate_attachment_strings:
            return self.generate_attachment_string("video", video["owner_id"], video["video_id"])
        return video

    async def get_server(self, **kwargs) -> dict:
        return await self._api.method("video.save", **kwargs)
