from langchain.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
from langchain_groq import ChatGroq
from typing import List
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()

def build_chain(vectorstore: FAISS):
    retriever = vectorstore.as_retriever(
        search_type='similarity',
        search_kwargs={'k':5}
    )

    prompt = PromptTemplate(
        template ="""
        You are a useful Assistant.
        You will be provided context from youtube transcript.
        Answer the following question from given context.
        {context}
        question: {question}
        """,
        input_variables=['context','question']
    )

    def context_docs(retrieved_docs: List[Document])-> str:
        context='\n'.join(doc.page_content for doc in retrieved_docs)
        return context

    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(context_docs),
        'question': RunnablePassthrough()
    })

    llm = ChatGroq(
       model = "llama-3.3-70b-versatile",
       temperature = 1
    )

    parser = StrOutputParser()
    main_chain = parallel_chain | prompt | llm | parser

    return main_chain