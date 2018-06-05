{% load i18n %}
{% load auth %}

var menu = {
    '{% trans "Новости" %}': '{% url 'post_list' %}',
    '{% trans "Категории" %}': {
        {% auth_can_view_category 'report' as allow_report %}
        {% auth_can_view_category 'photo' as allow_photo %}
        {% auth_can_view_category 'map' as allow_map %}
        {% auth_can_view_category 'drawing' as allow_drawing %}
        {% auth_can_view_category 'prose' as allow_prose %}

        {% if allow_report %}'{% trans "Очеты" %}': '{% url 'category_list' category='report' %}', {% endif %}
        {% if allow_photo %}'{% trans "Фотографии" %}': '{% url 'category_list' category='photo' %}', {% endif %}
        {% if allow_map %}'{% trans "Карты" %}': '{% url 'category_list' category='map' %}', {% endif %}
        {% if allow_drawing %}'{% trans "Графика" %}': '{% url 'category_list' category='drawing' %}', {% endif %}
        {% if allow_prose %}'{% trans "Писательство" %}': '{% url 'category_list' category='prose' %}' {% endif %}
    },
    '{% trans "Общение" %}': {
        '{% trans "Форум" %}': '#',
        '{% trans "Вылазки" %}': '#',
        '{% trans "Снаряжение" %}': '#',
        '{% trans "Другие вылазки" %}': '#',
        '{% trans "Курилка" %}': '#',
        '{% trans "Техн. раздел" %}': '#'
    },
    'Wiki/FAQ': '#',

    {% if user.is_staff %}
        'Управление': '/admin/',
    {% endif %}

    {% if user.is_authenticated %}
        '{% trans "Выход" %}': '{% url 'auth_logout' %}?next={{request.path}}'
    {% else %}
        '{% trans "Регистрация" %}': '{% url 'registration_register' %}',
        '{% trans "Вход" %}': '{% url 'auth_login' %}?next={{request.path}}'
    {% endif %}
};

$('#acisMenu').acisMenu({
    class: 'main-menu',
    items: menu
});