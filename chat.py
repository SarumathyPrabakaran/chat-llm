import transformers
from torch import cuda, bfloat16

from langchain_community.llms import HuggingFacePipeline
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA


class ChatBot:
    def __init__(self,file_path):
        llm_name = "meta-llama/Llama-2-7b-chat-hf"
        self.file_path = file_path

        self.llm = self._build_llm(llm_name)
        self.vectordb = self._build_db("sentence-transformers/all-mpnet-base-v2")
        self.qa = self.build_qa()


    def _build_llm(self,llm_model_name):
        bnb_config = transformers.BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=bfloat16
        )

        model = transformers.AutoModelForCausalLM.from_pretrained(
            llm_model_name,
            quantization_config=bnb_config,
            torch_dtype=bfloat16,
            device_map='auto',
        )

        tokenizer = transformers.AutoTokenizer.from_pretrained(llm_model_name)

        query_pipeline = transformers.pipeline(
                "text-generation",
                model=model,
                tokenizer=tokenizer,
                torch_dtype=bfloat16,
                device_map="auto",
                max_new_tokens = 350
        )

        llm = HuggingFacePipeline(pipeline=query_pipeline)

        return llm

    def _build_db(self, sentence_transformer_model):
        loader = TextLoader(self.file_path)
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1024, chunk_overlap=128)
        splitted_documents = text_splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(model_name = sentence_transformer_model,
                                           model_kwargs = {'device': f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'}
                                           )
        vectordb = Chroma.from_documents(documents = splitted_documents,
                                 embedding = embeddings,
                                 persist_directory = "db")
        return vectordb

    def build_qa(self,template = None):
        if not template:
            template = """
<s>[INST] <<SYS>>
You are Rias, You are the brain of a robot whose role is to serve the event attendees and answer their Questions.
You are a helpful, respectful and honest query answering assistant. You are a guide for AWS Community day happening at St. Joseph's Institute of Technology.
You will be provided information about the event plan and venues. All your answers are short and straight to the point. If a them accordingly sked you can introduce yourself as Rias.
You should answerand if you do not know the answer, do not try to make it up, instead say to contact event organizers.

Context: {context}

Only tell relevant information.
<</SYS>>

Question: {question}. Your answer must be in one or two lines.

Answer:[/INST]"""

        QA_CHAIN_PROMPT = PromptTemplate(input_variables=["context", "question"], template=template)

        qa = RetrievalQA.from_chain_type(self.llm,
                                        chain_type='stuff',
                                        retriever=self.vectordb.as_retriever(search_kwargs={'k':2}),
                                        chain_type_kwargs={"prompt": QA_CHAIN_PROMPT})
        self.qa = qa
        return qa

    def ask(self, question):
        return self.qa.invoke(question)['result']