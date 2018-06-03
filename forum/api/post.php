<?php
/**
 * Спецификация API размещения поста, GR01, rev. 1.

 Аргументы - topic_id, text, { user_id, display_name }.
 Результат - post_id или -1 в случае ошибки.

 Если задан user_id - текстовое имя автора подтягивается как обычно из таблицы `users` (номер привязан)
 Если user_id не задан - пост создаётся из-под аккаунта по умолчанию
 Если задан display_name и не задан user_id - пост создаётся из-под аккаунта по умолчанию, а в поле имени прописывается display_name.

 */

// Аккаунт гостя (ID = 1) или другой аккаунт, из-под которого будут поститься сообщения без привязки к пользователю 
define('API_DEFAULT_USER', 1);

// Имя пользователя по умолчанию
define('API_DEFAULT_USERNAME', 'Метеонаблюдатель');

// Префикс перед именем пользователя, чтобы отличать посты сделанные через API от обычных постов
define('API_USERNAME_PREFIX', '');


//////System constants, should be before the function call.
define('FORUM_SKIP_CSRF_CONFIRM', 1);


if (!defined('FORUM_ROOT'))	
    define('FORUM_ROOT', (dirname(dirname(__FILE__)).'/'));

chdir(FORUM_ROOT);

require FORUM_ROOT.'include/common.php';

//////

// Uncomment for debug
/*
$data = array('topic_id' => 77650,
		'text' => 'Гроза над Шулявкою! Рухається в західному напрямку',
		'user_id' => '',
		'display_name' => 'Вася');
echo make_new_post($data);
*/


//////////////////////////////////////////////////////////////////////////////////////////
if(isset($_REQUEST['mkpost']))
{
    echo make_new_post(json_decode($_REQUEST['msg'], true));
}
//////////////////////////////////////////////////////////////////////////////////////////


function make_new_post($data) {
global $forum_db, $forum_config;


if (!isset($data)) {
	$data = $_POST;
}

$tid     = isset($data['topic_id']) ? intval($data['topic_id']) : 0;
$text    = isset($data['text']) ? $data['text'] : '';
$user_id = isset($data['user_id']) ? intval($data['user_id']) : API_DEFAULT_USER;
$display_name = isset($data['display_name']) ? $data['display_name'] : '';

if ($tid == 0 || empty($text)) {
	return -1; 
}

//Get some user data
$query = array(
		'SELECT'	=> 'u.*, g.*',
		'FROM'		=> 'users AS u',
		'JOINS'		=> array(
				array(
						'INNER JOIN'	=> 'groups AS g',
						'ON'			=> 'g.g_id=u.group_id'
				)
		),
		'WHERE' =>  'u.id='.$user_id
);
$result = $forum_db->query_build($query);

if (!$result) {
  return -1;
}
$forum_user = $forum_db->fetch_assoc($result);


if (!isset($forum_user['id'])) {
	//Set default user
	$query = array(
			'SELECT'	=> 'u.*, g.*',
			'FROM'		=> 'users AS u',
			'JOINS'		=> array(
					array(
							'INNER JOIN'	=> 'groups AS g',
							'ON'			=> 'g.g_id=u.group_id'
					)
			),
			'WHERE' =>  'u.id='.API_DEFAULT_USER
	);

	$result = $forum_db->query_build($query) or die(-1);

	$forum_user = $forum_db->fetch_assoc($result);
}

if ($forum_user['id'] == 1) {

	$forum_user['timezone'] = $forum_config['o_default_timezone'];
	$forum_user['dst'] = $forum_config['o_default_dst'];
	$forum_user['is_guest'] = true;
	$forum_user['is_admmod'] = false;

} else {
	$forum_user['is_guest'] = false;
}

if ($forum_user['id'] == API_DEFAULT_USER) {
	$forum_user['username'] = !empty($display_name) ? $display_name : API_DEFAULT_USERNAME;
}

// Fetch some info about the topic and/or the forum

$query = array(
		'SELECT'	=> 'f.id, f.forum_name, f.moderators, f.redirect_url, t.subject, t.closed',
		'FROM'		=> 'topics AS t',
		'JOINS'		=> array(
				array(
						'INNER JOIN'	=> 'forums AS f',
						'ON'			=> 'f.id=t.forum_id'
				)
		),
		'WHERE'		=> 't.id='.$tid
);


$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);
 
if (!$forum_db->num_rows($result)) {
	return -1; 
}

$cur_posting = $forum_db->fetch_assoc($result);
$cur_posting['post_approval'] = 0;

// Start with a clean slate
$errors = array();

$username = $forum_user['username'];
$email = $forum_user['email'];

// Clean up message from POST
$message = forum_linebreaks(forum_trim($text));

if (strlen($message) > FORUM_MAX_POSTSIZE_BYTES)
	$errors[] = sprintf('Message should be shorder than %d', forum_number_format(strlen($message)), forum_number_format(FORUM_MAX_POSTSIZE_BYTES));

// Validate BBCode syntax
if ($forum_config['p_message_bbcode'] == '1' || $forum_config['o_make_links'] == '1')
{
	if (!defined('FORUM_PARSER_LOADED'))
		require FORUM_ROOT.'include/parser.php';

	$message = preparse_bbcode($message, $errors);
}

if ($message == '') {
	$errors[] = 'No message';
}

$now = time();

// Did everything go according to plan?
if (empty($errors))
{
	// If it's a reply
	if ($tid)
	{
		$post_info = array(
				'is_guest'		=> $forum_user['is_guest'],
				'poster'		=> API_USERNAME_PREFIX . $username,
				'poster_id'		=> $forum_user['id'],	// Always 1 for guest posts
				'poster_email'	=> ($forum_user['is_guest'] && $email != '') ? $email : null,	// Always null for non-guest posts
				'subject'		=> $cur_posting['subject'],
				'message'		=> $message,
				'hide_smilies'	=> 0,
				'posted'		=> $now,
				'subscr_action'	=> 0,
				'topic_id'		=> $tid,
				'forum_id'		=> $cur_posting['id'],
				'update_user'	=> true,
				'update_unread'	=> true
		);

		add_post($post_info, $new_pid);
	}
} else {
	return -1; 
}

return $new_pid;

}
