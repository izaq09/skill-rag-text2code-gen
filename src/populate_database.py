from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader

from utils import get_embedding_function, get_logger

logger = get_logger(__name__)

DB_PATH = Path("chroma")
DATA_PATH = Path("data")


def load_documents():
    """
    Procedure to load documents from the data directory
    """
    logger.info(f"Loading documents from {DATA_PATH}")
    loader = DirectoryLoader(str(DATA_PATH), glob="*.md", show_progress=True)
    return loader.load()


def split_documents(documents, chunk_size=2000, chunk_overlap=200):
    """
    Procedure to split documents into smaller chunks
    """
    logger.info("Splitting documents into smaller chunks")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len
    )
    return text_splitter.split_documents(documents)


def save_documents_to_db(chunks):
    """
    Procedure to save documents to the database
    """
    logger.info("Saving documents to the database")
    db = Chroma(
        persist_directory=str(DB_PATH), embedding_function=get_embedding_function()
    )
    db.add_documents(chunks)
    logger.info("Documents saved successfully")


def main(reset=False):
    """
    Main
    """

    # Load documents
    documents = load_documents()

    # Split documents into smaller chunks
    chunks = split_documents(documents)

    # Save documents to the database
    save_documents_to_db(chunks)


if __name__ == "__main__":
    main()
