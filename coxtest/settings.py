import chromadb

from coxtest.get_env import EnvKeys
from coxtest.rag.faq import FaqRagManager


env_key: EnvKeys
chroma_client: chromadb.Client


def set_chroma_db():
    """chromaDB setup"""
    global chroma_client
    # 컨테이너 로컬에 DB 파일 생성
    chroma_client = chromadb.PersistentClient(path=env_key.CHROMA_PATH)

    # chromaDB에 데이터 인입
    # for model_type in ['hug', 'oai']:
    for model_type in ['hug']:
        FaqRagManager(
            file_path=env_key.FAQ_PATH,
            embedding_model_type=model_type
        )


def initialize():
    """coxtest 패키지 initialize(프로세스 단위)"""
    global env_key

    try:
        # set env key
        env_key = EnvKeys()

        # set chroma db
        set_chroma_db()

    except Exception as e:
        raise Exception(f'Failed on initialize: {e}')
