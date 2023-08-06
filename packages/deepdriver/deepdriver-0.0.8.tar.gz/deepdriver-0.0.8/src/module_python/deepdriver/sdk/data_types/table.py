import json
from assertpy import assert_that
from pathlib import Path

from deepdriver.sdk.data_types.dataFrame import DataFrame
from deepdriver.sdk.data_types.media import LOG_TYPE_TABLE, Media
from deepdriver.sdk.data_types.run import Run
from deepdriver.sdk.interface import interface

class Table(Media):

    def __init__(self, data: DataFrame) -> None:
        super().__init__(log_type=LOG_TYPE_TABLE)

        assert_that(data).is_not_none()
        self.data = data

    def to_json(self, key_name: str) -> str:
        assert_that(key_name).is_not_none()

        value_type = __class__.__name__
        return json.dumps({
            "log_type" : self.log_type,
            "path" : self.get_path(key_name, value_type),
            "cols" : len(self.data.dataframe.columns),
            "rows" : len(self.data.dataframe),
        })

    # json으로 구성된 메타데이터 전송
    def upload(self, run: Run, key_name: str) -> None:
        # Run.log에 Table 객체가 기록된 경우 Table의 정보 및 값을 올리기 위한 함수

        # interface.py의 upoad_log 호출하여 table의 정보 전송
        # LogItem의 key값은 넘겨받은 key_name값으로 설정, val값은 Table.to_json()을 통해 얻은 값으로 설정후 전송
        interface.upload_log(run.run_id, run.log_step, {key_name: self.to_json(key_name)})

        # Table.upload_file()을 호출하여 table의 데이터를 서버로 전송하도록 함
        self.upload_file()

    # 실제 파일 서버로 전송
    # Run.log에 Image 객체가 기록된 경우 Image 의 값을 올리기 위한 함수
    # table내용을 json으로 변환하여 파일로 저장후 전송
    def upload_file(self, run: Run, key_name: str) -> None:
        # Table의 data인 deepdriver.dataframe으로부터 column과 data를 가져와서 json형태의 파일로 저장
        Path(self.get_local_dir_path(run.run_id)).mkdir(parents=True, exist_ok=True)
        local_path = self.get_local_path(run.run_id, key_name)
        with open(local_path, "w") as f:
            json.dump(self.data.data, f)

        # 저장한 파일을 Interface.py의 upoad_file을 호출하여 전송
        value_type = __class__.__name__
        root_path = self.get_root_path(run.run_id)
        path = self.get_path(key_name, value_type)
        interface.upload_file(local_path, root_path, path, run.run_id)

    def get_root_path(self, run_id: int) -> str:
        return f"{run_id}/media"

    def get_local_dir_path(self, run_id: int) -> str:
        return f"./deepdriver/run/{self.get_root_path(run_id)}"

    def get_path(self, key_name: str, value_type: str) -> str:
        return f"{key_name}.{value_type}.json"

    def get_local_path(self, run_id: int, key_name: str, value_type: str) -> str:
        return f"{self.get_local_dir_path(run_id)}/{self.get_path(key_name, value_type)}"
