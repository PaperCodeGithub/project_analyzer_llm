# Project README

## Overview

This project utilizes a codebase indexing and retrieval system powered by LangChain, ChromaDB, and a Gemma3 language model.  It's designed to allow you to ask questions about the codebase and receive relevant answers based on the code's content.

## Usage

You can ask questions about the codebase.  The system will use the Gemma3 language model to understand your question and retrieve relevant code snippets to answer it.

Example Questions:

*   "How do I implement authentication?"
*   "What is the purpose of the `calculate_something` function?"
*   "How do I use the database connection?"

**Key Components and Their Roles**

1.  **`scan_and_load_codebase(path=".", exclude=["**/node_modules/**", "**/target/**", "**/build/**", "**/.venv/**"])`**:
    *   This function is the core of the indexing process.
    *   It traverses the specified directory (`path`) and its subdirectories.
    *   It uses `GenericLoader` to load files based on specified extensions (`.py`, `.js`, `.ts`, etc.).
    *   It filters out certain directories (e.g., `node_modules`, `target`, `.venv`) using the `exclude` list.
    *   It extracts metadata from each file, specifically the "source" field, which is used to identify the file's origin.
    *   It adds the loaded documents to a list called `docs`.

2.  **Document Splitting and Embedding (`RecursiveCharacterTextSplitter`, `Chroma`)**:
    *   `RecursiveCharacterTextSplitter` is used to split the code into smaller chunks. This is crucial for efficient retrieval.  It uses a `chunk_size` and `chunk_overlap` to manage the size and overlap of these chunks.
    *   `Chroma` is a vector database used to store the embeddings (vector representations) of these chunks.  This allows for semantic similarity searches.
    *   The code uses `HuggingFaceEmbeddings` to generate the embeddings.

3.  **`create_stuff_documents_chain` and `create_retrieval_chain`**:
    *   These functions (presumably defined elsewhere, but referenced here) are LangChain chains that combine the document retrieval and the language model interaction.
    *   `create_stuff_documents_chain` likely constructs a chain that retrieves relevant documents based on the user's question and then feeds those documents to the language model.
    *   `create_retrieval_chain` likely builds a chain that uses the `Chroma` vectorstore to retrieve relevant documents and then passes them to the language model.

4.  **`ChatOllama` and `ChatPromptTemplate`**:
    *   `ChatOllama` is used to interact with the ChatOllama language model.
    *   `ChatPromptTemplate` defines the structure of the prompt that's sent to the language model.  It includes placeholders for the context (retrieved documents) and the user's question.

**Workflow**

1.  The user provides a path to the codebase.
2.  The `scan_and_load_codebase` function indexes the codebase, splitting it into chunks and storing the embeddings in Chroma.
3.  The user asks a question about the codebase.
4.  The `create_retrieval_chain` retrieves relevant documents from Chroma based on the question.
5.  The retrieved documents are fed to the language model (ChatOllama) via the `ChatPromptTemplate`.
6.  The language model generates an answer, which is then printed to the console.


