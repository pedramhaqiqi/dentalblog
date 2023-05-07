import io
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
        result = summarizer.chunkerize_and_summarize(8)
                    
        
        # created = BlogModel.objects.create(
        #     summary = pdf_text,
        #     title = title,
        #     source_url = source_url,
        # )
        
        return Response(result ,status=200)
        
        