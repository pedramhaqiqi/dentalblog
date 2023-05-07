import io
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
        "init_instrcution_message" : "Summarize the following information:"
    }
  
    def extract_text_from_pdf(self, pdf_bytes):
        with pdfplumber.open(pdf_bytes) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

        self.pdf_text = text
    
    def setOpenai(self):
        self.API_KEY= os.getenv('API_KEY')
        
    def summarize_chunk(self, chunk):
        response = ChatCompletion.create(
            api_key=self.API_KEY,
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "user", "content" : f"{self.ai_config['init_instrcution_message']}"},
                    {"role": "user", "content": f"{chunk}"},
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
