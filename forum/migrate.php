<?php
if (!defined('FORUM_ROOT'))
	define('FORUM_ROOT', './');
require FORUM_ROOT.'include/common.php';


$query = array(
	'SELECT'	=> '*',
	'FROM'		=> 'messages AS m',
);

$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);


$posts = array();
while($post = $forum_db->fetch_assoc($result)) {
	$posts[] = $post;
	
}

//print_r($posts);exit;

foreach ($posts as $cur_post)
{
		
	$cur_post['read'] = ($cur_post['showed'] == 1) ? $cur_post['posted'] : 0;
	$cur_post['status'] = ($cur_post['showed'] == 1) ? 'read' : 'sent';
		
	$query = array(
		'INSERT'	=> 'sender_id, receiver_id, lastedited_at, read_at, subject, body, status',
		'INTO'		=> 'pun_pm_messages',
		'VALUES'	=> '\''.$cur_post['sender_id']
		.'\', \''.$cur_post['owner']
		.'\', \''.$cur_post['posted']
		.'\', \''.$cur_post['read']
		.'\', \''.$forum_db->escape($cur_post['subject'])
		.'\', \''.$forum_db->escape($cur_post['message'])
		.'\', \''.$forum_db->escape($cur_post['status']).'\''
	);

	//$result = $forum_db->query_build($query, true);	echo $result;
	$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);
}

echo 'End';
?>
