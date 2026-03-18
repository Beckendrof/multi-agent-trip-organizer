from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain.schema import BaseRetriever

from backend.config import OPENAI_API_KEY, PINECONE_INDEX_NAME, EMBEDDING_MODEL


def get_retriever(top_k: int = 5) -> BaseRetriever:
    """Return a Pinecone-backed retriever for venue rule lookups."""
    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        openai_api_key=OPENAI_API_KEY,
    )
    vectorstore = PineconeVectorStore(
        index_name=PINECONE_INDEX_NAME,
        embedding=embeddings,
    )
    return vectorstore.as_retriever(search_kwargs={"k": top_k})
