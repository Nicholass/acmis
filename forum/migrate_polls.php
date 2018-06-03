<?php
if (!defined('FORUM_ROOT'))
	define('FORUM_ROOT', './');
require FORUM_ROOT.'include/common.php';


$query = array(
	'SELECT'	=> '*',
	'FROM'		=> 'polls ',
	'WHERE'		=> 'users_votes != \'\' AND ptype = 1',
	
);
$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);

$polls = array();
while ($poll = $forum_db->fetch_assoc($result)) {
	$polls[$poll['pollid']] = $poll;
}


$query = array(
	'SELECT'	=> 'id, question, posted',
	'FROM'		=> 'topics ',
	'WHERE'		=> 'question != \'\'',
);
$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);

$questions = array();
while ($row = $forum_db->fetch_assoc($result)) {
	$polls[$row["id"]]['question'] = $row['question'];
	$polls[$row["id"]]['created'] = $row['posted'];
}

print_r($polls);

//exit;

foreach ($polls as $topic_id => $cur_poll)
{

	if (!isset($cur_poll['created'])) {
		continue;
	}
	if (!isset($cur_poll['options'])) {
		continue;
	}
	
	print_r($cur_poll);
	

	$questions = unserialize($cur_poll['options']);
		if ($errno) exit;
	$votings = unserialize($cur_poll['users_votes']);
		if (error_get_last()) exit;
	print_r($questions);
	print_r($votings);
	
	
	
	
	//exit;
	
	$query = array(
		'INSERT'	=> 'read_unvote_users, revote, topic_id, question, created',
		'INTO'		=> 'questions',
		'VALUES'	=> 
		' \''. '0'
		.'\', \''. '0'
		.'\', \''.$topic_id
		.'\', \''.$forum_db->escape($cur_poll['question'])
		.'\', \''.$cur_poll['created'].'\''
	);
	
	$result = $forum_db->query_build($query);	echo $result; 

	foreach ($questions as $question) {
		$query = array(
			'INSERT'	=> 'topic_id, answer',
			'INTO'		=> 'answers',
			'VALUES'	=> 
			' \''.$topic_id
			.'\', \''.$forum_db->escape($question).'\''
		);
		$forum_db->query_build($query);
	}
	
	foreach ($questions as $question_id => $question) {
		$query = array(
			'SELECT'	=> 'id',
			'FROM'		=> 'answers',
			'WHERE'		=> 'answer = \''.$forum_db->escape($question).'\'',
		);
		$result = $forum_db->query_build($query);
		$new_answer = $forum_db->fetch_assoc($result);
		
		$new_answer_ids[$question_id] = $new_answer['id'];
		//прив'язати до votings
	}
	
	$new_answers = array();
	
	foreach ($votings as $voting) {
		$user_id = $voting[0];
		foreach ($voting[1] as $key => $value) {
			$old_answer_id  = $key;
		}
		$answer_id = $new_answer_ids[$old_answer_id];
		
		$query = array(
			'INSERT'	=> 'topic_id, user_id, answer_id',
			'INTO'		=> 'voting',
			'VALUES'	=> 
			' \''.$topic_id
			.'\', \''.$user_id.'\''
			.'\', \''.$answer_id.'\''
		);
		$forum_db->query_build($query);
	}

}

echo 'End';
?>
