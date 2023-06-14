import markdown
from blog.models import Post
from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy


class LatestPostsFeed(Feed):
    title = 'Игроград'
    link = reverse_lazy('blog:post_list')
    decription = 'Новые публикации сайта'

    def items(self):
        return Post.published.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords_html(markdown.markdown(item.text), 10)

    def item_pubdate(self, item):
        return item.publish
