import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import TokenTextSplitter
from langchain_core.documents import Document
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from src.prompt import *

load_dotenv()
GRQO_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GROQ_API_KEY"] = GRQO_API_KEY
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

#we can also create class here, but that is done for when large number of functions are involved

def file_processing(file_path):

    loader = PyPDFLoader(file_path)
    data = loader.load()

    question_gen = "" 

    for page in data:
        question_gen += page.page_content 
    
    splitter_ques_gen = TokenTextSplitter(
        encoding_name="cl100k_base",
        chunk_size=10000,
        chunk_overlap=200,
    )

    chunk_ques_gen = splitter_ques_gen.split_text(question_gen)

    document_ques_gen = [Document(page_content = t) for t in chunk_ques_gen]

    splitter_ans_gen = TokenTextSplitter(
        encoding_name="cl100k_base",
        chunk_size=1500,
        chunk_overlap=100,
    )

    document_ans_gen = splitter_ans_gen.split_documents(document_ques_gen)

    return document_ques_gen, document_ans_gen

def llm_pipeline(file_path):

    document_ques_gen, document_ans_gen = file_processing(file_path)

    llm_ques_gen_pipeline = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.3,
    )

    prompt_questions = PromptTemplate(template=prompt_template,input_variables=['text'])

    Refine_Prompt_Questions = PromptTemplate(
        input_variables=["existing_answers","text"],
        template=refine_template,
    )

    output_parser = StrOutputParser()

    ques_gen_chain = (
        prompt_questions
        | llm_ques_gen_pipeline
        | output_parser
    )

    refine_ques_gen_chain = (
        Refine_Prompt_Questions
        | llm_ques_gen_pipeline
        | output_parser
    )

    questions = ques_gen_chain.invoke({
        "text":document_ans_gen[0].page_content
    })

    for doc in document_ans_gen[1:]:
        questions = refine_ques_gen_chain.invoke({
            "existing_answers":questions,
            "text":doc.page_content
        })

    embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")

    vector_store = FAISS.from_documents(document_ans_gen, embeddings)

    llm_ans_gen = ChatGroq(temperature=0.1,model="openai/gpt-oss-120b")

    questions_list = questions.split("\n")

    retriever = vector_store.as_retriever(search_kwargs={"k":4})

    def format_docs(docs):
        return "\n\n".join(d.page_content for d in docs)
    
    answer_prompt = ChatPromptTemplate.from_template(answer_template)

    answer_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | answer_prompt
        | llm_ans_gen
        | StrOutputParser()
    )

    questions_list = [q.strip() for q in questions.split("\n") if q.strip()]

    return questions_list, answer_chain