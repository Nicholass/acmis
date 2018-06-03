<?php
/**
 * Anycode extension 1.0.0 Beta 2
 * 
 * Administration hooks page for (c) PunBB .
 *
 * 
 * @copyright Copyright (C) 2008 hcs, partially based on code copyright (C) 2008 PunBB, on code copyright (C) 2008  FluxBB.org
 * @license http://www.gnu.org/licenses/gpl.html GPL version 2 or higher
 * @package Anycode
 */
define('FORUM_SHOW_QUERIES', 1);

if (!defined('FORUM_ROOT'))
	define('FORUM_ROOT', '../../');
require FORUM_ROOT.'include/common.php';
require FORUM_ROOT.'include/common_admin.php';

($hook = get_hook('anycode_hook_start')) ? eval($hook) : null;

if ($forum_user['g_id']!=FORUM_ADMIN)
	message($lang_common['No permission']);

define('SOLUTION_PATH', $base_url.'/extensions/anycodetool/solutions.php');
define('HOOKS_PATH', $base_url.'/extensions/anycodetool/hooks.php');	
	
// Load the admin.php language files
require FORUM_ROOT.'lang/'.$forum_user['language'].'/admin_common.php';

if (isset($_POST['delete_hook']) || isset($_POST['del_hook_comply'])) {
	// Validate the CSRF token
	if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== generate_form_token(get_current_url()))
		csrf_confirm_form();	
		
	// User pressed the cancel button
	if (isset($_POST['del_hook_cancel']))
		redirect(HOOKS_PATH, $lang_admin_common['Cancel redirect']);
		
	if (!isset($_POST['hook_id']))
		message($lang_common['Bad request']);

	$hook_id = intval($_POST['hook_id']);

	($hook = get_hook('anycode_del_hook_form_submitted')) ? eval($hook) : null;
	
	$query = array(
		'SELECT'	=> 's.name AS sol_name, s.id AS sol_id, h.hook_id',
		'FROM'		=> 'anycode_hooks AS h',
		'JOINS'		=> array(
			array(
				'INNER JOIN'	=> 'anycode_solutions AS s',
				'ON'			=> 'h.solution_id=s.id'
			),
		),			
		'WHERE'		=> 'h.id='.$hook_id
	);
		
	($hook = get_hook('anycode_del_hk_qr_select_sol_hook')) ? eval($hook) : null;
	$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);
	
	if (!$forum_db->num_rows($result))
		message($lang_common['Bad request']);	

	$cur_hook = $forum_db->fetch_assoc($result);
	
	if (isset($_POST['del_hook_comply'])) {
		
		// Delete core hooks
		$query = array(
			'DELETE'	=> 'extension_hooks',
			'WHERE'		=> 'extension_id = \''.$forum_db->escape('anycode_'.$cur_hook['sol_name']).'\' AND id=\''.$forum_db->escape($cur_hook['hook_id']).'\''
		);
		
		($hook = get_hook('anycode_del_hk_qr_delete_ext_hooks')) ? eval($hook) : null;
		$forum_db->query_build($query) or error(__FILE__, __LINE__);

		// Delete solution hook	
		
		$query = array(
			'DELETE'	=> 'anycode_hooks',
			'WHERE'		=> 'id = '.$hook_id
		);
		
		($hook = get_hook('anycode_del_hk_qr_delete_sol_hook')) ? eval($hook) : null;
		$forum_db->query_build($query) or error(__FILE__, __LINE__);
		
		// Empty the PHP cache
		forum_clear_cache();

		// Regenerate the hooks cache
		if (!defined('FORUM_CACHE_FUNCTIONS_LOADED'))
			require FORUM_ROOT.'include/cache.php';

		generate_hooks_cache();

		($hook = get_hook('anycode_del_hook_pre_redirect')) ? eval($hook) : null;

		redirect(HOOKS_PATH, $lang_anycode['Hook deleted'].' '.$lang_admin_common['Redirect']);
	}
	else	// If the user hasn't comfirmed the delete
	{

		// Setup the form
		$forum_page['form_action'] = HOOKS_PATH;

		$forum_page['hidden_fields'] = array(
			'csrf_token'	=> '<input type="hidden" name="csrf_token" value="'.generate_form_token($forum_page['form_action']).'" />',
			'hook_to_delete'	=> '<input type="hidden" name="hook_id" value="'.$hook_id.'" />'
		);

		// Setup breadcrumbs
		$forum_page['crumbs'] = array(
			array($forum_config['o_board_title'], forum_link($forum_url['index'])),
			array($lang_admin_common['Forum administration'], forum_link($forum_url['admin_index'])),
			array($lang_anycode['AnyCode'], HOOKS_PATH),
			$lang_anycode['Delete hook']
		);

		($hook = get_hook('anycode_del_hook_pre_header_load')) ? eval($hook) : null;

		define('FORUM_PAGE_SECTION', 'anycodetool');
		define('FORUM_PAGE', 'admin-anycode-solutions');		
		
		require FORUM_ROOT.'header.php';

		// START SUBST - <!-- forum_main -->
		ob_start();

		($hook = get_hook('anycode_del_hook_output_start')) ? eval($hook) : null;

?>
	<div class="main-subhead">
		<h2 class="hn"><span><?php printf($lang_anycode['Confirm delete hook'],forum_htmlencode($cur_hook['hook_id']), forum_htmlencode($cur_hook['sol_name'])) ?></span></h2>
	</div>
	<div class="main-content main-frm">
		<div class="ct-box warn-box">
			<p class="warn"><?php echo $lang_anycode['Delete hook warning'] ?></p>
		</div>
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo $forum_page['form_action'] ?>">
			<div class="hidden">
				<?php echo implode("\n\t\t\t\t", $forum_page['hidden_fields'])."\n" ?>
			</div>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="del_hook_comply" value="<?php echo $lang_anycode['Delete hook'] ?>" /></span>
			</div>
		</form>
	</div>
<?php

		($hook = get_hook('anycode_del_hook_end')) ? eval($hook) : null;

		$tpl_temp = forum_trim(ob_get_contents());
		$tpl_main = str_replace('<!-- forum_main -->', $tpl_temp, $tpl_main);
		ob_end_clean();
		// END SUBST - <!-- forum_main -->
		require FORUM_ROOT.'footer.php';
	}
}

if (isset($_POST['update_hook'])) {

			// Validate the CSRF token
	if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== generate_form_token(get_current_url()))
		csrf_confirm_form();	
		
	if (isset($_POST['hook_id']))
		$hook_id = intval($_POST['hook_id']);
	else
		 message($lang_common['Bad request']);

	if (isset($_POST['hook_code']))
		$hook_code = forum_trim($_POST['hook_code']);
	else 
		message($lang_common['Bad request']);

	$hook_enable = (isset($_POST['hook_enable']) ? 1 : 0);

	$query = array(
		'SELECT'	=> 's.name AS sol_name, s.enable AS sol_enable, h.enable, h.hook_id',
		'FROM'		=> 'anycode_hooks AS h',
		'JOINS'		=> array(
			array(
				'INNER JOIN'	=> 'anycode_solutions AS s',
				'ON'			=> 'h.solution_id=s.id'
			),
		),			
		'WHERE'		=> 'h.id='.$hook_id
	);

	($hook = get_hook('anycode_hk_edit_select_hook')) ? eval($hook) : null;	
	$result = $forum_db->query_build($query) or dbError(__FILE__, __LINE__);	

	if (!$forum_db->num_rows($result)) 
		message($lang_common['Bad request']);
		
	$cur_hook = $forum_db->fetch_assoc($result);
	
	// if hook change state to enabled and solution is enabled
	// we add hook into core
	if ($hook_enable == 1 && $cur_hook['enable'] == 0 && $cur_hook['sol_enable'] == 1) {
		
		$query = array(
			'INSERT'	=> 'id, extension_id, code, installed, priority',
			'INTO'		=> 'extension_hooks',
			'VALUES'	=> '\''.$forum_db->escape(forum_trim($cur_hook['hook_id'])).'\', \''.$forum_db->escape('anycode_'.$cur_hook['sol_name']).'\', \''.$forum_db->escape(forum_trim($hook_code)).'\', '.time().', '.(isset($hook_priority) ? $hook_priority : 5)
		);
		
		($hook = get_hook('anycode_upd_hook_qr_ins_hook')) ? eval($hook) : null;
		$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);			
		
	
	} elseif ($hook_enable == 0 && $cur_hook['enable'] == 1) {
		//if hook disabled we delete hook from core
		$query = array(
			'DELETE'	=> 'extension_hooks',
			'WHERE'		=> 'extension_id=\''.$forum_db->escape('anycode_'.$cur_hook['sol_name']).'\' AND id=\''.$forum_db->escape('anycode_'.$cur_hook['hook_id']).'\''
		);
		($hook = get_hook('anycode_upd_hook_qr_delete_hooks')) ? eval($hook) : null;
		$forum_db->query_build($query) or error(__FILE__, __LINE__);
	}
	else {
		//update core hook code
		$query = array(
			'UPDATE'	=> 'extension_hooks',
			'SET'		=> 'code=\''.$forum_db->escape($hook_code).'\'',
			'WHERE'		=> 'extension_id=\''.$forum_db->escape('anycode_'.$cur_hook['sol_name']).'\' AND id=\''.$forum_db->escape($cur_hook['hook_id']).'\''
		);	
		($hook = get_hook('anycode_upd_hook_qr_upd_hook')) ? eval($hook) : null;
		$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);	
	}
	
	// update solution hook info
	$query = array(
		'UPDATE'	=> 'anycode_hooks',
		'SET'		=> 'code=\''.$forum_db->escape($hook_code).'\', enable='.$hook_enable,
		'WHERE'		=> 'id='.$hook_id
	);	
	($hook = get_hook('anycode_upd_hook_qr_upd_hook')) ? eval($hook) : null;
	$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);	
	
	// Regenerate the hooks cache
	if (!defined('FORUM_CACHE_FUNCTIONS_LOADED'))
		require FORUM_ROOT.'include/cache.php';

	generate_hooks_cache();

	($hook = get_hook('anycode_upd_hook_pre_redirect')) ? eval($hook) : null;

	redirect(HOOKS_PATH, $lang_anycode['Hook updated'].' '.$lang_admin_common['Redirect']);
}


if (isset($_POST['edit_hook'])) {

		// Validate the CSRF token
	if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== generate_form_token(get_current_url()))
		csrf_confirm_form();	
		
	if (isset($_POST['hook'])) {
		list($sol_id, $hook_id) = each($_POST['hook']);
		$sol_id = intval($sol_id);
		$hook_id = intval($hook_id);
		
		$query = array(
			'SELECT'	=> 's.name, h.hook_id, h.code, h.enable, h.id, h.solution_id',
			'FROM'		=> 'anycode_hooks AS h',
			'JOINS'		=> array(
				array(
					'INNER JOIN'	=> 'anycode_solutions AS s',
					'ON'			=> 'h.solution_id=s.id'
				),
			),			
			'WHERE'		=> 'h.id='.$hook_id
		);

		($hook = get_hook('anycode_hk_edit_select_hook')) ? eval($hook) : null;	
		$result = $forum_db->query_build($query) or dbError(__FILE__, __LINE__);
			
		if (!$forum_db->num_rows($result)) 
			message($lang_common['Bad request']);
			
		$cur_hook = $forum_db->fetch_assoc($result);
		
	}
	else
		message($lang_common['Bad request']);
	
	// Setup breadcrumbs
	$forum_page['crumbs'] = array(
		array($forum_config['o_board_title'], forum_link($forum_url['index'])),
		array($lang_admin_common['Forum administration'], forum_link($forum_url['admin_index'])),
		array($lang_anycode['AnyCode'], SOLUTION_PATH),
		array($lang_anycode['Hooks'], HOOKS_PATH),
		sprintf($lang_anycode['Edit hook crumb'],$cur_hook['hook_id'])
	);

	($hook = get_hook('anycode_hk_edit_pre_header_load')) ? eval($hook) : null;

	define('FORUM_PAGE_SECTION', 'anycodetool');
	define('FORUM_PAGE', 'admin-anycode-hooks');

	require FORUM_ROOT.'header.php';

	// START SUBST - <!-- forum_main -->
	ob_start();

	$forum_page['form_action'] = HOOKS_PATH;
	$forum_page['hidden_fields'] = array(
		'csrf_token'	=> '<input type="hidden" name="csrf_token" value="'.generate_form_token($forum_page['form_action']).'" />',
		'hook_id'	=>	'<input type="hidden" name="hook_id" value="'.$hook_id.'" />'
	);
	$forum_page['group_count'] = $forum_page['item_count'] = $forum_page['fld_count'] = 0;

	($hook = get_hook('anycode_hk_edit_hook_output_start')) ? eval($hook) : null;
?>
	<div class="main-subhead">
		<h2 class="hn"><span><?php echo sprintf($lang_anycode['Edit hook head'],forum_htmlencode($cur_hook['hook_id']),forum_htmlencode($cur_hook['name'])) ?></span></h2>
	</div>
	<div class="main-content main-frm">
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo $forum_page['form_action'] ?>">
			<div class="hidden">
				<?php echo implode("\n\t\t\t\t", $forum_page['hidden_fields'])."\n" ?>
			</div>
<?php ($hook = get_hook('anycode_pre_edit_hook_fieldset')) ? eval($hook) : null; ?>
			<fieldset class="frm-group group<?php echo ++$forum_page['group_count'] ?>">
				<legend class="group-legend"><span><?php echo $lang_anycode['Edit hook legend'] ?></span></legend>
<?php ($hook = get_hook('anycode_pre_edit_hook_code')) ? eval($hook) : null; ?>
				<div class="txt-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="txt-box textarea">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_anycode['Edit hook code'] ?></span></label><br />
						<div class="txt-input"><span class="fld-input"><textarea name="hook_code" size="80" rows="12"><?php echo $cur_hook['code'] ?></textarea></span></div>
					</div>
				</div>				
<?php ($hook = get_hook('anycode_hk_pre_hook_checkbox')) ? eval($hook) : null; ?>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="sf-box checkbox">
						<span class="fld-input"><input type="checkbox" id="fld<?php echo ++$forum_page['fld_count'] ?>" name="hook_enable" value="1" checked="checked" /></span>
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_anycode['Enable hook label'] ?></span> <?php echo $lang_anycode['Enable hook'] ?></label>
					</div>
				</div>				
<?php ($hook = get_hook('anycode_hk_pre_add_hook_fieldset_end')) ? eval($hook) : null; ?>
			</fieldset>
<?php ($hook = get_hook('anycode_hk_add_hook_fieldset_end')) ? eval($hook) : null; ?>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="update_hook" value="<?php echo $lang_anycode['Update hook'] ?>" /></span>
			<span class="submit"><input type="submit" name="delete_hook" value="<?php echo $lang_anycode['Delete hook'] ?>" /></span>
			</div>
		</form>
	</div>
<?php
($hook = get_hook('anycode_hk_post_sel_sol_form')) ? eval($hook) : null;


	($hook = get_hook('anycode_hk_edit_hook_end')) ? eval($hook) : null;

	$tpl_temp = forum_trim(ob_get_contents());
	$tpl_main = str_replace('<!-- forum_main -->', $tpl_temp, $tpl_main);
	ob_end_clean();
	// END SUBST - <!-- forum_main -->

	require FORUM_ROOT.'footer.php';
}

// Add a hook
if (isset($_POST['add_hook'])) {

	// Validate the CSRF token
	if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== generate_form_token(get_current_url()))
		csrf_confirm_form();	

	$errors = array();
		
	if (!isset($_POST['hook_enable']))
		$hook_enable = 0;
	else
		$hook_enable= 1;
		
	if (isset($_POST['sol_to_select']))
		$sol_id = intval($_POST['sol_to_select']);
	else
		$errors[] = $lang_anycode['Empty solution'];
		
	if (!isset($_POST['hook_name']))
		$errors[] = $lang_anycode['Empty hook'];

	$hook_name = forum_trim(forum_htmlencode(($_POST['hook_name'])));
	
	if ($hook_name == '')
		$errors[] = $lang_anycode['Empty hook'];
		
	if (!isset($_POST['hook_code']))
		$errors[] = $lang_anycode['Empty code'];
	
	$hook_code = forum_trim(($_POST['hook_code']));

	if ($hook_code == '')
		$errors[] = $lang_anycode['Empty code'];
	
	
	if (empty($errors)) {
		
	
		$query = array(
			'SELECT'	=> 'h.id, h.hook_id, s.name',
			'FROM'		=> 'anycode_hooks AS h',
			'JOINS'		=> array(
				array(
					'INNER JOIN'	=> 'anycode_solutions AS s',
					'ON'			=> 'h.solution_id='.$sol_id
				),
			),
			'WHERE'		=> 'h.hook_id=\''.$hook_name.'\''
		);

		($hook = get_hook('anycode_add_hook_qr_get_hook_name')) ? eval($hook) : null;
	
		$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);

		// No errors - Add hook
		if (!$forum_db->num_rows($result)) {
		
			$query = array(
				'INSERT'	=> 'owner_id, solution_id, lastedited_at, hook_id, code, enable',
				'INTO'		=> 'anycode_hooks',
				'VALUES'	=> '\''.$forum_user['id'].'\', \''.$sol_id.'\', \''.time().'\', \''.$forum_db->escape($hook_name).'\', \''.$forum_db->escape(forum_trim($_POST['hook_code'])).'\', \''.$hook_enable.'\''
			);		

			($hook = get_hook('anycode_add_hook_qr_ins_hook')) ? eval($hook) : null;
			$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);		

			// if solution and hook is enabled 
			// add hook into core 
			$query = array(
				'SELECT'	=> 's.name, s.enable',
				'FROM'		=> 'anycode_solutions AS s',
				'WHERE'		=> 's.id=\''.$sol_id.'\''
			);

			($hook = get_hook('anycode_add_hook_qr_get_sol_enable')) ? eval($hook) : null;
			$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);
		
			$cur_sol = $forum_db->fetch_assoc($result);
		
			if ($cur_sol['enable'] == 1 && $hook_enable ==1) {
			
				$query = array(
					'INSERT'	=> 'id, extension_id, code, installed, priority',
					'INTO'		=> 'extension_hooks',
					'VALUES'	=> '\''.$forum_db->escape(forum_trim($hook_name)).'\', \''.$forum_db->escape('anycode_'.$cur_sol['name']).'\', \''.$forum_db->escape($hook_code).'\', '.time().', '.(isset($hook_priority) ? $hook_priority : 5)
				);
			
				($hook = get_hook('anycode_add_hook_qr_insert_hook')) ? eval($hook) : null;
				$forum_db->query_build($query) or error(__FILE__, __LINE__);			
			}

			// Empty the PHP cache
			forum_clear_cache();
	
			// Regenerate the hooks cache
			if (!defined('FORUM_CACHE_FUNCTIONS_LOADED'))
				require FORUM_ROOT.'include/cache.php';

			generate_hooks_cache();

			($hook = get_hook('anycode_add_hook_pre_redirect')) ? eval($hook) : null;
				
			redirect(HOOKS_PATH, $lang_anycode['Hook added'].' '.$lang_admin_common['Redirect']);
		}

		$errors[] = sprintf($lang_anycode['Hook already installed'],$hook_name);
	}
}


// Setup breadcrumbs
$forum_page['crumbs'] = array(
	array($forum_config['o_board_title'], forum_link($forum_url['index'])),
	array($lang_admin_common['Forum administration'], forum_link($forum_url['admin_index'])),
	array($lang_anycode['AnyCode'], SOLUTION_PATH),
	$lang_anycode['Hooks']
);

($hook = get_hook('anycode_hk_pre_header_load')) ? eval($hook) : null;

define('FORUM_PAGE_SECTION', 'anycodetool');
define('FORUM_PAGE', 'admin-anycode-hooks');

$query = array(
	'SELECT'	=> 's.id, s.name',
	'FROM'		=> 'anycode_solutions AS s',
);

($hook = get_hook('anycode_hk_select_solutions')) ? eval($hook) : null;

$result = $forum_db->query_build($query) or dbError(__FILE__, __LINE__);
$num_sol = $forum_db->num_rows($result);

for ($i = 0; $i < $num_sol; ++$i)
	$sol_list[] = $forum_db->fetch_assoc($result);

require FORUM_ROOT.'header.php';

// START SUBST - <!-- forum_main -->
ob_start();

$forum_page['form_action'] = HOOKS_PATH;
$forum_page['hidden_fields'] = array(
	'csrf_token'	=> '<input type="hidden" name="csrf_token" value="'.generate_form_token($forum_page['form_action']).'" />'
);
$forum_page['group_count'] = $forum_page['item_count'] = $forum_page['fld_count'] = 0;

($hook = get_hook('anycode_hk_main_output_start')) ? eval($hook) : null;

?>
	<div class="main-subhead">
		<h2 class="hn"><span><?php echo $lang_anycode['Add hook head'] ?></span></h2>
	</div>
	<div class="main-content main-frm">
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo $forum_page['form_action'] ?>">
			<div class="hidden">
				<?php echo implode("\n\t\t\t\t", $forum_page['hidden_fields'])."\n" ?>
			</div>
<?php

	// If there were any errors, show them
	if (!empty($errors))
	{
		$forum_page['errors'] = array();
		foreach ($errors as $cur_error)
			$forum_page['errors'][] = '<li class="warn"><span>'.$cur_error.'</span></li>';

		($hook = get_hook('anycode_pre_hook_errors')) ? eval($hook) : null;

?>
		<div class="ct-box error-box">
			<h2 class="warn hn"><?php echo $lang_anycode['Hook errors'] ?></h2>
			<ul class="error-list">
				<?php echo implode("\n\t\t\t\t", $forum_page['errors'])."\n" ?>
			</ul>
		</div>
<?php

	}

?>				
<?php ($hook = get_hook('anycode_pre_add_hook_fieldset')) ? eval($hook) : null; ?>
			<fieldset class="frm-group group<?php echo ++$forum_page['group_count'] ?>">
				<legend class="group-legend"><span><?php echo $lang_anycode['Add hook legend'] ?></span></legend>
<?php 
if  ($num_sol) { 
?>				
<?php ($hook = get_hook('anycode_pre_new_hook_name')) ? eval($hook) : null; ?>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="sf-box text">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_anycode['Add hook label'] ?></span></label><br />
						<span class="fld-input"><input type="text" id="fld<?php echo $forum_page['fld_count'] ?>" name="hook_name" size="42" maxlength="150" /></span>
					</div>
				</div>
				
<?php ($hook = get_hook('anycode_pre_new_hook_code')) ? eval($hook) : null; ?>
				<div class="txt-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="txt-box textarea">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_anycode['Add hook code'] ?></span></label><br />
						<div class="txt-input"><span class="fld-input"><textarea name="hook_code" size="80" rows="12"></textarea></span></div>
					</div>
				</div>				

				
<?php ($hook = get_hook('anycode_hk_pre_hook_checkbox')) ? eval($hook) : null; ?>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="sf-box checkbox">
						<span class="fld-input"><input type="checkbox" id="fld<?php echo ++$forum_page['fld_count'] ?>" name="hook_enable" value="1" checked="checked" /></span>
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_anycode['Enable hook label'] ?></span> <?php echo $lang_anycode['Enable hook'] ?></label>
					</div>
				</div>				
				
				
<?php ($hook = get_hook('anycode_hk_pre_sel_sol_name')) ? eval($hook) : null; ?>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="sf-box text">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_anycode['Select solution label'] ?></span></label><br />
						<span class="fld-input"><select id="fld<?php echo $forum_page['fld_count'] ?>" name="sol_to_select">
<?php

	foreach ($sol_list as $cur_solution)
	{
		echo "\t\t\t\t\t\t\t".'<option value="'. $cur_solution['id'].'">'.forum_htmlencode( $cur_solution['name']).'</option>'."\n";
	}

?>
						</select></span>						
					</div>
				</div>
<?php ($hook = get_hook('anycode_hk_pre_add_hook_fieldset_end')) ? eval($hook) : null; ?>
			</fieldset>
<?php ($hook = get_hook('anycode_hk_add_hook_fieldset_end')) ? eval($hook) : null; ?>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="add_hook" value="<?php echo $lang_anycode['Add hook'] ?>" /></span>
			</div>
<?php			
}
else {
?>
				<div class="ct-box">
					<p><?php echo $lang_anycode['Need solution'] ?></p>
				</div>
			</fieldset>
<?php
}
?>			
		</form>
	</div>
<?php
($hook = get_hook('anycode_hk_post_sel_sol_form')) ? eval($hook) : null;

// Reset counter
$forum_page['group_count'] = $forum_page['item_count'] = 0;

if ($num_sol) 
{


	foreach ($sol_list as $cur_solution) {
		
		$query = array(
			'SELECT'	=> 'h.id, h.hook_id',
			'FROM'		=> 'anycode_hooks AS h',
			'WHERE'		=> 'h.solution_id=\''.$cur_solution['id'].'\''
		
		);

		($hook = get_hook('anycode_hk_select_hooks_solution')) ? eval($hook) : null;

		$result = $forum_db->query_build($query) or dbError(__FILE__, __LINE__);		
		
		if ($forum_db->num_rows($result)) {		
		
		
?>
	<div class="main-subhead">
		<h2 class="hn"><span><?php echo sprintf($lang_anycode['Hook solution'],$cur_solution['name']) ?></span></h2>
	</div>
		<div class="main-content main-frm">
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo $forum_page['form_action'] ?>">
			<div class="hidden">
				<?php echo implode("\n\t\t\t\t", $forum_page['hidden_fields'])."\n" ?>
			</div>
		
<?php ($hook = get_hook('anycode_hk_pre_edit_hook_select')) ? eval($hook) : null; ?>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="sf-box select">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_anycode['Select hook'] ?></span></label><br />
						<span class="fld-input"><select id="fld<?php echo $forum_page['fld_count'] ?>" name="hook[<?php echo $forum_page['fld_count'] ?>]">
<?php

	while ($cur_hook = $forum_db->fetch_assoc($result))
	{
		echo "\t\t\t\t\t\t\t".'<option value="'. $cur_hook['id'].'">'.forum_htmlencode( $cur_hook['hook_id']).'</option>'."\n";
	}

?>						
						</select></span>
					</div>
				</div>
<?php ($hook = get_hook('anycode_hk_edit_hook_select_end')) ? eval($hook) : null; ?>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="edit_hook" value="<?php echo $lang_anycode['Edit hook'] ?>" /></span>
			</div>
		</form>
	</div>
<?php
		}
	}
	
	($hook = get_hook('anycode_hk_post_edit_hook_form')) ? eval($hook) : null;
	


	
	
	
		
}

($hook = get_hook('anycode_hook_end')) ? eval($hook) : null;

$tpl_temp = forum_trim(ob_get_contents());
$tpl_main = str_replace('<!-- forum_main -->', $tpl_temp, $tpl_main);
ob_end_clean();
// END SUBST - <!-- forum_main -->

require FORUM_ROOT.'footer.php';