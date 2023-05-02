from rest_framework.views import APIView
from rest_framework.response import Response
from blogs.models import BlogModel
from blogs.serializers import BlogsSerializer


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
            blog : pdf file containing the blog paper
            image_url : url of the image related to the blog post
            source_url : url of the source related to the blog post
        }
            
        """
        
        title = request.data.get('title', '')
        blog = request.data.get('blog','')
        source_url = request.data.get('source_url','')
        image_url = request.data.get('image_url','')
        
        BlogModel.objects.create(
            summary = blog,
            title = title,
            source_url = source_url,
            image_url = image_url
        )
        
        return Response(status=200)
        