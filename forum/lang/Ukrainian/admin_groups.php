<?php

// Language definitions used in all admin files
//Translate by vart (forum.politclub.org)

$lang_admin_groups = array(

// admin_groups
'Group settings heading'		 => 'Налаштування групи, які діють у разі неперекриття їх особливими налаштуваннями форуму',    //Group's default permission that apply when no forum specific permissions are set
'Group title label' 			 => 'Назва групи',    //Group title
'User title label'  			 => 'Звання користувачів',    //User title
'Group title head'  			 => 'Назва групи та звання користувачів',    //Group and user title
'Group title legend'			 => 'Встановлення заголовків та звань',    //Set titles
'Group perms head'  			 => 'Права користувачів групи',    //Group permissions
'Group flood head'  			 => 'Встановлення часових інтервалів для користувачів групи',    //Group flood protection settings
'User title help'   			 => 'Це звання перекриє будь-які ранги користувачів, що входять до цієї групи. Залиште порожнім, якщо не бажаєте змінювати ранги.',    //This title will override any rank users in this group have attained. Leave blank to use default title or rank.
'Remove group legend'   		 => 'Видалення групи',    //Remove group
'Permissions'   				 => 'Права',    //Permissions
'Moderation'					 => 'Модерування',    //Moderation
'Allow moderate label'  		 => 'Дозволити модерування користувачів.',    //Allow users moderator privileges.
'Allow mod edit profiles label'  => 'Дозволити зміну профілів користувачів.',    //Allow moderators to edit user profiles.
'Allow mod edit username label'  => 'Дозволити зміну імен користувачів.',    //Allow moderators to rename users.
'Allow mod change pass label'    => 'Дозволити зміну паролів користувачів.',    //Allow moderators to change user passwords.
'Allow mod bans label'  		 => 'Дозволити блокування користувачів.',    //Allow moderators to ban users.
'Allow read board label'		 => 'Дозволити перегляд форуму.',    //Allow users to view the board.
'Allow read board help' 		 => 'Ця опція застосовується до вього форуму і не може бути (при вимкненні) перекрита особливими налаштуваннями форуму. Якщо вона вимкнена, то користувачі цієї групи зможуть тільки входити/виходити з форуму та реєструватися.',    //This setting applies to every aspect of the board and can, if disabled, not be overridden by forum specific read permissions. If this is disabled, users in this group will only be able to login/logout and register.
'Allow view users label'		 => 'Дозволити перегляд списку користувачів та їх профілів.',    //Allow users to view the user list and user profiles.
'Allow post replies label'  	 => 'Дозволити відповідати в темах.',    //Allow users to post replies in topics.
'Allow post topics label'   	 => 'Дозволити створення нових тем.',    //Allow users to post new topics.
'Allow edit posts label'		 => 'Дозволити редагування власних повідомлень.',    //Allow users to edit their own posts.
'Allow delete posts label'  	 => 'Дозволити видалення власних повідомлень.',    //Allow users to delete their own posts.
'Allow delete topics label' 	 => 'Дозволити видалення власних тем (зі всіма відповідями включно).',    //Allow users to delete their own topics (including any replies).
'Allow set user title label'	 => 'Дозволити редагування власних звань.',    //Allow users to set their own user titles.
'Allow use search label'		 => 'Дозволити використання пошуку.',    //Allow users to use the search feature.
'Allow search users label'  	 => 'Дозволити використання текстового пошуку користувачів.',    //Allow users to freetext search for users in the user list.
'Allow send email label'		 => 'Дозволити надсилання e-mail повідомлень іншим користувачам.',    //Allow users to send e-mails to other users.
'Restrictions'  				 => 'Обмеження',    //Restrictions
'Mod permissions'   			 => 'Права модераторів',    //Moderator permissions
'User permissions'  			 => 'Права користувачів',    //User permissions
'Flood interval label'  		 => 'Часовий інтервал між повідомленнями',    //Post flood interval
'Flood interval help'   		 => 'Кількість секунд, що мають минути між повідомленнями користувачів цієї групи. Встановіть 0 для вимкнення.',    //Number of seconds that users in this group have to wait between posts. Set to 0 to disable.
'Search interval label' 		 => 'Часовий інтервал між пошуками',    //Search flood interval
'Search interval help'  		 => 'Кількість секунд, що мають минути між спробами здійснення пошуку на форумі користувачами цієї групи. Встановіть 0 для вимкнення.',    //Number of seconds that users in this group have to wait between searches. Set to 0 to disable.
'Email flood interval label'	 => 'Часовий інтервал між e-mail повідомленнями',    //Email flood interval
'Email flood interval help' 	 => 'Кількість секунд, що мають минути між e-mail повідомленнями користувачів цієї групи. Встановіть 0 для вимкнення.',    //Number of seconds that users in this group have to wait between e-mails. Set to 0 to disable.
'Allow moderate help'   		 => 'Для надання користувачеві можливостей модератора він має бути призначений модератором хоча б одного форуму. Це можливо зробити на сторінці адміністрування користувача, обравши вкладу Адміністрування в профілі користувача.',    //In order for a user in this group to have moderator abilities, he/she must be assigned to moderate one or more forums. This is done via the user administration page of the user's profile.
'Remove group'  				 => 'Видалити цю групу',    //Remove this group
'Edit group'					 => 'Редагувати цю групу',    //Edit this group
'default'   					 => '(за замовчуванням)',    //(default)
'Cannot remove group'   		 => 'Ця група не може бути видалена.',    //This group cannot be removed.
'Cannot remove default' 		 => 'Для видалення цієї групи необхідно призначити іншу групу "за замовчуванням".',    //To remove this group you must assign a new default group.
'Remove group head' 			 => 'Видалення групи "%s" з кількістю користувачів %s',    //Remove "%s" group which contains %s members
'Remove group help' 			 => '(Перемістити поточних користувачів до цієї групи)',    //(Transfer current members to this group)
'Move users to' 				 => 'Перемістити користувачів до групи',    //Move users to
'Cannot remove default group'    => 'Група "за замовчуванням" не може бути видалена. Для видалення цієї групи необхідно призначити іншу групу "за замовчуванням".',    //The default group cannot be removed. In order to delete this group, you must first setup a different group as the default.
'Add group heading' 			 => 'Додавання нової групи (успадкує права тієї групи, на базі якої буде створена)',    //Add new group (will inherit the permissions of the group it is based on)
'Add group legend'  			 => 'Додати нову групу',    //Add new group
'Edit group heading'			 => 'Редагування існуючої групи',    //Edit existing group
'Base new group label'  		 => 'Базова група',    //Base new group on
'Add group' 					 => 'Додати нову групу',    //Add new group
'Default group heading' 		 => 'Група "за замовчуванням" для нових користувачів (групи адміністраторів та модераторів недоступні з міркувань безпеки)',    //Default group for new users (administrator/moderator groups not available for security reasons)
'Default group legend'  		 => 'Призначити групу "за замовчуванням" для нових користувачів',    //Set default group for new users
'Default group label'   		 => 'Група "за замовчуванням"',    //Default group
'Set default'   				 => 'Призначити групу',    //Set default group
'Existing groups heading'   	 => 'Існуючі групи',    //Existing groups
'Existing groups intro' 		 => 'Групи Гостей та Адміністраторів не можуть бути видалені, проте можуть бути редаговані. Пам\'ятайте, що у деяких групах певні налаштування недоступні (наприклад, право редагування для Гостей). Адміністратори завжди мають повні права.',    //The pre-defined groups Guests and Administrators cannot be removed. They can however be edited. Please note though, that in some groups, certain options are unavailable (e.g. the "edit posts" permission for guests). Administrators always have full permissions.
'Group removed' 				 => 'Групу видалено.',    //Group removed.
'Default group set' 			 => 'Групу "за замовчуванням" призначено.',    //Default group set.
'Group added'   				 => 'Групу додано.',    //Group added.
'Group edited'  				 => 'Групу відредаговано.',    //Group edited.
'Update group'  				 => 'Надіслати',    //Update group
'Must enter group message'  	 => 'Ви повинні ввести назву групи.',    //You must enter a group title.
'Already a group message'   	 => 'Група <strong>"%s"</strong> вже існує.',    //There is already a group with the title <strong>"%s"</strong>.
'Moderator default group'   	 => 'Це група "за замовчуванням" для нових користувачів. Вона не може мати модераторські права.',    //This is the default group for new users and therefore cannot be assigned moderator privileges.

);
