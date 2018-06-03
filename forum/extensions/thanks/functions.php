<?php

/**
 * core thanks
 * 
 * @partially based on code copyright (C) 2009 hcs reputation extension for PunBB (C)
 * @copyright Copyright (C) 2008 PunBB, partially based on code copyright (C) 2008 FluxBB.org
 * @license http://www.gnu.org/licenses/gpl.html GPL version 2 or higher
 * @package thanks
 */

if (!defined('FORUM'))
	die();

function thank($post_id) {
	global $lang_thanks, $forum_db, $forum_user;
	
	$user_thanked_id = $forum_user['id'];
	
	if (empty($user_id) && empty($post_id))
		$error = $lang_thanks['error_00'];
	else if ($user_thanked_id == 1)
		$error = $lang_thanks['error_01'];
	else
	{
		$query = array(
				'SELECT'	=> 'poster, poster_id, posted',
				'FROM'		=> 'posts',
				'WHERE'		=> 'id='.$post_id
		);
		$result = $forum_db->query_build($query) or $error = $lang_thanks['error_06'];
		$res = $forum_db->fetch_assoc($result);
	
		if (!$forum_db->num_rows($result))
			$error =  $lang_thanks['error_03'];
	}
	
	if (empty($error)) {
		if ($res['poster_id'] == $user_thanked_id) {
			$error = $lang_thanks['error_02'];
		} else if (time() - $res['posted'] > 1209600) {
			$error = $lang_thanks['error_07'];
		}
	}
	
	if (empty($error)) {
		$query = array(
				'SELECT'	=> 'user_thanked_id, post_id',
				'FROM'		=> 'thanks',
				'WHERE'		=> 'post_id='.$post_id.' AND user_thanked_id='.$user_thanked_id
		);
		$result = $forum_db->query_build($query) or $error = $lang_thanks['error_06'];
		$say_thanks = sprintf($lang_thanks['error_04'], $res['poster']);
		if ($forum_db->num_rows($result) > 0) $error = $say_thanks;
	}
	
	if (empty($error))
	{
		$query = array(
				'INSERT'	=> 'user_id, user_thanked_id, post_id, thank_date',
				'INTO'		=> 'thanks',
				'VALUES'	=> $res['poster_id'].', '.$user_thanked_id.', '.$post_id.', '.time()
		);
		$forum_db->query_build($query) or $error = $lang_thanks['error_06'];
		$query2 = array(
				'UPDATE'	=> 'posts',
				'SET'		=> 'thanks=thanks+1',
				'WHERE'		=> 'id='.$post_id
		);
		$forum_db->query_build($query2) or $error = $lang_thanks['error_06'];
	}
	
	if (empty($error)) {
		show_thanks($post_id);
	} else {
		echo $error;
	}
}

function show_thanks($post_id) {
	global $forum_db, $lang_thanks;
	
	$UserThanks = '';
	
	$query_thanks = array(
			'SELECT'	=> 't.thank_date, u.username',
			'FROM'		=> 'thanks AS t',
			'JOINS'		=> array(
					array(
							'INNER JOIN'	=> 'users AS u',
							'ON'			=> 't.user_thanked_id=u.id'
					)),
			'WHERE'		=> 't.post_id='.$post_id
	);

	$result_thanks = $forum_db->query_build($query_thanks) or error(__FILE__, __LINE__);
	if (!$forum_db->num_rows($result_thanks) > 0)
		$error =  $lang_thanks['error_03'];
	else
	{
		$counter = 0;
		$total   = $forum_db->num_rows($result_thanks);
		
		$UserThanks = '<b>+'.$total.': </b>';

		while ($row = $forum_db->fetch_assoc($result_thanks))
		{
			//$timeT = date( 'd-m-Y H:h', $row['thank_date']);

			$UserThanks .= ' '.$row['username'];
			$counter++;

			if ($counter < $total) {
				$UserThanks .= ', ';
			}
		}
	}
	if (empty($error)) exit ($UserThanks);
	else  exit($error);

}


