from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, View

from .forms import CommentForm
from .models import Post


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "posts"

    def get_queryset(self):
        return super().get_queryset()[:3]


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class SingletonPostView(View):
    template_name = "blog/post-detail.html"

    def is_stored_post(self, request, post_id):
        return post_id in request.session.get("stored_posts", [])

    def render_post(self, request, post, comment_form):
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id),
        }
        return render(request, self.template_name, context)

    def get(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        return self.render_post(request, post, CommentForm())

    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))

        return self.render_post(request, post, comment_form)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts", [])
        posts = Post.objects.filter(id__in=stored_posts) if stored_posts else []

        context = {
            "posts": posts,
            "has_posts": bool(stored_posts),
        }
        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        try:
            post_id = int(request.POST["post_id"])
        except (KeyError, ValueError):
            return HttpResponseRedirect(reverse("starting-page"))

        stored_posts = request.session.get("stored_posts", [])

        if post_id in stored_posts:
            stored_posts.remove(post_id)
        else:
            stored_posts.append(post_id)

        # Reassign so the session knows it was modified.
        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect(reverse("starting-page"))
