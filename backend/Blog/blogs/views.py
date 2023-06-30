import io
from time import sleep
import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from blogs.models import BlogModel
from blogs.serializers import BlogsSerializer
from blogs.pdf import PDFSummarizer



# Create your views here.


class BlogView(APIView):
    serializer = BlogsSerializer
    def get(self, request):
        """
            Returns a list of all the blog posts
        """
        
        Queryblogs = BlogModel.objects.all()
        serialized_blog = self.serializer(Queryblogs, many=True)
        
        return Response(serialized_blog.data, status=200)
    
    def post(self, request):
        """Creates a new blog post

        Body parameters:
        {
            title: The title of the blog post
            pdf_file : pdf file containing the blog paper
            source_url : url of the source related to the blog post
        }
            
        """
        
        title = request.data.get('title', '')
        source_url = request.data.get('source_url','')
        pdf_file = request.FILES['pdf_file']
        
        summarizer = PDFSummarizer(pdf_file)
        chunks = 10
        
        
        result=  summarizer.chunkerize_and_summarize(chunks)
       
            
        questions = [
                        "what is the summary of the abstract of this article",
                        "what is the thesis of the article",
                        "what was the method used in the article",
                        "List, explain and discuss key findings in the article",
                        "summarize a conclusion for this article",
                        "List the most important sources"
                    ]
        
        blog: str = ''
        
        # for q in questions:
        #     res = summarizer.question_llm(q, result)
        #     blog += f"{q}: {res}"
            
        
        return Response(result ,status=200)
        
        