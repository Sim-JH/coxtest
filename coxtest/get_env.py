import os


class EnvKeys:
    """Env parser"""
    def __init__(self):
        # config
        source_home = "/src/module/coxtest"
        self.TEMPLATE_PATH = f"{source_home}/template"
        self.FAQ_PATH = f"{self.TEMPLATE_PATH}/final_result.pkl"
        self.CHROMA_PATH = f"{self.TEMPLATE_PATH}/chroma_db"

        # 환경변수
        self.WEB_HOST: str = os.getenv('WEB_HOST', '0.0.0.0')
        self.WEB_PORT: str = os.getenv('WEB_PORT', '5000')
        self.REDIS_HOST: str = os.getenv('REDIS_HOST', 'coxtest-redis')
        self.REDIS_PORT: str = os.getenv('REDIS_PORT', '6379')
