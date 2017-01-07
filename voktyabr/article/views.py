from django.views.generic import TemplateView
from .models import Article


class ArticleView(TemplateView):
    template_name = 'article/article.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        id = kwargs.get('id', '')
        data['article'] = Article.objects.get(id=id, show=True)
        return data