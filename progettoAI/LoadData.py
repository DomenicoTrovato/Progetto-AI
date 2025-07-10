from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_community.document_loaders import PyPDFLoader
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama


# STEP 1: Carica il documento
loader = PyPDFLoader("Progetto-AI\QuestMaster – Documento Lore_ L’Amuleto della Luce.pdf")
documents = loader.load()

# STEP 2: Dividi il testo in chunk gestibili
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

# STEP 3: Crea l'index semantico (FAISS)
embeddings = OllamaEmbeddings(model="llama3.1:8b")
db = FAISS.from_documents(docs, embeddings)

# STEP 4: Crea la catena QA
retriever = db.as_retriever()
llm = Ollama(model="llama3.1:8b")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# STEP 5: Esegui una domanda
while True:
    domanda = input("Fai una domanda sul documento (oppure scrivi 'esci'): ")
    if domanda.lower() == 'esci':
        break
    risposta = qa_chain.run(domanda)
    print("\nRisposta:", risposta, "\n")