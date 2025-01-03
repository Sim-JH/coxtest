import os
import pickle
from typing import List, Literal

import openai
from sentence_transformers import SentenceTransformer


class FaqRagManager:
    def __init__(
            self,
            file_path=f'{os.getcwd()}/coxtest/template/final_result.pkl',
            collection='faq',
            embedding_model_type: Literal['hug', 'oai'] = 'hug'
    ):
        """ FAQ Rag 클래스
        :param file_path: 데이터 파일 경로
        :param collection: ChromaDB 컬렉션 명 헤더
        :param embedding_model_type: 사용할 임베딩 모델 타입
        """
        from coxtest.settings import chroma_client  # 지연 로드
        
        self.chroma_client = chroma_client
        self.file_path = file_path
        self.collection = f"{collection}_{embedding_model_type}"
        self.model_type = embedding_model_type
        self.openai_api_key = None
        self.collection = self.chroma_client.get_or_create_collection(self.collection)

        # 데이터베이스에 데이터가 없으면 로드
        if not self.collection.count():
            print(self.collection, self.collection.count())
            self._initialize_data()

    def _generate_embeddings(self, texts: List[str]):
        """ 텍스트에 대해 임베딩 생성 """
        if self.model_type == "hug":
            embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            return embedding_model.encode(texts)
        elif self.model_type == "oai":
            res = openai.Embedding.create(
                model="text-embedding-ada-002",
                input=texts
            )
            result = [data['embedding'] for data in res['data']]
            return result

    def _load_faq_data(self, file_path: str):
        """ FAQ 데이터를 파일에서 로드 """
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    def _initialize_data(self):
        """ FAQ 데이터를 로드하고 ChromaDB에 저장 """
        print(f"{self.file_path} 데이터 로드 및 {self.model_type} 임베딩 생성 중...")
        faq_data = self._load_faq_data(self.file_path)
        questions = []
        answers = []

        for question, answer in faq_data.items():
            questions.append(question)
            answers.append(answer)

        embeddings = self._generate_embeddings(questions)

        for i, question in enumerate(questions):
            self.collection.add(
                embeddings=[embeddings[i]],
                metadatas={"answer": answers[i]},
                ids=[str(i)]
            )

        print(f"{len(questions)}개의 데이터를 ChromaDB에 저장")

    def query(self, user_question: str, n_results: int = 1):
        """ 사용자의 질문에 대해 가장 관련성이 높은 FAQ 항목을 검색

        :param user_question: 사용자의 질문
        :param n_results: 반환할 결과 개수
        :return: 관련 FAQ 항목 리스트
        """
        query_embedding = self._generate_embeddings([user_question])
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )

        return results["metadatas"]


