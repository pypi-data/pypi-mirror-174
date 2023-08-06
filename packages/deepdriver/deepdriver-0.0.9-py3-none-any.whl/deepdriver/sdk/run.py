import json
from typing import Dict

from deepdriver.sdk.artifact import Artifact, ArtifactEntry
from deepdriver.sdk.data_types.run import get_run

# dictionary 형태의 데이터, image, table, chart 등을 log 함수를 통해 서버로 전송
def log(data: Dict) -> bool:
    return get_run().log(data)

# image, table, dictionary 형태의 데이터를 log_artifact 를 통해 서버로 전송
def log_artifact(artifact: Artifact) -> bool:
    return get_run().log_artifact(artifact)

def use_artifact(name: str, type: str, tag: str="", team_name: str="", exp_name: str="") -> Artifact:
    artifact_id, artifact_record = get_run().use_artifact(name, type, tag, team_name, exp_name)
    entry_list = []
    for entry in artifact_record.entry_list:
        entry_list.append(ArtifactEntry(entry.path, entry.local_path, entry.size, entry.digest))
    return Artifact(artifact_record.name, artifact_record.type,
        id=artifact_id,
        desc=artifact_record.description,
        meta_data=json.loads(artifact_record.metadata),
        entry_list=entry_list,
    )

# Interface.py의 finish()함수를 호출할때 하기의 summary정보를 dictionary 형태로 넘겨준다
def finish() -> bool:
    return get_run().finish()
