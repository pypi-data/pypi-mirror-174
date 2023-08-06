from assertpy import assert_that

from deepdriver.sdk.interface import interface

# deepdriver 실험환경을 사용하기위한 로그인 과정
# 서버의 login api를 호출하여 key를 서버로 전송하고 결과로서 jwt key를 받는다
def login(key: str) -> bool:
    assert_that(key).is_not_none()
    return interface.login(key)
