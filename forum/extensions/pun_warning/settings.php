<?php

if (!defined('FORUM_ROOT'))
	define('FORUM_ROOT', '../../');
require FORUM_ROOT.'include/common.php';
require FORUM_ROOT.'include/common_admin.php';

if (($forum_user['g_id'] != FORUM_ADMIN) && ($forum_user['g_moderator'] != '1'))
	message($lang_common['No permission']);
	
// Load the admin.php language files
require FORUM_ROOT.'lang/'.$forum_user['language'].'/admin_common.php';

define('FUNCTIONS_PATH', FORUM_ROOT.'extensions/pun_warning/functions.php');
define('PROCESS_PATH', FORUM_ROOT.'extensions/pun_warning/process.php');	

require_once (FUNCTIONS_PATH);

// Setup breadcrumbs
$forum_page['crumbs'] = array(
	array($forum_config['o_board_title'], forum_link($forum_url['index'])),
	array($lang_admin_common['Forum administration'], forum_link($forum_url['admin_index'])),
	'Pun Warning'
);
$action=@$_GET['action'];
define('FORUM_PAGE_SECTION', 'pun_warning');
define('FORUM_PAGE', 'admin_pun_warning_settings');


require FORUM_ROOT.'header.php';


	// START SUBST - <!-- forum_main -->
		ob_start();
	
		require_once(PROCESS_PATH);
		
		$tpl_temp = forum_trim(ob_get_contents());
		$tpl_main = str_replace('<!-- forum_main -->', $tpl_temp, $tpl_main);
		ob_end_clean();
	// END SUBST - <!-- forum_main -->

	require FORUM_ROOT.'footer.php';

?>