from langchain_chroma import Chroma
from langchain import hub

from langchain_openai import OpenAIEmbeddings
from langchain_openai import ChatOpenAI
from langchain.chains import create_history_aware_retriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableParallel

def query(question:str, history:list[str]):
    vectorstore = Chroma(persist_directory="../chroma_db", embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    prompt = hub.pull("rlm/rag-prompt")
    llm = ChatOpenAI()

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain_from_docs = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt
        | llm
        | StrOutputParser()
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain_from_docs)

    resp = rag_chain_with_source.invoke(question)
    return resp


def query2(question, history):
    llm = ChatOpenAI()
    vectorstore = Chroma(persist_directory="../chroma_db", embedding_function=OpenAIEmbeddings())
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
    rephrase_prompt = hub.pull("langchain-ai/chat-langchain-rephrase")
    llm = ChatOpenAI()
    chat_retriever_chain = create_history_aware_retriever(
        llm, retriever, rephrase_prompt
    )

    resp = chat_retriever_chain.invoke({"input": question, "chat_history": history})
    print("RESPONSE IS \n{}".format(resp))
    return resp
