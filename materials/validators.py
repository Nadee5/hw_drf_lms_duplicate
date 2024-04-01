from rest_framework.serializers import ValidationError


def validator_url(url):
    if url and 'youtube.com' not in url:
        raise ValidationError('Содержит ссылку на запрещенный ресурс')
