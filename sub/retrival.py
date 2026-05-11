import warnings

from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import ChatOllama
from langchain_chroma import Chroma

from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import sys
from colorama import init, Fore, Style
init(autoreset=True)

warnings.filterwarnings("ignore")

load_dotenv()

def scan_and_load_codebase(path=".", exclude=["**/node_modules/**", "**/target/**", "**/build/**", "**/.venv/**"]):

    suffixes = ['.py', '.js', '.ts', '.c', '.cpp', '.rs', '.h', '.txt', '.md', '.html']
    
    docs = []
    seen_sources = set()
    for glob_pattern in ["**/[!.]*", "*"]:
        loader = GenericLoader.from_filesystem(
            path=path,
            glob=glob_pattern,
            exclude=exclude,
            suffixes=suffixes,
            parser=LanguageParser()
        )
        
        for doc in loader.load():
            source = doc.metadata.get("source")
            if source not in seen_sources:
                seen_sources.add(source)
                docs.append(doc)
                print(f"Loaded: {source}")

    print(f"\n{Fore.LIGHTYELLOW_EX}Total documents loaded: {len(docs)}{Style.RESET_ALL}")

    print(f"{Fore.LIGHTGREEN_EX}Indexing documents...{Style.RESET_ALL}")
    splitters = {
        ".py": RecursiveCharacterTextSplitter.from_language(language=Language.PYTHON, chunk_size=2000, chunk_overlap=200),
        ".cpp": RecursiveCharacterTextSplitter.from_language(language=Language.CPP, chunk_size=2000, chunk_overlap=200),
        ".rs": RecursiveCharacterTextSplitter.from_language(language=Language.RUST, chunk_size=2000, chunk_overlap=200),
        ".js": RecursiveCharacterTextSplitter.from_language(language=Language.JS, chunk_size=2000, chunk_overlap=200),
        ".ts": RecursiveCharacterTextSplitter.from_language(language=Language.TS, chunk_size=2000, chunk_overlap=200), # Fixed missing dot here
        ".c": RecursiveCharacterTextSplitter.from_language(language=Language.C, chunk_size=2000, chunk_overlap=200),
        ".h": RecursiveCharacterTextSplitter.from_language(language=Language.C, chunk_size=2000, chunk_overlap=200),
        ".html": RecursiveCharacterTextSplitter.from_language(language=Language.HTML, chunk_size=2000, chunk_overlap=200),
        ".txt": RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200),
        ".md": RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200),
    }

    fallback_splitter = RecursiveCharacterTextSplitter(chunk_size=2000, chunk_overlap=200)

    texts = []
    for doc in docs:
        ext = os.path.splitext(doc.metadata.get("source", ""))[1]
        splitter = splitters.get(ext, fallback_splitter)
        texts.extend(splitter.split_documents([doc]))

    print(f"{Fore.LIGHTGREEN_EX}Storing vectors...{Style.RESET_ALL}")

    vectorstore = Chroma.from_documents(
        documents=texts, 
        embedding=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    )

    print(f"{Fore.LIGHTGREEN_EX}Initializing language model...{Style.RESET_ALL}")

    llm = ChatOllama(model="gemma3", temperature=0)

    prompt = ChatPromptTemplate.from_template("""
                    You are a helpful assistant with full access to the codebase.
                    Use the following context to explain or generate code as user asked.
                    Context: {context}
                    Question: {input}
                    """)

    combine_docs_chain = create_stuff_documents_chain(llm, prompt)
    retrieval_chain = create_retrieval_chain(vectorstore.as_retriever(), combine_docs_chain)
    
    return retrieval_chain