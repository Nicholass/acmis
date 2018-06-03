<?php

// Language definitions for frequently used strings
//Translate by vart (forum.politclub.org)

$lang_common = array(

// Text orientation and encoding
'lang_direction'			=>	'ltr',	// ltr (Left-To-Right) or rtl (Right-To-Left)
'lang_identifier'			=>	'ua',

// Number formatting
'lang_decimal_point'	=>	',',
'lang_thousands_sep'	=>	' ',

// Notices
'Bad request'				=>	'Хибний запит. Посилання некоректне або застаріле.',
'No view'				=>	'Ви не маєте прав доступу для перегляду цих форумів.',
'No permission'				=>	'Ви не маєте прав доступу до цієї сторінки.',
'CSRF token mismatch'		=>	'Неможливо підтвердити безпеку з\'єднання. Вірогідно це трапилось через те, що між входом на сторінку та відправленням даних минув деякий час. Якщо ви бажаєте продовжити виконання дії, будь ласка, натисніть на кнопку Підтвердити. В іншому випадку ви маєте натиснути на кнопку Скасувати, щоб повернутися у те місце, де перебували.',
'No cookie'				=>	'Здається ви зареєструвалися успішно, проте cookie не були встановлені. Будь ласка, перевірте параметри налаштування та, якщо це можливо, увімкніть cookie для цього веб-сайту.',


// Miscellaneous
'Forum index'				=>	'Список форумів',	// Forum index
'Submit'					=>	'Надіслати',	// "name" of submit buttons
'Cancel'					=>	'Скасувати', // "name" of cancel buttons
'Preview'					=>	'Перегляд',	// submit button to preview message
'Delete'					=>	'Видалити',
'Split'					=>	'Розбити',	//Split
'Ban message'				=>	'Ви були забанені на цьому форумі.',
'Ban message 2'				=>	'Термін закінчення бану %s.',
'Ban message 3'				=>	'Адміністратор або модератор, який вас забанив, залишив таке повідомлення:',
'Ban message 4'				=>	'Будь ласка, спрямовуйте будь-які запити до адміністратора форуму за адресою %s.',
'Never'						=>	'Ніколи',
'Today'						=>	'Сьогодні',
'Yesterday'					=>	'Вчора',
'Forum message'				=>	'Повідомлення форуму',
'Maintenance warning'		=>	'<strong>УВАГА! %s увімкнено.</strong> НЕ ВИХОДЬТЕ З ФОРУМУ, оскільки ви не зможете увійти до форуму знову.',
'Maintenance mode'			=>	'Режим обслуговування',
'Redirecting'				=>	'Перенаправлення',
'Forwarding info'			=>	'Вас буде автоматично перенаправлено на нову сторінку за %s %s.',
'second'					=>	'секунду',	// singular
'seconds'					=>	'секунд(и)',	// plural
'Click redirect'			=>	'Натисніть сюди, якщо ви не бажаєте чекати довше (або якщо ваш переглядач не пересилає вас автоматично)',
'Invalid e-mail'			=>	'Ви ввели хибну e-mail адресу.',
'New posts'					=>	'Нові повідомлення',	// the link that leads to the first new post
'New posts title'			=>	'Знайти теми, які містять повідомлення, залишені з моменту вашого останнього візиту.',	// the popup text for new posts links
'Active topics'				=>	'Активні теми',
'Active topics title'		=>	'Знайти теми, які містять останні повідомлення.',
'Unanswered topics'			=>	'Теми без відповідей',
'Unanswered topics title'	=>	'Знайти теми без відповідей.',
'Username'					=>	'Ім\'я користувача',
'Registered'				=>	'Зареєстровано',
'Write message'				=>	'Напишіть повідомлення',
'Forum'						=>	'Форум',
'Posts'						=>	'Повідомлення',
'Pages'						=>	'Сторінки',
'Page'						=>	'Сторінка',
'BBCode'					=>	'BBCode',	// You probably shouldn't change this
'Smilies'					=>	'Посмішки',
'Images'					=>	'Зображення',
'You may use'				=>	'Ви можете використовувати: %s',
'and'						=>	'та',
'Image link'				=>	'зображення',	// This is displayed (i.e. <image>) instead of images when "Show images" is disabled in the profile
'wrote'						=>	'написав',	// For [quote]'s (e.g., User wrote:)
'Code'						=>	'Код',		// For [code]'s
'Forum mailer'				=>	'%s поштовик',	// As in "MyForums Mailer" in the signature of outgoing e-mails
'Write message legend'		=>	'Додайте ваше повідомлення',
'Required information'		=>	'Необхідна інформація',
'Reqmark'					=>	'*',
'Required'					=>	'(обов\'язкове поле)',
'Required warn'				=>	'Усі поля, позначені %s, повинні бути заповнені перед відправленням форми.',
'Crumb separator'			=>	' »&#160;', // The character or text that separates links in breadcrumbs
'Title separator'			=>	' &mdash; ',
'Page separator'			=>	'&#160;', //The character or text that separates page numbers
'Spacer'					=>	'…', // Ellipsis for paginate
'Paging separator'			=>	' ', //The character or text that separates page numbers for page navigation generally
'Previous'					=>	'Попередня',
'Next'					=>	'Наступна',
'Cancel redirect'			=>	'Дію скасовано. Перенаправлення...',
'No confirm redirect'		=>	'Підтвердження не забезпечено. Дію скасовано. Перенаправлення...',
'Please confirm'			=>	'Будь ласка, підтвердіть:',
'Help page'					=>	'Допомога: %s',
'Re'						=>	'Re:',
'Page info'					=>	'(Сторінка %1$s з %2$s)',
'Item info single'			=>	'%s [ %s ]',
'Item info plural'			=>	'%s [з %s по %s із %s ]', // e.g. Topics [ 10 to 20 of 30 ]
'Info separator'			=>	' | ', // e.g. 1 Page | 10 Topics
'Powered by'				=>	'Працює на <strong>%s</strong>',
'Maintenance'				=>	'Обслуговування',
'Installed extension'		=>	'Офіційних розширень встановлено: %s. Copyright &copy; 2003&ndash;2011 <a href="http://punbb.informer.com/">PunBB</a>.',
'Installed extensions'		=>	'Встановлено <span id="extensions-used" title="%s">%s офіційних розширень.</span>. Copyright &copy; 2003&ndash;2011 <a href="http://punbb.informer.com/">PunBB</a>.',

// CSRF confirmation form
'Confirm'					=>	'Підтвердити',	// Button
'Confirm action'			=>	'Підтвердити дію',
'Confirm action head'		=>	'Будь ласка, підтвердіть або скасуйте вашу останню дію',

// Title
'Title'						=>	'Заголовок',
'Member'					=>	'Учасник',	// Default title
'Moderator'					=>	'Модератор',
'Administrator'				=>	'Адміністратор',
'Banned'					=>	'Забанений',
'Guest'						=>	'Гість',

// Stuff for include/parser.php
'BBCode error 1'			=>	'[/%1$s] було знайдено без співпадінь [%1$s]',
'BBCode error 2'			=>	'Тег [%s] порожній',	//tag is empty
'BBCode error 3'			=>	'[%1$s] було відкрито всередині [%2$s], що не дозволено',
'BBCode error 4'			=>	'[%s] було відкрито всередині себе, що не дозволено',
'BBCode error 5'			=>	'[%1$s] було знайдено без співпадінь [/%1$s]',
'BBCode error 6'			=>	'Тег [%s] має порожню секцію властивостей',
'BBCode nested list'		=>	'Теги [list] не можуть бути вкладені',
'BBCode code problem'		=>	'Проблема з тегами [code]',

// Stuff for the navigator (top of every page)
'Index'						=>	'Головна',
'User list'					=>	'Користувачі',
'Rules'						=>  'Правила',
'Search'					=>  'Пошук',
'Register'					=>  'Реєстрація',
'register'					=>	'зареєструватися',
'Login'						=>  'Вхід',
'login'						=>	'увійти',
'Not logged in'				=>  'Ви не увійшли.',
'Profile'					=>	'Профіль',
'Logout'					=>	'Вийти',
'Logged in as'				=>	'Ви увішли як %s.',
'Admin'						=>	'Адміністрування',
'Last visit'				=>	'Ваш останній візит: %s',
'Mark all as read'			=>	'Помітити всі теми як прочитані',
'Login nag'					=>	'Будь ласка, увійдіть або зареєструйтеся.',
'New reports'				=>	'Нові скарги',

// Alerts
'New alerts'				=>	'Нові попередження',	//Alerts
'Maintenance alert'			=>	'<strong>УВАГА! Режим обслуговування увімкнено.</strong> На разі форуми знаходяться в режимі обслуговування. <em>НЕ ВИХОДЬТЕ З ФОРУМУ</em>, бо не зможете зайти до нього знову.',
'Updates'					=>	'PunBB оновлення',
'Updates failed'			=>	'Остання спроба перевірки оновлень на сервісі punbb.informer.com була невдалою. Ймовірно, це означає, що сервіс оновлень тимчасово перевантажено. Проте, якщо це попередження не зникає більше двох діб, ви маєте перевірити наявність оновлень у ручному режимі.',
'Updates version n hf'		=>	'Нова версія PunBB (версія %s) доступна для завантаження на <a href="http://punbb.informer.com/">punbb.informer.com</a>. До того ж, одне або більше виправлених розширень доступні для встановлення на вкладці Розширення панелі адміністрування.',
'Updates version'			=>	'Новіша версія PunBB (версія %s) доступна для завантаження на <a href="http://punbb.informer.com/">punbb.informer.com</a>.',
'Updates hf'				=>	'Одне або більше виправлених розширень доступні для встановлення на вкладці Розширення панелі адміністрування.',
'Database mismatch'			=>	'Невідповідність версії бази даних',
'Database mismatch alert'	=>	'Ваша поточна база даних працює спільно з новою версією PunBB. Ця невідповідність може призводити до некоректної роботи вашого форуму. Це означає, що ви маєте оновити свій форум до найновішої версії PunBB.',

// Stuff for Jump Menu
'Go'						=>	'Перейти',		// submit button in forum jump
'Jump to'					=>	'Перейти до форуму:',

// For extern.php RSS feed
'RSS description'			=>	'Останні теми у %s.',
'RSS description topic'		=>	'Останні повідомлення у %s.',
'RSS reply'					=>	'Re: ',	// The topic subject will be appended to this string (to signify a reply)

// Accessibility
'Skip to content'					=>	'Перейти до вмісту форуму',

// Debug information
'Querytime'						=>	'Згенеровано за %1$s секунди, виконано %2$s запитів',
'Debug table'						=>	'Інформація для розробника',
'Debug summary'						=>	'Інформація про оброблення запитів до бази даних',
'Query times'						=>	'Час (сек.)',
'Query'							=>	'Запит',
'Total query time'					=>	'Загальний час запиту'

);
