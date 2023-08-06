import logging
from typing import Dict

from deepdriver.sdk.data_types.run import set_run, Run
from deepdriver.sdk.interface import interface

logger = logging.getLogger("deepdriver")

# 실행과 실험환경을 만드는 함수
def init(exp_name: str="", team_name: str="", run_name: str="", config: Dict=None) -> Run:
    rsp = interface.init(exp_name, team_name, run_name, config)
    run = Run(rsp["teamName"], rsp["expName"], rsp["runName"], rsp["runId"], rsp["runUrl"])
    logger.info("DeepDriver initialized\n"
        f"Team Name={rsp['teamName']}\n"
        f"Exp Name={rsp['expName']}\n"
        f"Run Name={rsp['runName']}\n"
        f"Run URL={rsp['runUrl']}"
    )
    set_run(run)
    return run
