<!DOCTYPE html>
<html <!-- forum_local -->>
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->

    <link rel="stylesheet" href="/static/jquery-ui/themes/base/jquery-ui.min.css">
    <link rel="stylesheet" href="/static/dist/jquery.fancybox.min.css" >
    <link rel="stylesheet" href="/static/css/style.css">

    <!-- HTML5 shim and Respond.js for IE8 support of HTML5 elements and media queries -->
    <!-- WARNING: Respond.js doesn't work if you view the page via file:// -->
    <!--[if lt IE 9]>
    <script src="https://oss.maxcdn.com/html5shiv/3.7.3/html5shiv.min.js"></script>
    <script src="https://oss.maxcdn.com/respond/1.4.2/respond.min.js"></script>
    <![endif]-->

    <script src="/static/jquery/dist/jquery.min.js"></script>
    <script src="/static/jquery-ui/jquery-ui.min.js"></script>
    <script src="/static/fancybox/dist/jquery.fancybox.min.js"></script>

    <!-- forum_head -->
</head>
<body>

<div class="container-wrapper">
    <div class="header">
        <img src="/static/images/logo.jpg" class="logo" alt="ACIS logo" />
        <img src="/static/images/slogan.gif" class="slogan" alt="Artificial Caves Investigation System" />
    </div>
    <div class="menu" id="acisMenu">
        {% if user.is_authenticated %}
            <p class="greeting">Вы вошли как: <strong><a href="{% url 'profile' %}">{{ user.username }}</a></strong></p>
        {% endif %}
    </div>
    <div class="navbar">
        <ul class="breadcrumbs">
            <li><a href="{% url 'post_list' %}">Главная</a></li>
            <li class="sep">&#187;</li>
            <li class="current">Форум</li>
        </ul>

        <form action="{% url 'set_language' %}" class="langSwitcher" method="post">{% csrf_token %}
            <input name="next" type="hidden" value="{{ redirect_to }}" />
            <input name="language" type="hidden" value="{{ LANGUAGE_CODE }}">
            <ul>
                {% get_current_language as LANGUAGE_CODE %}
                {% get_available_languages as LANGUAGES %}
                {% get_language_info_list for LANGUAGES as languages %}
                {% for language in languages %}
                    <li class="langBtn{% if language.code == LANGUAGE_CODE %} selected{% endif %}" id="{{ language.code }}">
                        <a href="#" title="{{ language.name_local }} ({{ language.code }})">
                            <img src="{% static 'images/locale/' %}{{ language.code }}.png" alt="{{ language.code }}" />
                        </a>
                    </li>
                {% endfor %}
            </ul>
        </form>
    </div>
    <div class="main">
        <!--boms -->

        <div id="brd-wrap" class="brd">
            <div <!-- forum_page -->>
                <div id="brd-navlinks" class="gen-content">
                	<!-- forum_navlinks -->
                	<!-- forum_admod -->
                </div>

                <!-- forum_announcement -->

                <div class="hr"><hr /></div>

                <div id="brd-main">
                	<!-- forum_main_title -->
                	<!-- forum_crumbs_top -->
                	<!-- forum_main_menu -->
                	<!-- forum_main_pagepost_top -->
                	<!-- forum_main -->
                	<!-- forum_main_pagepost_end -->
                	<!-- forum_crumbs_end -->
                </div>
                <!-- forum_qpost -->

                <div id="brd-visit" class="gen-content">
                	<!-- forum_welcome -->
                	<!-- forum_visit -->
                </div>

                <div id="weather" class="gen-content">
                    <!-- forum_weather -->
                </div>

                <!-- forum_info -->

                <div class="hr"><hr /></div>

                <div id="brd-about" class="gen-content">
        	        <!-- forum_about -->
                </div>

                <!-- forum_debug -->


        </div>

        <!--eoms -->

        <p>&nbsp;</p>
        <p>&nbsp;</p>
    </div>
    <div class="footer">
        Copyright © 2001-2016 ACIS
    </div>
</div>

<script type="text/javascript">
var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
</script>
<script type="text/javascript">
var pageTracker = _gat._getTracker("UA-2699312-1");
pageTracker._initData();
pageTracker._trackPageview();
</script>

<script src="/static/js/menu.js"></script>
<script src="/static/js/misc.js"></script>

<script>
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
</script>
</body>
</html>