from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post, Category


def post_filter():
    """Filter published posts with valid pub_date and published categories."""
    return Post.objects.filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True
    )


def index(request):
    """Render homepage with 5 latest published posts."""
    return render(
        request,
        'blog/index.html',
        {'post_list': post_filter()[:5]}
    )


def post_detail(request, id):
    """Render detailed view of a single post."""
    post = get_object_or_404(
        post_filter(),
        pk=id
    )
    return render(
        request,
        'blog/detail.html',
        {'post': post}
    )


def category_posts(request, category_slug):
    """Render posts filtered by specific category."""
    category = get_object_or_404(
        Category.objects.filter(is_published=True),
        slug=category_slug
    )
    post_list = post_filter().filter(category=category)
    return render(
        request,
        'blog/category.html',
        {
            'category': category,
            'post_list': post_list
        }
    )