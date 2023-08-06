from __future__ import annotations

import grpc
import json
from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from deepdriver.sdk.interface import http_interface
from deepdriver.sdk.interface.grpc_interface_pb2 import *
from deepdriver.sdk.interface.grpc_interface_pb2_grpc import ResourceStub
if TYPE_CHECKING:
    from deepdriver.sdk.artifact import Artifact

stub: ResourceStub

def set_stub(stub_: ResourceStub) -> None:
    global stub
    stub = stub_

def get_stub() -> ResourceStub:
    global stub
    return stub

def upload_config():
    pass

def upload_log(run_id: int, log_step: int, item_dict: Dict[str, Any]) -> bool:
    item = [LogItem(key=key, value=str(value)) for key, value in item_dict.items()]
    rsp: UploadLogResponse = get_stub().upload_log(UploadLogRequest(
        item=item,
        step=LogStep(num=log_step),
        run=RunInfo(run_id=run_id),
        authorization=http_interface.get_jwt_key(),
    ))
    return rsp.rsp_result.result == "success"

CHUNK_SIZE = 1024 * 1024  # 1MB

def load_file(local_path: str, root_path: str, path: str, run_id: int, artifact_id: int, last_file_yn: str, artifact_digest: str, entry_digest: str, entry_list: List[ArtifactEntry]) -> UploadFileRequest:
    yield UploadFileRequest(
        file=FileRecord(file=FileItem(
            filepath=FilePath(
                path=path,
                root_path=root_path,
            )
        )),
        artifact_id=artifact_id,
        run_id=run_id,
        digest=entry_digest,
        last_file_yn=last_file_yn,
        authorization=http_interface.get_jwt_key(),
        total_file_info=TotalFileInfo(
            digest=artifact_digest,
            entry=entry_list,
        ),
    )
    with open(local_path, "rb") as file:
        while True:
            chunk_bytes = file.read(CHUNK_SIZE)
            if len(chunk_bytes) == 0: # Reached EOF
                return
            yield UploadFileRequest(
                file=FileRecord(file=FileItem(
                    contents=chunk_bytes
                )),
                artifact_id=artifact_id,
                run_id=run_id,
                digest=entry_digest,
                last_file_yn=last_file_yn,
                authorization=http_interface.get_jwt_key(),
                total_file_info=TotalFileInfo(
                    digest=artifact_digest,
                    entry=entry_list,
                ),
            )

def upload_file(local_path: str, root_path: str, path: str, run_id: int, artifact_id: int, last_file_yn: str, artifact_digest: str, entry_digest: str, entry_list: List[ArtifactEntry]) -> bool:
    rsp: UploadFileResponse = get_stub().upload_file(load_file(local_path, root_path, path, run_id, artifact_id, last_file_yn, artifact_digest, entry_digest, entry_list))
    return rsp.rsp_result.result == "success"

def save_file(file_path: str, rsps) -> None:
    with open(file_path, "wb") as file:
        for rsp in rsps:
            chunk = bytes(rsp.contents)
            if len(chunk) == 0:
                raise Exception("empty chunk")
            file.write(chunk)
    return None

def download_file(path: str, artifact_id: int, local_path: str):
    # TODO 응답에 digest 값을 받아 추후 각 파일에 대한 정합성 체크시 활용한다.
    save_file(local_path, get_stub().download_file(DownloadFileRequest(
        path=path,
        artifact_id=artifact_id,
        authorization=http_interface.get_jwt_key(),
    )))

def upload_artifact(run_id: int, artifact: Artifact, artifact_digest: str, entry_list: List[ArtifactEntry]) -> int:
    rsp: UploadArtifactResponse = get_stub().upload_artifact(UploadArtifactRequest(
        artifact=ArtifactRecord(
            run_id=run_id,
            type=artifact.type,
            name=artifact.name,
            digest=artifact_digest,
            description=artifact.desc,
            versioning=artifact.versioning,
            metadata=json.dumps(artifact.meta_data),
            entry_list=entry_list,
        ),
        authorization=http_interface.get_jwt_key(),
    ))
    return rsp.artifact_id if rsp.rsp_result.result == "success" else None

def use_artifact(name: str, type: str, tag: str, team_name: str, exp_name: str, run_id: int) -> Tuple(int, ArtifactRecord):
    rsp: UseArtifactResponse = get_stub().use_artifact(UseArtifactRequest(
        artifact_name=name,
        artifact_type=type,
        artifact_tag=tag,
        team_name=team_name,
        exp_name=exp_name,
        run_id=run_id,
        authorization=http_interface.get_jwt_key(),
    ))
    return rsp.artifact_id, rsp.artifact

def download_artifact():
    pass

def login(key: str) -> bool:
    rsp = http_interface.login(key)
    if rsp["result"] == "success":
        # grpc stub 생성
        channel = grpc.insecure_channel(rsp["grpcHost"])
        stub = ResourceStub(channel)
        set_stub(stub)
    return rsp["result"] == "success"

def init(exp_name: str="", team_name: str="", run_name: str="", config: Dict=None) -> Dict:
    return http_interface.init(exp_name, team_name, run_name, config)

def finish(data: Dict) -> Dict:
    return http_interface.finish(data)
