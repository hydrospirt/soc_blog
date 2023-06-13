from decouple import config
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST
from taggit.models import Tag

from .forms import CommentForm, EmailPostForm
from .models import Post, Status


def post_list(request, tag_slug=None):
    post_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(post_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/post/list.html',
        {'posts': posts,
         'tag': tag}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post,
                             status=Status.PUBLISHED,
                             slug=post,
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        'blog/post/detail.html',
        {'post': post,
         'comments': comments,
         'form': form,
         }
    )


def post_share(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Status.PUBLISHED
    )

    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            subject = (f'{cd["name"]} рекомендую прочитать ' +
                       f'"{post.title}"')
            message = ('Прочти интересную публикацию ' +
                       f'"{post.title}" по {post_url}\n\n' +
                       f'{cd["name"]} оставил Вам комментарий: ' +
                       f'{cd["comments"]}')
            send_mail(subject, message, config('EMAIL_HOST_USER'),
                      [cd['to']])
            sent = True

    form = EmailPostForm()
    return render(
        request,
        'blog/post/share.html',
        {'post': post,
         'form': form,
         'sent': sent}
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status=Status.PUBLISHED
    )
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
    return render(request,
                  'blog/post/comment.html',
                  {'post': post,
                   'form': form,
                   'comment': comment})
