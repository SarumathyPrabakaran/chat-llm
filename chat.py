import transformers
import torch
from torch import cuda, bfloat16

from langchain_community.llms import HuggingFacePipeline

class ChatBot:
  def __init__(self, file_path):
    model_id = "meta-llama/Llama-2-7b-chat-hf"
    # device = f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'
    bnb_config = transformers.BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=bfloat16
    )
    model = transformers.AutoModelForCausalLM.from_pretrained(
    model_id,
    quantization_config=bnb_config,
    device_map='auto',
    )

    tokenizer = transformers.AutoTokenizer.from_pretrained(model_id)
    query_pipeline = transformers.pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        torch_dtype=torch.float16,
        device_map="auto"
    )

    self.llm = HuggingFacePipeline(pipeline=query_pipeline)
    with open(file_path, 'r') as f:
      self.file_content = f.read()
   


  def invoke(self, question):
    template = f"""
        <s>[INST] <<SYS>>
        You are a helpful, respectful and honest query answering assistant. Your name is Rias, you are a guide for AWS Community day happening at St. Joseph's Institute of Technology.
        You will be provided information about the event plan and venues. All your answers are short and straight to the point.
        You should answer them accordingly and if you do not know the answer, do not try to make it up, instead say to contact event organizers.

        Context: {self.file_content}
        <</SYS>>

        Question: {question}

        Answer:[/INST]
        """

    return self.llm.invoke(template)