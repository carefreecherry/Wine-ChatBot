from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema.document import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores.chroma import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
import cohere
from langchain.memory import ConversationBufferMemory
import spacy

# Load the English NLP model
nlp = spacy.load("en_core_web_sm")

# Initialize conversation memory
memory = ConversationBufferMemory(return_messages=True, max_token_limit=1000)

# Define the embeddings function using HuggingFace model
def get_embedding_functions():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )
    return embeddings

# Function to add documents to ChromaDB
def add_to_chroma(chunks):
    db = Chroma(
        persist_directory="C:/Users/shrey/CS-ChatBot/ChromaDB",
        embedding_function=get_embedding_functions()
    )
    last_page = 0
    current_chunk_index = 0
    chunk_ids = []
    
    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"
        
        if page != last_page:
            current_chunk_index = 0
        else:
            current_chunk_index += 1
        
        current_page_id = f"{current_page_id}:{current_chunk_index}"
        chunk.metadata["id"] = current_page_id
        chunk_ids.append(current_page_id)
        last_page = page
        print(current_page_id)
    
    db.add_documents(chunks, ids=chunk_ids)
    db.persist()

# Function to retrieve the Chroma database instance
def get_chroma():
    db = Chroma(
        persist_directory="C:/Users/shrey/CS-ChatBot/ChromaDB",
        embedding_function=get_embedding_functions()
    )
    return db

# Function to split documents into chunks
def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False
    )
    return text_splitter.split_documents(documents)

# Function to load documents from PDF directory
def load_documents():
    document_loader = PyPDFDirectoryLoader("C:/Users/shrey/CS-ChatBot/PDF")
    return document_loader.load()

# Function to retrieve context for a given query
def get_context(query):
    db = get_chroma()
    results = db.similarity_search_with_score(query, k=2)
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results]).replace('\n', ' ')
    print(context_text)
    return context_text

# Function to get response from Cohere based on the context and query
def get_response_stream(query, context=""):
    co = cohere.Client("0ioIA8dB9N4B0pwUaCABEW9udSz9ruX1bt9n7zUw")
    context_text = get_context(query)

    if not context_text:
        yield "INFORMATION NOT AVAILABLE. CONTACT THE BUSINESS DIRECTLY."
        return

    # Add the current query to memory
    memory.chat_memory.add_user_message(query)

    # Get conversation history
    conversation_history = memory.load_memory_variables({})["history"]

    # Process the conversation history to identify key entities
    doc = nlp(" ".join([msg.content for msg in conversation_history]))
    key_entities = [ent.text for ent in doc.ents if ent.label_ in ["PRODUCT", "ORG", "PERSON"]]

    # Prepare the prompt (as before)
    prompt = f"""You are an AI assistant for Jessup Cellars winery. Use the following pieces of context to answer the question at the end. 
    If you don't know the answer, just say that INFORMATION NOT AVAILABLE. CONTACT THE BUSINESS DIRECTLY. Don't try to make up an answer.
    Always maintain context from previous messages and refer back to specific details when appropriate.

    Previous conversation:
    {conversation_history}

    Context: {context_text}

    Current question: {query}

    Key entities mentioned: {", ".join(key_entities)}

    When answering follow-up questions:
    1. Use pronouns naturally, but ensure they clearly refer to the correct entity.
    2. If a pronoun might be ambiguous, use the full name of the wine, grape, or product instead.
    3. When introducing new information about a previously mentioned entity, briefly remind the user what that entity is.
    4. Pay special attention to these key entities: {", ".join(key_entities)}

    AI Assistant: """

    # Use the chat_stream method with the specified parameters
    response_text = ""
    for event in co.chat_stream(
        message=prompt,
        temperature=0.7,
        max_tokens=300,
        k=0,
        p=0.75
    ):
        if event.event_type == "text-generation":
            response_text += event.text
            yield event.text
        elif event.event_type == "stream-end":
            break

    if "INFORMATION NOT AVAILABLE" in response_text:
        yield " CONTACT THE BUSINESS DIRECTLY."
    else:
        # Add the AI's response to memory
        memory.chat_memory.add_ai_message(response_text.strip())
    
# Uncomment the following lines to create and populate the Chroma database from PDFs
# documents = load_documents()
# chunks = split_documents(documents)
# print(chunks[0])
# add_to_chroma(chunks)
