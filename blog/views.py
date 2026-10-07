from django.shortcuts import render, get_object_or_404
from datetime import date
from .models import Post


all_posts = [
    # {
    #     "slug": "hike-in-the-mountains",
    #     "image": "mountains.jpg",
    #     "author": "Abhinav",
    #     "date": date(2024, 7, 10),
    #     "title": "Mountain Hiking",
    #     "excerpt": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl vel tincidunt lacinia, nunc nisl aliquam nunc, eget aliquam nisl nunc vel nisl.",
    #     "content": """
    #     Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. 
    #     Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. 
    #     Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi.
    #     Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit 
    #     amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. 
    #     Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue.
    #     """
    # },
    # {
    #     "slug": "beach-vacation",
    #     "image": "woods.jpg",
    #     "author": "Abhinav",
    #     "date": date(2024, 6, 15),
    #     "title": "Beach Vacation",
    #     "excerpt": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl vel tincidunt lacinia, nunc nisl aliquam nunc, eget aliquam nisl nunc vel nisl.",
    #     "content": """
    #     Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. 
    #     Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. 
    #     Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi.
    #     Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit 
    #     amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. 
    #     Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue.
    #     """
    # },
    # {
    #     "slug": "city-exploration",
    #     "image": "coding.jpg",
    #     "author": "Abhinav",
    #     "date": date(2024, 5, 20),
    #     "title": "City Exploration",
    #     "excerpt": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed euismod, nisl vel tincidunt lacinia, nunc nisl aliquam nunc, eget aliquam nisl nunc vel nisl.",
    #     "content": """
    #     Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed non risus. 
    #     Suspendisse lectus tortor, dignissim sit amet, adipiscing nec, ultricies sed, dolor. 
    #     Cras elementum ultrices diam. Maecenas ligula massa, varius a, semper congue, euismod non, mi.
    #     Proin porttitor, orci nec nonummy molestie, enim est eleifend mi, non fermentum diam nisl sit 
    #     amet erat. Duis semper. Duis arcu massa, scelerisque vitae, consequat in, pretium a, enim. 
    #     Pellentesque congue. Ut in risus volutpat libero pharetra tempor. Cras vestibulum bibendum augue.
    #     """
    # }
    
]


# Create your views here.

def get_date(post):
    return post['date']


def starting_page(request):
    latest_posts = Post.objects.all().order_by("-date")[:3]
    # sorted_posts = sorted(all_posts, key=get_date)
    # latest_posts = sorted_posts[-3:]
    return render(request, "blog/index.html", {
        "posts": latest_posts
    })

def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    return render(request, "blog/all-posts.html",{
        "all_posts": all_posts
    })

def post_detail(request, slug):
    identified_post = get_object_or_404(Post, slug=slug)
    # post = next(post for post in all_posts if post["slug"] == slug)
    return render(request, "blog/post-detail.html", {
        "post": identified_post,
        "post_tags":identified_post.tags.all()
    })