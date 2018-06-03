<?php

function fancy_pm_notification_get_unread_count() {
	global $forum_db, $forum_user, $forum_config, $lang_pun_pm, $pun_pm_inbox_full;

	list($new_messages, $pun_pm_inbox_full) = pun_pm_read_cache();

	if ($new_messages === FALSE) {
		pun_pm_deliver_messages();

		//How much delivered messages do we have?
		$query = array(
			'SELECT'	=> 'count(id)',
			'FROM'		=> 'pun_pm_messages',
			'WHERE'		=> 'receiver_id = '.$forum_user['id'].' AND status = \'delivered\' AND deleted_by_receiver = 0'
		);

		$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);

		list($new_messages) = $forum_db->fetch_row($result);

		pun_pm_write_cache($forum_user['id'], $new_messages, $pun_pm_inbox_full);
	}

	return $new_messages ? intval($new_messages, 10) : 0;
}

?>
