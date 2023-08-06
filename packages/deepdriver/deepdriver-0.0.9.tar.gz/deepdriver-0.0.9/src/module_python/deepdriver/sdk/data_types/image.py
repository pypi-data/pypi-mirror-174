import os
from assertpy import assert_that
import hashlib
import json
import PIL
import random
import string
from typing import Union

from deepdriver.sdk.data_types.media import LOG_TYPE_IMAGE, Media

class Image(Media):

    def __init__(self, data: Union[str, PIL.Image.Image]) -> None:
        super().__init__(log_type=LOG_TYPE_IMAGE)

        assert_that(data).is_not_none()
        if isinstance(data, str):
            # str인 경우 local_path로 지정하고 data 에는 해당 경로 파일을 로드한 PIL.Image 객체를 지정함
            self.local_path = data
            self.data = PIL.Image.open(self.local_path)
        elif isinstance(data, PIL.Image.Image):
            self.data = data

            # data가 PIL.Image 객체인 경우 7자리의 random id값을 생성한후 {random_id}.{file_format}으로 저장
            random_id = "".join(random.choice(string.digits) for _ in range(7))
            self.local_path = f"{random_id}.{data.format}"
            data.save(self.local_path)
        else:
            raise Exception(f"unknown data type {type(data)}")
        self.height = data.size[1]
        self.width = data.size[0]
        self.format = data.format

    def to_json(self, key_name: str) -> str:
        assert_that(key_name).is_not_none()
        with open(self.local_path,"rb") as f:
            digest = hashlib.md5(f.read()).hexdigest()
        return json.dumps({
            "log_type": self.log_type,
            "hash": digest,
            "size": os.stat(self.local_path).st_size,
            "path": self.get_path(key_name),
            "height": self.height,
            "width": self.width,
            "format": self.format,
        })

    # json으로 구성된 메타데이터 전송
    def upload(self) -> None:
        pass

    # 실제 파일 서버로 전송
    # 이미지를 파일로 저장 혹은 복사 한후 전송
    def upload_file(self) -> None:
        pass

    def get_path(self, key_name: str) -> str:
        return f"{key_name}.{self.format}"
