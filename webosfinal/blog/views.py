from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import generic
from .models import Post
from django.http import HttpResponse
from .forms import CommentForm
import json

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_detail.html'



def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    # Check if the flag is already present in the cookies
    flag_cookie = request.COOKIES.get('flag')

    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()

            comment_text = new_comment.body.lower()  # Convert to lowercase for case-insensitive comparison
            if "<script>alert(xss)</script>" in comment_text:
                # Construct the response with JavaScript to trigger the alert
                response_data = {
                    'message': 'this is flag number 3'
                }
                response = HttpResponse(json.dumps(response_data), content_type='application/json')
                return response

            if "cat ../settings.py" in comment_text:
                # Construct the response with JavaScript to trigger the alert
                response_data = {
                    'message': 'this is flag number 4'
                }
                response = HttpResponse(json.dumps(response_data), content_type='application/json')
                return response



            # Set the flag in the cookies
            response = HttpResponse(template_name)
            response.set_cookie('thisisflagnumber2', 'congrats')
            return response
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})
