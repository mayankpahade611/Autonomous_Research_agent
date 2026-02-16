from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_text_splitter():
    return RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

def split_text(text: str):
    splitter = get_text_splitter()
    return splitter.split_text(text)

