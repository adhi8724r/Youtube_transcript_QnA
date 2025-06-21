from youtube_transcript_api import YouTubeTranscriptApi,TranscriptsDisabled
from typing import List
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

def get_docs(id: str)->str:
    try:
        transcript_api = YouTubeTranscriptApi()
        transcript = transcript_api.fetch(video_id=id)
        document=""
        for snippet in transcript:
            document=document+" "+snippet.text

        return document
    except TranscriptsDisabled:
        print("Transcript not available")
        raise
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

def split_text(document: str)-> List[Document]:
    splitter = RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=100)
    chunks = splitter.create_documents([document])

    return chunks
