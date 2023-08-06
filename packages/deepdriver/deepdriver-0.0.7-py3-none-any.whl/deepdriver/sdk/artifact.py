import hashlib
import os
from assertpy import assert_that
from typing import Dict, List, Union
from pathlib import Path
from PIL.Image import Image

from deepdriver.sdk.chart.chart import Chart
from deepdriver.sdk.data_types.run import Run
from deepdriver.sdk.data_types.table import Table
from deepdriver.sdk.interface import interface
from deepdriver.sdk.interface.grpc_interface_pb2 import ArtifactEntry as grpc_ArtifactEntry

class ArtifactEntry:

    def __init__(self, path: str, local_path: str, size: int, digest: str):
        assert_that(path).is_not_none()
        assert_that(local_path).is_not_none()

        # path는 서버에 전송될 경로
        # ArtifactEntry의 path설정 규칙
        self.path = path

        # 아티펙트 엔트리의 로컬 경로
        # local_path는 artifact.add()를 통해서 추가된 파일의 로컬 경로
        self.local_path = local_path

        # 파일의 사이즈
        self.size = size

        # 파일의 digest 값
        self.digest = digest

    # ArtifactEntry 객체를 기반으로 파일 다운로드 수행
    def download(self, local_root_path: str, artifact_id: int):
        assert_that(local_root_path).is_not_none()
        assert_that(artifact_id).is_not_none()

        local_path = f"{local_root_path}/{self.path}"
        i_last_separator = len(local_path) - local_path[::-1].find("/") - 1
        Path(local_path[:i_last_separator]).mkdir(parents=True, exist_ok=True)

        interface.download_file(self.path, artifact_id, local_path)

        # 다운로드 완료 후 local_path 설정
        self.local_path = local_path

    # ArtifactEntry 객체를 기반으로 파일 업로드 수행
    def upload(self, root_path: str, run_id: int, artifact_id: int, last_file_yn: str, artifact_digest: str, entry_list: List[grpc_ArtifactEntry]) -> bool:
        assert_that(root_path).is_not_none()
        assert_that(run_id).is_not_none()
        assert_that(artifact_id).is_not_none()
        assert_that(last_file_yn).is_not_none()
        assert_that(artifact_digest).is_not_none()
        assert_that(entry_list).is_not_none()
        return interface.upload_file(self.local_path, root_path, self.path, run_id, artifact_id, last_file_yn, artifact_digest, self.digest, entry_list)

    def __str__(self) -> str:
        return f"{{path:{self.path},local_path:{self.local_path}}}"

# Artifact 객체에 추가되는 객체는 Image, 일반 파일, 폴더(하위 파일 포함), Table, 소스코드 등이 있다
class Artifact:

    def __init__(self, name: str, type: str, id: int=0, desc: str=None, versioning: str="Y", meta_data: Dict=None, entry_list: List[ArtifactEntry]=None) -> None:
        assert_that(name).is_not_none()
        assert_that(type).is_not_none()

        self.name = name
        self.type = type
        self.id = id
        self.desc = desc
        self.versioning = versioning

        # 메타정보 (for 모델 or 코드)
        # Ai 학습 모델과 같은 데이터가 아티펙트로 추가될 때 추가정보( 하이퍼파라미터)도 같이 기록되기위한 meta_data 정보
        self.meta_data = meta_data if meta_data else {}

        # ArtifactEntry 의 list
        # Artifact.add() 함수로 데이터가 추가될때마다 리스트에 추가됨
        self.entry_list = entry_list if entry_list else []

    # 해당 Artifact에 데이터를 추가하는 함수
    # obj 및 파일 내용이 추가되면 임시 파일로 저장후 path를 추가한다
    # 추가된 각 항목에 대해서 ArtifactEntry를 생성한 후 Artifact가 가진 ArtifactEntry list에 추가함
    # name: 아티펙트에 각 엔트리의 식별자로 기록될 이름
    # data: 아티펙트에 추가될 데이터( Table  | Image | chart | file name | directory path | reference url )
    def add(self, data: Union[str, Table, Image, Chart], name: str=None) -> None:
        assert_that(data).is_not_none()

        # data에 str가 들어오면 file 인지, dir 인지 reference url(http:// or s3:// ..) 인지 체크
        if isinstance(data, str):
            if os.path.isfile(data):
                # file인경우 ArtifactEntry 생성후 local_path, path,size, digest등을 설정한 후 Artifact의 entry_list에 추가
                local_path = data
                if name:
                    # add시 name이 지정된 경우: name/하위폴더명/파일명
                    i_name_begin = local_path.find(name)
                    path = local_path[i_name_begin:]
                else:
                    # add시 name이 지정되지 않은 경우: 하위폴더명/파일명
                    path = os.path.join(*local_path.split("/")[2:])
                size = os.stat(local_path).st_size
                with open(local_path,"rb") as f:
                    digest = hashlib.md5(f.read()).hexdigest()
                self.entry_list.append(ArtifactEntry(path, local_path, size, digest))
            else:
                # dir인경우 하위 파일을 순회하며 위의 과정 반복
                dir_path = data
                for file_dir_name in os.listdir(dir_path):
                    file_dir_path = os.path.join(dir_path, file_dir_name)
                    self.add(file_dir_path, name)

    # Artifact의 정보를 전송하고, ArtifactEntry 각각의 파일을 전송한다
    def upload(self, run: Run) -> bool:
        # Interface.py의 upoad_artifact ( grpc_interface.py의 upoad_artifact)를 호출 하여 artifact 정보에 대해 전송
        entry_dict = {entry.path: entry for entry in self.entry_list}
        entry_list: List(grpc_ArtifactEntry) = []
        hasher = hashlib.md5()
        for entry_path, entry in sorted(entry_dict.items()):
            entry_list.append(grpc_ArtifactEntry(
                path=entry_path,
                digest=entry.digest,
                size=entry.size,
                local_path=entry.local_path,
            ))
            hasher.update(f"{entry_path}:{entry.digest}\n".encode())
        artifact_digest = hasher.hexdigest()
        id = interface.upload_artifact(run.run_id, self, artifact_digest, entry_list)
        if id is None:
            return False
        self.id = id

        # artifact에 추가된 파일들(ArtifactEntry의 파일)은 각각의 upload함수 호출
        for i, entry in enumerate(self.entry_list):
            # ArtifactEntry.upload() 호출시 인자로서 파일이 저장될 폴더 정보를 넘겨줌
            root_path = f"{run.run_id}/artifact/{self.type}/{self.name}"
            last_file_yn = "Y" if i == len(self.entry_list)-1 else "N"
            succeeded = entry.upload(root_path, run.run_id, self.id, last_file_yn, artifact_digest, entry_list)
            if not succeeded:
                return False
        return True

    # Artifact 객체를 기반으로 Artifact에 등록된 모든 엔트리의 다운로드 수행
    def download(self) -> str:
        # ./deepdriver/artifact/{artifact_id}/ 폴더가 생성된다
        local_root_path = f"./deepdriver/artifact/{self.id}"

        # Artifact 객체가 가진 entry_list 의  ArtifactEntry.download()를 각각 호출
        for entry in self.entry_list:
            entry.download(local_root_path, self.id)
        return local_root_path

    def __str__(self) -> str:
        return "[" + ",".join(str(entry) for entry in self.entry_list) + "]"
