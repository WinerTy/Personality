from django import template

register = template.Library()

# Список запрещенных слов

BAD_WORDS = ['bad_word']

# Фильтр менят слова из Списка BAD_WORDS на * (Не чувствителен к регистру)

@register.filter()
def censore(value):
    if not isinstance(value, str):
        raise ValueError('Фильтр применяется только к строкам')

    value = value.lower()

    for word in BAD_WORDS:
        value = value.replace(word, "*" * len(word))

    return value