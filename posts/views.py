from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from .models import PostFeed
from .forms import PostFeedForm
from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from connections.models import Connection


class ListPostView(LoginRequiredMixin, ListView):
    template_name = 'posts/feed_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        usernames = Connection.objects.filter(follower__username=self.request.user).values_list('following__username',
                                                                                                flat=True).distinct()
        posts = PostFeed.objects.filter(user__username__in=usernames).order_by('-published_date')
        return posts


class DetailPostView(LoginRequiredMixin, DetailView):
    template_name = 'posts/feed_detail.html'
    context_object_name = 'post'
    model = PostFeed


class CreatePostView(LoginRequiredMixin, CreateView):
    form_class = PostFeedForm
    template_name = 'posts/form.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return redirect('/posts')


class UpdatePostView(LoginRequiredMixin, UpdateView):
    form_class = PostFeedForm
    template_name = 'posts/form.html'
    queryset = PostFeed.objects.all()

    def get(self, request, *args, **kwargs):
        post = PostFeed.objects.get(slug=kwargs['slug'])
        if post.user == request.user:
            return super(UpdatePostView, self).get(request, *args, **kwargs)
        else:
            return redirect('/posts')


class DeletePostView(LoginRequiredMixin, DeleteView):
    form_class = PostFeedForm
    template_name = 'posts/feed_delete.html'

    def get_object(self):
        slug = self.kwargs['slug']
        post = get_object_or_404(PostFeed, slug=slug)
        return post

    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.user == self.request.user:
            return super(DeleteView, self).get(request, *args, **kwargs)
        else:
            return redirect('/posts')

    def get_success_url(self):
        return reverse("post_list")