from django import forms
from .models import Article

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content","article_image"]  #createddate ve author u zaten otomatik oluşacak.
