import io
from time import sleep
import pdfplumber
import os
from dotenv import load_dotenv
from openai import ChatCompletion 
load_dotenv()

class PDFSummarizer:
    pdf_file: str
    pdf_text: str
    API_KEY: str
    
    ai_config: dict = {
        "init_instrcution_message" : """
         You are a helpful assistant tasked with summarizing parts of research papers in a blog-like format. 
         1. Analyze the paper, focusing on the abstract, introduction, results, and conclusion.
         2. Extract key points, including the main argument, methodology, findings, and implications.
         3. Use reliable external sources to fill in any unclear terms, concepts, or references.
         4. Write an engaging and informative summary using the key points and external sources to fill knowledge gaps.
         5. Avoid redundancy; each point should be unique and contribute to the reader's understanding.
         6. Review and revise the summary for clarity, coherence, and conciseness.
         """
    }
  
    def extract_text_from_pdf(self, pdf_bytes):
        with pdfplumber.open(pdf_bytes) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        self.pdf_text = text
    
    def setOpenai(self):
        self.API_KEY= os.getenv('API_KEY')
        
    def question_llm(
        self,
        system_prompt: str,
        prompt: str,
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=500,
    ):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ]

        response = ChatCompletion.create(
            api_key= self.API_KEY,
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0]['message']['content']
    
    def summarize_chunk(self, chunk):
        response = ChatCompletion.create(
            api_key=self.API_KEY,
            model="gpt-3.5-turbo",
            max_tokens=200,
            messages=[
                    {"role": "user", "content" : self.ai_config['init_instrcution_message']},
                    {"role": "user", "content": chunk},
                ]
            )
        
        return response.choices[0]['message']['content']
    
    def split_text_into_chunks(self, chunk_count):
        words = self.pdf_text.split()
        total_words = len(words)
        words_per_chunk = total_words // chunk_count
        extra_words = total_words % chunk_count

        start = 0
        for _ in range(chunk_count):
            end = start + words_per_chunk + (1 if extra_words > 0 else 0)
            chunk = " ".join(words[start:end])
            yield chunk
            start = end
            extra_words -= 1
                    
    def chunkerize_and_summarize(self, chunk_count):
        result = ''
        for chunk in self.split_text_into_chunks(chunk_count):
            print('chunklen',len(chunk))
            sleep(2)
            result += self.summarize_chunk(chunk)
        return result
        
    def __init__(self, pdf_file):
        super()
        self.setOpenai()
        self.pdf_file = pdf_file
        self.extract_text_from_pdf(io.BytesIO(pdf_file.read()))
       
       
if __name__ == '__main__':   
    summarizer = PDFSummarizer()
    print(summarizer.summarize())

