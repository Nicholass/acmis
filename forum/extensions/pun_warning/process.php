<?php
if (!defined('FORUM_ROOT'))
	define('FORUM_ROOT', '../../');
require_once FORUM_ROOT.'include/common.php';
require_once FORUM_ROOT.'include/common_admin.php';

if (($forum_user['g_id'] != FORUM_ADMIN) && ($forum_user['g_moderator'] != '1'))
	message($lang_common['No permission']);

$action=@$_GET['action'];

switch($action){
	case 'add_warn':
		if(isset($_POST['action'])=='addwarning'){
			pun_warn_add2();
			break;
		} else {
			pun_warn_add();
			break;
		}
	case 'update_config':
		pun_warn_update_config();
		break;
	
	case 'list_warn':
		if(!empty($_REQUEST['uid'])){
			pun_warn_list($_REQUEST['uid']);
		} else {
			pun_warn_list_show_form();
		}
		break;

	default:
		//pun_warn_admin_crumbs();
		if ($forum_user['g_id'] != FORUM_ADMIN) {
			pun_warn_list();
		} else {
			pun_warn_admin_section();
		}
		break;
}




?>