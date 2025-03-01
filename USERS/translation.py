from modeltranslation.translator import register, TranslationOptions
from django.contrib.auth import get_user_model

User=get_user_model()

@register(User)
class UserTranslationOptions(TranslationOptions):
    fields = ('bio', 'occupation')