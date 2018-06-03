<?php
/***********************************************************************

  PunBB extension
  "Deleted Posts Log" v3.2b
  
  (C) Franz Liedke 2008
  lie2815@yahoo.de

************************************************************************/


if (!defined('FORUM_ROOT'))
	define('FORUM_ROOT', '../../');
require FORUM_ROOT.'include/common.php';
require FORUM_ROOT.'include/common_admin.php';

if (!$forum_user['is_admmod'])
	message($lang_common['No permission']);

// Load the admin.php language file
require FORUM_ROOT.'lang/'.$forum_user['language'].'/admin_common.php';

//
// Generate a string with numbered links (modified paginate function from PunBB's core)
//
function deletedpostslog_paginate($num_pages, $cur_page, $link)
{
	global $base_url, $lang_common;
	
	$pages = array();
		
	if ($num_pages <= 1)
		$pages = array('<strong>1</strong>');
	else
	{
		// Add a previous page link
		if ($num_pages > 1 && $cur_page > 1)
			$pages[] = '<a class="prev" href="'.$base_url.$link.'?p='.($cur_page - 1).'#log">'.$lang_common['Previous'].'</a>&#160;';

		if ($cur_page > 3)
		{
			$pages[] = '<a href="'.$base_url.$link.'?p=1#log">1</a>';

			if ($cur_page > 5)
				$pages[] = '&#8230;';
		}

		// Don't ask me how the following works. It just does, OK? :-)
		for ($current = ($cur_page == 5) ? $cur_page - 3 : $cur_page - 2, $stop = ($cur_page + 4 == $num_pages) ? $cur_page + 4 : $cur_page + 3; $current < $stop; ++$current)
		{
			if ($current < 1 || $current > $num_pages)
				continue;
			else if ($current != $cur_page)
				$pages[] = '<a href="'.$base_url.$link.'?p='.$current.'#log">'.$current.'</a>';
			else
				$pages[] = '<strong>'.$current.'</strong>';
		}
		if ($cur_page <= ($num_pages-3))
		{
			if ($cur_page != ($num_pages-3) && $cur_page != ($num_pages-4))
				$pages[] = '&#8230;';

			$pages[] = '<a href="'.$base_url.$link.'?p='.$num_pages.'#log">'.$num_pages.'</a>';
		}

		// Add a next page link
		if ($num_pages > 1 && $cur_page < $num_pages)
			$pages[] = '&#160;<a class="next" href="'.$base_url.$link.'?p='.($cur_page + 1).'#log">'.$lang_common['Next'].'</a>';
	}

	return implode('&#160;', $pages);
}


if (isset($_POST['options']))
{
	$parse_log = isset($_POST['form']['parselog']) ? $_POST['form']['parselog'] : 0;
	$num_show_posts = isset($_POST['form']['numshowposts']) ? intval($_POST['form']['numshowposts']) : 10;
	$sort_by_date = isset($_POST['form']['sortbydate']) ? $_POST['form']['sortbydate'] : 0;
	
	if ($parse_log != $forum_config['deletedpostslog_parselog'])
		$forum_db->query('UPDATE '.$forum_db->prefix.'config SET conf_value='.$parse_log.' WHERE conf_name=\'deletedpostslog_parselog\'') or error('Unable to update system configuration (deletedpostslog_parselog)', __FILE__, __LINE__);
	
	if ($sort_by_date != $forum_config['deletedpostslog_sortbydate'])
		$forum_db->query('UPDATE '.$forum_db->prefix.'config SET conf_value='.$sort_by_date.' WHERE conf_name=\'deletedpostslog_sortbydate\'') or error('Unable to update system configuration (deletedpostslog_sortbydate)', __FILE__, __LINE__);
		
	if (($num_show_posts != $forum_config['deletedpostslog_numshowposts']) && ($num_show_posts < 100) && ($num_show_posts > 0))
		$forum_db->query('UPDATE '.$forum_db->prefix.'config SET conf_value='.$num_show_posts.' WHERE conf_name=\'deletedpostslog_numshowposts\'') or error('Unable to update system configuration (deletedpostslog_numshowposts)', __FILE__, __LINE__);
	
	// Regenerate the config cache
	require_once FORUM_ROOT.'include/cache.php';
	generate_config_cache();
	
	redirect($_SERVER['HTTP_REFERER'], 'Options updated. '.$lang_admin_common['Redirect']);
}

else if (isset($_POST['restore']))
{
	$posts = $_POST['posts'];
	if (empty($posts))
		message('No posts were selected to be restored.');
	
	$result = $forum_db->query('SELECT p.id, t.id AS topic_id, t.first_post_id AS topic_first_post_id, t.forum_id FROM '.$forum_db->prefix.'posts AS p INNER JOIN '.$forum_db->prefix.'topics AS t ON t.id=p.topic_id WHERE p.id IN ('.implode(',', $posts).')') or error('Unable to fetch post information', __FILE__, __LINE__);
	if($forum_db->num_rows($result) != count($posts))
		message($lang_common['Bad request']);
		
	$topics = array();					// contains all topics whose first posts will be restored
	$all_topics['topic_id'] = array();
	$all_topics['forum_id'] = array();

	while($cur_post = $forum_db->fetch_assoc($result))
	{
		if(!in_array($cur_post['topic_id'], $all_topics['topic_id']))
		{
			$all_topics['topic_id'][] = $cur_post['topic_id'];
			if(!in_array($cur_post['forum_id'], $all_topics['forum_id']))
				$all_topics['forum_id'][] = $cur_post['forum_id'];
		}
		
		if($cur_post['topic_first_post_id'] == $cur_post['id']) 
			$topics['topic_id'][] = $cur_post['topic_id'];
	}
	
	if(!empty($topics['topic_id']))
	{
		$forum_db->query('UPDATE '.$forum_db->prefix.'topics SET deleted=0 WHERE id IN ('.implode(',', $topics['topic_id']).')') or error('Unable to restore topics', __FILE__, __LINE__);
		$forum_db->query('UPDATE '.$forum_db->prefix.'subscriptions SET deleted=0 WHERE topic_id IN ('.implode(',', $topics['topic_id']).')') or error('Unable to restore topic subscriptions', __FILE__, __LINE__);
	}
		
	$forum_db->query('UPDATE '.$forum_db->prefix.'posts SET deleted=0, deleter_id=NULL, deleted_when=NULL WHERE id IN ('.implode(',', $posts).')') or error('Unable to restore posts', __FILE__, __LINE__);
	
	foreach($all_topics['topic_id'] as $topic_id)
	{
		sync_topic($topic_id);
	}
	
	foreach($all_topics['forum_id'] as $forum_id)
	{
		sync_forum($forum_id);
	}	
	
	redirect($_SERVER['HTTP_REFERER'], 'Restored posts. '.$lang_admin_common['Redirect']);
}

else if (isset($_POST['delete']))
{
	if (isset($_POST['delete_comply']))
	{
		$posts = $_POST['posts'];
	
		$result = $forum_db->query('SELECT p.id, t.id AS topic_id, t.first_post_id AS topic_first_post_id, t.forum_id FROM '.$forum_db->prefix.'posts AS p INNER JOIN '.$forum_db->prefix.'topics AS t ON t.id=p.topic_id WHERE p.id IN ('.$posts.')') or error('Unable to fetch post information', __FILE__, __LINE__);
		if($forum_db->num_rows($result) != count(explode(',', $posts)))
			message($lang_common['Bad request']);
		
		$topics = array();

		while($cur_post = $forum_db->fetch_assoc($result))
		{
			if($cur_post['topic_first_post_id'] == $cur_post['id']) 
			{
				$topics['topic_id'][] = $cur_post['topic_id'];
				$topics['forum_id'][] = $cur_post['forum_id'];
			}
		}
	
		if(!empty($topics))
		{
			$forum_db->query('DELETE FROM '.$forum_db->prefix.'topics WHERE id IN ('.implode(',', $topics['topic_id']).')') or error('Unable to delete topics', __FILE__, __LINE__);
			$forum_db->query('DELETE FROM '.$forum_db->prefix.'subscriptions WHERE topic_id IN ('.implode(',', $topics['topic_id']).')') or error('Unable to delete topic subscriptions', __FILE__, __LINE__);
			$forum_db->query('DELETE FROM '.$forum_db->prefix.'posts WHERE topic_id IN ('.implode(',', $topics['topic_id']).')') or error('Unable to delete posts that belong to deleted topics', __FILE__, __LINE__);
		}
	
		$forum_db->query('DELETE FROM '.$forum_db->prefix.'posts WHERE id IN ('.$posts.')') or error('Unable to delete posts', __FILE__, __LINE__);
	
		redirect($_SERVER['HTTP_REFERER'], 'Deleted posts forever. '.$lang_admin_common['Redirect']);
	}
	else if (isset($_POST['delete_cancel']))
		redirect($_SERVER['HTTP_REFERER'], $lang_admin_common['Cancel redirect']);
	else
	{
		$posts = $_POST['posts'];
		if (empty($posts))
			message('No posts were selected to be deleted forever.');
	
		$result = $forum_db->query('SELECT p.id, t.id AS topic_id, t.first_post_id AS topic_first_post_id, t.forum_id FROM '.$forum_db->prefix.'posts AS p INNER JOIN '.$forum_db->prefix.'topics AS t ON t.id=p.topic_id WHERE p.id IN ('.implode(',', $posts).')') or error('Unable to fetch post information', __FILE__, __LINE__);
		if($forum_db->num_rows($result) != count($posts))
			message($lang_common['Bad request']);
		
		// Setup breadcrumbs
		$forum_page['crumbs'] = array(
			array($forum_config['o_board_title'], forum_link($forum_url['index'])),
			array($lang_admin_common['Forum administration'], forum_link($forum_url['admin_index'])),
			array('Deleted Posts Log', $base_url.'/extensions/deletedpostslog/postslog.php'),
			'Delete posts forever' 
		);
		
		define('FORUM_PAGE_SECTION', 'management');
		define('FORUM_PAGE', 'admin-management-deletedpostslog');
		require FORUM_ROOT.'header.php';

		// START SUBST - <!-- forum_main -->
		ob_start();

?>

	<div class="main-subhead">
		<h2 class="hn"><span>Delete posts forever</span></h2>
	</div>
	
	<div class="main-content main-frm">
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo $_SERVER['PHP_SELF'] ?>">
			<div class="hidden">
				<input type="hidden" name="csrf_token" value="<?php echo generate_form_token('http://'.$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF']) ?>" />
				<input type="hidden" name="delete" value="1" />
				<input type="hidden" name="posts" value="<?php echo implode(',', $posts) ?>" />
			</div>
			<div class="ct-box">
				<p class="warn"><strong>WARNING!</strong> You will not be able to restore these posts.</p>
			</div>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" class="button" name="delete_comply" value="Delete" /></span>
				<span class="cancel"><input type="submit" class="button" name="delete_cancel" value="<?php echo $lang_admin_common['Cancel'] ?>" /></span>
			</div>
		</form>
	</div>


<?php
	$tpl_temp = forum_trim(ob_get_contents());
	$tpl_main = str_replace('<!-- forum_main -->', $tpl_temp, $tpl_main);
	ob_end_clean();
	// END SUBST - <!-- forum_main -->

		require FORUM_ROOT.'footer.php';
	}
}

$forum_page['fld_count'] = $forum_page['set_count'] = 0;

// Setup breadcrumbs
$forum_page['crumbs'] = array(
	array($forum_config['o_board_title'], forum_link($forum_url['index'])),
	array($lang_admin_common['Forum administration'], forum_link($forum_url['admin_index'])),
	'Deleted Posts Log'
);

define('FORUM_PAGE_SECTION', 'management');
define('FORUM_PAGE', 'admin-management-deletedpostslog');
require FORUM_ROOT.'header.php';

	// START SUBST - <!-- forum_main -->
	ob_start();

?>

	<div class="main-subhead">
		<h2 class="hn"><span>Deleted Posts Log Options</span></h2>
	</div>

	<div class="main-content main-frm">
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo $_SERVER['PHP_SELF'] ?>">
			<div class="hidden">
				<input type="hidden" name="csrf_token" value="<?php echo generate_form_token('http://'.$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF']) ?>" />
			</div>
			<fieldset class="sf-set set<?php echo ++$forum_page['set_count'] ?>">
				<div class="sf-box checkbox">
					<label for="fld<?php echo ++$forum_page['fld_count'] ?>" >
						<span>Parse log</span>
						Parse BBCode and smilies in the log.
					</label>
					<span class="fld-input">
						<input type="checkbox" id="fld<?php echo $forum_page['fld_count'] ?>" name="form[parselog]" value="1"<?php if ($forum_config['deletedpostslog_parselog'] == '1') echo ' checked="checked"' ?> />
					</span>
				</div>
				<div class="sf-box text">
					<label for="fld<?php echo ++$forum_page['fld_count'] ?>">
						<span>Number of posts</span>
						<small>Number of posts to be displayed on one page of the log (between 1 and 99).</small>
					</label>
						<span class="fld-input"><input type="text" id="fld<?php echo $forum_page['fld_count'] ?>" name="form[numshowposts]" value="<?php echo $forum_config['deletedpostslog_numshowposts'] ?>" size="2" maxlength="2" /></span>
						
				</div>
				<div class="sf-box checkbox">
					<label for="fld<?php echo ++$forum_page['fld_count'] ?>">
						<span>Sort by date</span>
						Sort the log by deletion date (descending).
					</label>
					<span class="fld-input">
						<input type="checkbox" id="fld<?php echo $forum_page['fld_count'] ?>" name="form[sortbydate]" value="1"<?php if ($forum_config['deletedpostslog_sortbydate'] == '1') echo ' checked="checked"' ?> /> 
					</span>
				</div>
			</fieldset>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="options" value="<?php echo $lang_admin_common['Save changes'] ?>" /></span>
			</div>
		</form>
	</div>

	<a name="log"></a>
	<div class="main-content main-frm">
		<div class="main-subhead">
			<h2 class="hn"><span>Log</span></h2>
		</div>
<?php

$result = $forum_db->query('SELECT COUNT(id) FROM '.$forum_db->prefix.'posts WHERE deleted=1') or error('Unable to fetch deleted posts count', __FILE__, __LINE__);
$num_posts = $forum_db->result($result);

$num_pages = ceil($num_posts/$forum_config['deletedpostslog_numshowposts']);

$p = isset($_GET['p']) ? ((intval($_GET['p'])<=$num_pages) ? (intval($_GET['p'])-1) : 0) : 0;

$pagination = ($num_pages > 1) ? ("\t\t".'<div style="border: 1px solid #C0C0C0; text-align: center; padding: 5px;"><span style="font-weight: bold;">Pages:</span> '.deletedpostslog_paginate($num_pages, $p+1, '/extensions/deletedpostslog/postslog.php').'</div>') : '';

if ($forum_config['deletedpostslog_sortbydate'])
	$result = $forum_db->query("SELECT p1.id, t.id AS topic_id, u1.username AS poster, u2.username AS deleter, p1.poster_id, p1.message, p1.posted, p1.deleter_id, p1.deleted_when, p1.topic_id, t.subject AS topic_subject, t.deleted AS topic_deleted, t.first_post_id AS topic_first_post_id, p2.deleted AS topic_first_post_deleted, t.forum_id, f.forum_name FROM ".$forum_db->prefix."posts AS p1 INNER JOIN ".$forum_db->prefix."topics AS t ON t.id=p1.topic_id LEFT JOIN ".$forum_db->prefix."forums AS f ON f.id=t.forum_id LEFT JOIN ".$forum_db->prefix."users AS u1 ON u1.id=p1.poster_id LEFT JOIN ".$forum_db->prefix."users AS u2 ON u2.id=p1.deleter_id INNER JOIN ".$forum_db->prefix."posts AS p2 ON t.first_post_id=p2.id WHERE p1.deleted=1 ORDER BY p1.deleted_when DESC, t.forum_id ASC, p1.topic_id ASC, p1.id ASC LIMIT ".($p*$forum_config['deletedpostslog_numshowposts']).",".$forum_config['deletedpostslog_numshowposts']) or error('Unable to fetch deleted posts', __FILE__, __LINE__);
else
	$result = $forum_db->query("SELECT p1.id, t.id AS topic_id, u1.username AS poster, u2.username AS deleter, p1.poster_id, p1.message, p1.posted, p1.deleter_id, p1.deleted_when, p1.topic_id, t.subject AS topic_subject, t.deleted AS topic_deleted, t.first_post_id AS topic_first_post_id, p2.deleted AS topic_first_post_deleted, t.forum_id, f.forum_name FROM ".$forum_db->prefix."posts AS p1 INNER JOIN ".$forum_db->prefix."topics AS t ON t.id=p1.topic_id LEFT JOIN ".$forum_db->prefix."forums AS f ON f.id=t.forum_id LEFT JOIN ".$forum_db->prefix."users AS u1 ON u1.id=p1.poster_id LEFT JOIN ".$forum_db->prefix."users AS u2 ON u2.id=p1.deleter_id INNER JOIN ".$forum_db->prefix."posts AS p2 ON t.first_post_id=p2.id WHERE p1.deleted=1 ORDER BY t.forum_id ASC, p1.topic_id ASC, p1.id ASC LIMIT ".($p*$forum_config['deletedpostslog_numshowposts']).",".$forum_config['deletedpostslog_numshowposts']) or error('Unable to fetch deleted posts', __FILE__, __LINE__);
	
if ($forum_db->num_rows($result))
{
	
	?>
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo $_SERVER['PHP_SELF'] ?>">
			<div class="hidden">
				<input type="hidden" name="csrf_token" value="<?php echo generate_form_token('http://'.$_SERVER['HTTP_HOST'].$_SERVER['PHP_SELF']) ?>" />
				<input type="hidden" name="form_sent" value="1" />
			</div>
			<div class="ct-box">	
				<p class="important"><strong>IMPORTANT!</strong> Posts can only be restored if the first post of their topic does still exist in the forums.</p>
				<p class="warn"><strong>WARNING!</strong> If you delete a post that was the first post in its topic, all other posts belonging to that topic will be deleted, too.</p>
			</div>
	<?php
	

	
	echo $pagination; ?>
	<div class="ct-group">
	
	<?php
	
	$forum_page['num_items'] = 0;
	
	include(FORUM_ROOT.'include/parser.php');
	$forum_page['item_num'] = 0;
		
	while ($cur_post = $forum_db->fetch_assoc($result))
	{
		$first_post = false;
		$no_checkbox = false;
		
		if($cur_post['id'] == $cur_post['topic_first_post_id'])	// If recent post is the first post of a topic
			$first_post = true;
		else
		{
			if($cur_post['topic_first_post_deleted'])			// If the first post of this post's topic has been deleted
				$no_checkbox = true;
		}
				
		$poster = ($cur_post['poster'] != '') ? '<a href="'.forum_link($forum_url['user'], $cur_post['poster_id']).'">'.htmlspecialchars($cur_post['poster']).'</a>' : $lang_admin_common['Deleted user'];
		$forum = ($cur_post['forum_name'] != '') ? '<a href="'.forum_link($forum_url['forum'], $cur_post['forum_id']).'">'.htmlspecialchars($cur_post['forum_name']).'</a>' : $lang_admin_common['Deleted forum'];
		$topic = ($cur_post['topic_deleted'] == 0) ? '<a href="'.forum_link($forum_url['topic'], $cur_post['topic_id']).'">'.htmlspecialchars($cur_post['topic_subject']).'</a>' : htmlspecialchars($cur_post['topic_subject']);
		$post = $forum_config['deletedpostslog_parselog'] ? parse_message($cur_post['message'], 0) : nl2br($cur_post['message']);
		$deleter = ($cur_post['deleter'] != '') ? '<a href="'.forum_link($forum_url['user'], $cur_post['deleter_id']).'">'.htmlspecialchars($cur_post['deleter']).'</a>' : $lang_admin_common['Deleted user'];
		
?>
			<div class="ct-set group-item<?php echo ++$forum_page['item_num'] ?>">
				<div class="ct-legend">
				<span><?php echo 'Post '.format_time($cur_post['posted']);?></span>
				<?php echo 'By: '.$poster; ?><?php if ($first_post) echo '&nbsp;&nbsp;&nbsp;&nbsp;[ FIRST POST ] ' ?></span>
				</div>
				<p class="item-select">
					<input type="checkbox" id="fld<?php echo $forum_page['fld_count'] ?>" name="posts[<?php echo $cur_post['id'] ?>]" value="<?php echo $cur_post['id'] ?>"<?php if ($no_checkbox) echo 'disabled ' ?> />
				<?php echo $forum ?>&#160;В»&#160;<?php echo $topic ?>
				</p>
				
				<p><?php echo $post ?></p>
				<p>[ <?php printf('Deleted %s by %s', format_time($cur_post['deleted_when']), $deleter) ?> ]</p>
			
			</div>
<?php

	} ?>
	</div>
	<?php	echo $pagination;
	
?>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="restore" value="Restore" /></span>
				<span class="submit"><input type="submit" name="delete" value="Delete forever" /></span>
			</div>
		</form>
<?php

}
else
{

?>
		<div class="ct-box">
			<p>There are no deleted posts.</p>
		</div>
<?php

}

?>
	</div>


<?php
	$tpl_temp = forum_trim(ob_get_contents());
	$tpl_main = str_replace('<!-- forum_main -->', $tpl_temp, $tpl_main);
	ob_end_clean();
	// END SUBST - <!-- forum_main -->
require FORUM_ROOT.'footer.php';
?>
