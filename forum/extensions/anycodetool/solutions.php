<?php
/**
 * Anycode extension 1.0.0 Beta 2
 * 
 * Administration solution page for (c) PunBB .
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

($hook = get_hook('anycode_solution_start')) ? eval($hook) : null;

if ($forum_user['g_id']!=FORUM_ADMIN)
	message($lang_common['No permission']);

define('SOLUTION_PATH', $base_url.'/extensions/anycodetool/solutions.php');
define('MANAGER_PATH', $base_url.'/extensions/anycodetool/manager.php');	
	
// Load the admin.php language files
require FORUM_ROOT.'lang/'.$forum_user['language'].'/admin_common.php';


if (isset($_POST['add_sol']))
{
	
	// Validate the CSRF token
	if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== generate_form_token(get_current_url()))
		csrf_confirm_form();	

	$errors = array();
	$new_sol_name = forum_trim($_POST['new_sol_name']);
	
	if ($new_sol_name == '')
		$errors[] = $lang_anycode['Must name solution'];
	
	if(strlen($new_sol_name) > 42)
		$errors[] =  $lang_anycode['Name solution to long'];
		
	if (preg_match('/[^a-zA-Z0-9_-]/',$new_sol_name))
		$errors[] = sprintf($lang_anycode['Name solution invalid'],forum_htmlencode($new_sol_name));
		
	$query = array(
		'SELECT'	=> 'name',
		'FROM'		=> 'anycode_solutions',
		'WHERE'	=> 'name=\''.$forum_db->escape($new_sol_name).'\''
	);		
	
	$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);
	
	if ($forum_db->num_rows($result))
		$errors[] = sprintf($lang_anycode['Solution already exist'],forum_htmlencode($new_sol_name));		
		
	($hook = get_hook('anycode_add_sol_form_submitted')) ? eval($hook) : null;
	
	if (empty($errors)) {
	
		$query = array(
			'INSERT'	=> 'name, owner_id',
			'INTO'		=> 'anycode_solutions',
			'VALUES'	=> '\''.$forum_db->escape($new_sol_name).'\', '.$forum_user['id']
		);

		($hook = get_hook('anycode_add_sol_qr_add_sol')) ? eval($hook) : null;
		$forum_db->query_build($query) or error(__FILE__, __LINE__);
		
		// Add the new extension
		$query = array(
			'INSERT'	=> 'id, title, version, description, author',
			'INTO'		=> 'extensions',
			'VALUES'	=> '\''.$forum_db->escape('anycode_'.$new_sol_name).'\', \''.$forum_db->escape('anycode title').'\', \''.$forum_db->escape('0.0.0').'\', \''.$forum_db->escape('This is part of AnyCode extension').'\', \''.$forum_db->escape('author').'\''
		);

		($hook = get_hook('anycode_add_sol_qr_add_ext')) ? eval($hook) : null;
		$forum_db->query_build($query) or error(__FILE__, __LINE__);		

		($hook = get_hook('anycode_add_sol_pre_redirect')) ? eval($hook) : null;
		redirect(SOLUTION_PATH, $lang_anycode['Solution added'].' '.$lang_admin_common['Redirect']);
	}
}

// Delete a solution
else if (isset($_POST['del_sol']) || isset($_POST['del_sol_comply']))
{
	
	if (!isset($_POST['sol_to_delete']))
		message($lang_common['Bad request']);
	
	$sol_to_delete = intval($_POST['sol_to_delete']);
	if ($sol_to_delete < 1)
		message($lang_common['Bad request']);

	// User pressed the cancel button
	if (isset($_POST['del_sol_cancel']))
		redirect(SOLUTION_PATH, $lang_admin_common['Cancel redirect']);

	($hook = get_hook('anycode_del_sol_form_submitted')) ? eval($hook) : null;

	if (isset($_POST['del_sol_comply']))	// Delete a solution with all hooks
	{
		
		// Validate the CSRF token
		if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== generate_form_token(get_current_url()))
			csrf_confirm_form();			
		
		@set_time_limit(0);

		$query = array(
			'SELECT'	=> 's.name',
			'FROM'		=> 'anycode_solutions AS s',
			'WHERE'		=> 's.id='.$sol_to_delete
		);
		
		($hook = get_hook('anycode_del_sol_qr_get_name_to_delete')) ? eval($hook) : null;
		$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);

		if (!$forum_db->num_rows($result))
			message($lang_common['Bad request']);	

		$cur_solution = $forum_db->fetch_assoc($result);

		// Delete hooks
		$query = array(
			'DELETE'	=> 'extension_hooks',
			'WHERE'		=> 'extension_id = \''.$forum_db->escape('anycode_'.$cur_solution['name']).'\''
		);
		
		($hook = get_hook('anycode_del_sol_qr_delete_ext_hooks')) ? eval($hook) : null;
		$forum_db->query_build($query) or error(__FILE__, __LINE__);

		// Delete extension
		$query = array(
			'DELETE'	=> 'extensions',
			'WHERE'		=> 'id = \''.$forum_db->escape('anycode_'.$cur_solution['name']).'\''
		);
		
		($hook = get_hook('anycode_del_sol_qr_delete_ext')) ? eval($hook) : null;
		$forum_db->query_build($query) or error(__FILE__, __LINE__);		
		
		$query = array(
			'DELETE'	=> 'anycode_hooks',
			'WHERE'		=> 'solution_id = '.$sol_to_delete
		);
		
		($hook = get_hook('anycode_del_sol_qr_delete_sol_hooks')) ? eval($hook) : null;
		$forum_db->query_build($query) or error(__FILE__, __LINE__);
		
		// Delete the solution
		$query = array(
			'DELETE'	=> 'anycode_solutions',
			'WHERE'		=> 'id='.$sol_to_delete
		);

		($hook = get_hook('anycode_del_sol_qr_delete_solution')) ? eval($hook) : null;
		$forum_db->query_build($query) or error(__FILE__, __LINE__);

		// Empty the PHP cache
		forum_clear_cache();

		// Regenerate the hooks cache
		if (!defined('FORUM_CACHE_FUNCTIONS_LOADED'))
			require FORUM_ROOT.'include/cache.php';

		generate_hooks_cache();

		($hook = get_hook('anycode_del_sol_pre_redirect')) ? eval($hook) : null;

		redirect(SOLUTION_PATH, $lang_anycode['Solution deleted'].' '.$lang_admin_common['Redirect']);
	}
	else	// If the user hasn't comfirmed the delete
	{
		$query = array(
			'SELECT'	=> 's.name',
			'FROM'		=> 'anycode_solutions AS s',
			'WHERE'		=> 's.id='.$sol_to_delete
		);

		($hook = get_hook('anycode_del_sol_qr_get_solution_name')) ? eval($hook) : null;
		$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);
		if (!$forum_db->num_rows($result))
			message($lang_common['Bad request']);

		$solution = $forum_db->fetch_assoc($result);

		// Setup the form
		$forum_page['form_action'] = SOLUTION_PATH;

		$forum_page['hidden_fields'] = array(
			'csrf_token'	=> '<input type="hidden" name="csrf_token" value="'.generate_form_token($forum_page['form_action']).'" />',
			'cat_to_delete'	=> '<input type="hidden" name="sol_to_delete" value="'.$sol_to_delete.'" />'
		);

		// Setup breadcrumbs
		$forum_page['crumbs'] = array(
			array($forum_config['o_board_title'], forum_link($forum_url['index'])),
			array($lang_admin_common['Forum administration'], forum_link($forum_url['admin_index'])),
			array($lang_anycode['AnyCode'], SOLUTION_PATH),
			$lang_anycode['Delete solution']
		);

		($hook = get_hook('anycode_del_sol_pre_header_load')) ? eval($hook) : null;

		define('FORUM_PAGE_SECTION', 'anycodetool');
		define('FORUM_PAGE', 'admin-anycode-solutions');		
		
		require FORUM_ROOT.'header.php';

		// START SUBST - <!-- forum_main -->
		ob_start();

		($hook = get_hook('anycode_del_sol_output_start')) ? eval($hook) : null;

?>
	<div class="main-subhead">
		<h2 class="hn"><span><?php printf($lang_anycode['Confirm delete sol'], forum_htmlencode($solution['name'])) ?></span></h2>
	</div>
	<div class="main-content main-frm">
		<div class="ct-box warn-box">
			<p class="warn"><?php echo $lang_anycode['Delete solution warning'] ?></p>
		</div>
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo $forum_page['form_action'] ?>">
			<div class="hidden">
				<?php echo implode("\n\t\t\t\t", $forum_page['hidden_fields'])."\n" ?>
			</div>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="del_sol_comply" value="<?php echo $lang_anycode['Delete solution'] ?>" /></span>
				<span class="cancel"><input type="submit" name="del_sol_cancel" value="<?php echo $lang_admin_common['Cancel'] ?>" /></span>
			</div>
		</form>
	</div>
<?php

		($hook = get_hook('anycode_del_sol_end')) ? eval($hook) : null;

		$tpl_temp = forum_trim(ob_get_contents());
		$tpl_main = str_replace('<!-- forum_main -->', $tpl_temp, $tpl_main);
		ob_end_clean();
		// END SUBST - <!-- forum_main -->
		require FORUM_ROOT.'footer.php';
	}
}

else if (isset($_POST['update']))	// Change solution
{

	// Validate the CSRF token
	if (!isset($_POST['csrf_token']) || $_POST['csrf_token'] !== generate_form_token(get_current_url()))
		csrf_confirm_form();	
		
	if (!isset($_POST['sol_name']))
		message($lang_common['Bad request']);
		
	$sol_name = array_map('trim', $_POST['sol_name']);
	
	if (!isset($_POST['sol_enable']))
		message($lang_common['Bad request']);
			
	$sol_enable = array_map('intval', $_POST['sol_enable']);

	($hook = get_hook('anycode_update_sol_form_submitted')) ? eval($hook) : null;

	$query = array(
		'SELECT'	=> 's.id, s.name,  s.enable',
		'FROM'		=> 'anycode_solutions AS s',
	);

	($hook = get_hook('anycode_update_sols_qr_get_solutions')) ? eval($hook) : null;
	$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);
	
	while ($cur_sol = $forum_db->fetch_assoc($result))
	{
		if (isset($sol_name[$cur_sol['id']]))
		{
			if ($sol_name[$cur_sol['id']] == '')
				message($lang_anycode['Must enter solution']);

			// We only want to update if we changed anything
			if ($cur_sol['name'] != $sol_name[$cur_sol['id']])
			{
				$query = array(
					'UPDATE'	=> 'anycode_solutions',
					'SET'		=> 'name=\''.$forum_db->escape($sol_name[$cur_sol['id']]).'\'',
					'WHERE'		=> 'id='.$cur_sol['id']
				);

				($hook = get_hook('anycode_upd_sol_qr_upd_name_sol')) ? eval($hook) : null;
				$forum_db->query_build($query) or error(__FILE__, __LINE__);
				
				//update core hooks
				$query = array(
					'UPDATE'	=> 'extension_hooks',
					'SET'		=> 'extension_id=\'anycode_'.$forum_db->escape($sol_name[$cur_sol['id']]).'\'',
					'WHERE'		=> 'extension_id=\''.$forum_db->escape('anycode_'.$cur_sol['name']).'\''
				);

				($hook = get_hook('anycode_update_sols_qr_update_hooks')) ? eval($hook) : null;
				$forum_db->query_build($query) or error(__FILE__, __LINE__);
				
			}
			
			if ($cur_sol['enable'] != $sol_enable[$cur_sol['id']]) {
				if ($sol_enable[$cur_sol['id']] == 1) {
					// update core hooks:
					// install enabled solution hooks into extension_hooks
					$query = array(
						'SELECT'	=> 'h.id, h.hook_id, h.code, h.enable',
						'FROM'		=> 'anycode_hooks AS h',
						'WHERE'		=> 'h.solution_id='.$cur_sol['id'].' AND h.enable=1'
					);

					($hook = get_hook('anycode_update_sol_qr_get_hooks')) ? eval($hook) : null;
					$hresult = $forum_db->query_build($query) or error(__FILE__, __LINE__);									if ($forum_db->num_rows($hresult)) {
						// есть хуки, инсталлируем их в ядро
						while ($cur_hook = $forum_db->fetch_assoc($hresult)){
							$query = array(
								'INSERT'	=> 'id, extension_id, code, installed, priority',
								'INTO'		=> 'extension_hooks',
								'VALUES'	=> '\''.$forum_db->escape(forum_trim($cur_hook['hook_id'])).'\', \''.$forum_db->escape('anycode_'.$cur_sol['name']).'\', \''.$forum_db->escape(forum_trim($cur_hook['code'])).'\', '.time().', '.(isset($cur_hook['priority']) ? $cur_hook['priority'] : 5)
							);
							($hook = get_hook('anycode_update_sol_qr_add_hook')) ? eval($hook) : null;
							$forum_db->query_build($query) or error(__FILE__, __LINE__);
						}
					}
				}
				else {
					// update core hooks:
					// uninstall unenabled solution hooks from extension_hooks		
					$query = array(
						'DELETE'	=> 'extension_hooks',
						'WHERE'		=> 'extension_id=\''.$forum_db->escape('anycode_'.$cur_sol['name']).'\''
					);

				($hook = get_hook('anycode_upd_sol_qr_delete_hooks')) ? eval($hook) : null;
				$forum_db->query_build($query) or error(__FILE__, __LINE__);
				}
				
				$query = array(
					'UPDATE'	=> 'anycode_solutions',
					'SET'		=> 'enable=\''. $sol_enable[$cur_sol['id']].'\'',
					'WHERE'		=> 'id='.$cur_sol['id']
				);

				($hook = get_hook('anycode_upd_sol_qr_upd_enbl_sol')) ? eval($hook) : null;
				$forum_db->query_build($query) or error(__FILE__, __LINE__);										}
		}
	}
	
	// Regenerate the hooks cache
	if (!defined('FORUM_CACHE_FUNCTIONS_LOADED'))
		require FORUM_ROOT.'include/cache.php';

	generate_hooks_cache();

	($hook = get_hook('anycode_update_sols_pre_redirect')) ? eval($hook) : null;

	redirect(SOLUTION_PATH, $lang_anycode['Solution updated'].' '.$lang_admin_common['Redirect']);
}

// Setup breadcrumbs
$forum_page['crumbs'] = array(
	array($forum_config['o_board_title'], forum_link($forum_url['index'])),
	array($lang_admin_common['Forum administration'], forum_link($forum_url['admin_index'])),
	array($lang_anycode['AnyCode'], $GLOBALS['base_url'].'/extensions/anycodetool/solutions.php')
);

($hook = get_hook('anycode_pre_header_load')) ? eval($hook) : null;

define('FORUM_PAGE_SECTION', 'anycodetool');
define('FORUM_PAGE', 'admin-anycode-solutions');

// Fetch some info about the post, the topic and the forum
$query = array(
	'SELECT'	=> '*',
	'FROM'		=> 'anycode_solutions',
);

($hook = get_hook('anycode_select_solutions')) ? eval($hook) : null;

$result = $forum_db->query_build($query) or dbError(__FILE__, __LINE__);
$num_sol = $forum_db->num_rows($result);

for ($i = 0; $i < $num_sol; ++$i)
	$sol_list[] = $forum_db->fetch_assoc($result);

require FORUM_ROOT.'header.php';

// START SUBST - <!-- forum_main -->
ob_start();

$forum_page['item_count'] = 0;
$forum_page['form_action'] = SOLUTION_PATH;
$forum_page['hidden_fields'] = array(
	'csrf_token'	=> '<input type="hidden" name="csrf_token" value="'.generate_form_token($forum_page['form_action']).'" />'
);
$forum_page['group_count'] = $forum_page['item_count'] = $forum_page['fld_count'] = 0;

($hook = get_hook('anycode_main_output_start')) ? eval($hook) : null;

?>
	<div class="main-subhead">
		<h2 class="hn"><span><?php echo $lang_anycode['Add solution head'] ?></span></h2>
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

		($hook = get_hook('anycode_pre_sol_errors')) ? eval($hook) : null;

?>
		<div class="ct-box error-box">
			<h2 class="warn hn"><?php echo $lang_anycode['Solution errors'] ?></h2>
			<ul class="error-list">
				<?php echo implode("\n\t\t\t\t", $forum_page['errors'])."\n" ?>
			</ul>
		</div>
<?php

	}
	
	($hook = get_hook('anycode_pre_add_sol_fieldset')) ? eval($hook) : null; 
	
?>
			<div class="ct-box">
				<p><?php echo $lang_anycode['Add solution info'] ?></p>
			</div>
			<fieldset class="frm-group group<?php echo ++$forum_page['group_count'] ?>">
				<legend class="group-legend"><span><?php echo $lang_anycode['Add solution legend'] ?></span></legend>
<?php ($hook = get_hook('anycode_pre_new_sol_name')) ? eval($hook) : null; ?>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="sf-box text">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_anycode['New solution label'] ?></span></label><br />
						<span class="fld-input"><input type="text" id="fld<?php echo $forum_page['fld_count'] ?>" name="new_sol_name" size="42" maxlength="42" /></span>
					</div>
				</div>
<?php ($hook = get_hook('anycode_pre_add_sol_fieldset_end')) ? eval($hook) : null; ?>
			</fieldset>
<?php ($hook = get_hook('anycode_add_sol_fieldset_end')) ? eval($hook) : null; ?>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="add_sol" value="<?php echo $lang_anycode['Add solution'] ?>" /></span>
			</div>
		</form>
	</div>
<?php
($hook = get_hook('anycode_post_add_sol_form')) ? eval($hook) : null;

// Reset counter
$forum_page['group_count'] = $forum_page['item_count'] = 0;

if ($num_sol) 
{

?>
	<div class="main-subhead">
		<h2 class="hn"><span><?php echo $lang_anycode['Del solution head'] ?></span></h2>
	</div>
	<div class="main-content main-frm">
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo $forum_page['form_action'] ?>">
			<div class="hidden">
				<?php echo implode("\n\t\t\t\t", $forum_page['hidden_fields'])."\n" ?>
			</div>
<?php ($hook = get_hook('anycode_pre_del_sol_fieldset')) ? eval($hook) : null; ?>
			<fieldset class="frm-group group<?php echo ++$forum_page['group_count'] ?>">
				<legend class="group-legend"><strong><?php echo $lang_anycode['Delete solution'] ?></strong></legend>
<?php ($hook = get_hook('anycode_pre_del_sol_select')) ? eval($hook) : null; ?>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="sf-box select">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_anycode['Delete solution label'] ?></span> <small><?php echo $lang_admin_common['Delete help'] ?></small></label><br />
						<span class="fld-input"><select id="fld<?php echo $forum_page['fld_count'] ?>" name="sol_to_delete">
<?php

	foreach ($sol_list as $cur_solution)
	{
		echo "\t\t\t\t\t\t\t".'<option value="'. $cur_solution['id'].'">'.forum_htmlencode( $cur_solution['name']).'</option>'."\n";
	}

?>
						</select></span>
					</div>
				</div>
<?php ($hook = get_hook('anycode_pre_del_sol_fieldset_end')) ? eval($hook) : null; ?>
			</fieldset>
<?php ($hook = get_hook('anycode_del_sol_fieldset_end')) ? eval($hook) : null; ?>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="del_sol" value="<?php echo $lang_anycode['Delete solution'] ?>" /></span>
			</div>
		</form>
	</div>
<?php

	($hook = get_hook('anycode_post_del_sol_form')) ? eval($hook) : null;
	
	// Reset counter
	$forum_page['group_count'] = $forum_page['item_count'] = 0;
	
?>
	<div class="main-subhead">
		<h2 class="hn"><span><?php echo $lang_anycode['Edit solution head'] ?></span></h2>
	</div>
	<div class="main-content main-frm">
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo $forum_page['form_action'] ?>">
			<div class="hidden">
				<?php echo implode("\n\t\t\t\t", $forum_page['hidden_fields'])."\n" ?>
			</div>
<?php

	($hook = get_hook('anycode_edit_sol_fieldsets_start')) ? eval($hook) : null;
	foreach ($sol_list as $cur_solution) {

		$forum_page['item_count'] = 0;

		($hook = get_hook('anycode_pre_edit_cur_sol_fieldset')) ? eval($hook) : null;

?>
			<fieldset class="frm-group group<?php echo ++$forum_page['group_count'] ?>">
				<legend class="group-legend"><span><?php printf($lang_anycode['Edit solution legend'],  '<span class="hideme"> ('.forum_htmlencode($cur_solution['name']).')</span>') ?></span></legend>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
<?php ($hook = get_hook('anycode_pre_edit_sol_name')) ? eval($hook) : null; ?>
					<div class="sf-box text">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_anycode['Solution name label'] ?></span></label><br />
						<span class="fld-input"><input type="text" id="fld<?php echo $forum_page['fld_count'] ?>" name="sol_name[<?php echo $cur_solution['id'] ?>]" value="<?php echo forum_htmlencode($cur_solution['name']) ?>" size="42" maxlength="42" /></span>
					</div>
				</div>
<?php ($hook = get_hook('anycode_pre_enable_sol_checkbox')) ? eval($hook) : null; ?>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="mf-box">						
						<div class="mf-item">
							<span class="fld-input"><input type="radio" id="fld<?php echo ++$forum_page['fld_count'] ?>" name="sol_enable[<?php echo $cur_solution['id'] ?>]" value="1"<?php if ($cur_solution['enable'] == '1') echo ' checked="checked"' ?> /></span>
							<label for="fld<?php echo $forum_page['fld_count'] ?>"><?php echo $lang_anycode['Enable'] ?></label>
						</div>
						<div class="mf-item">
							<span class="fld-input"><input type="radio" id="fld<?php echo ++$forum_page['fld_count'] ?>" name="sol_enable[<?php echo $cur_solution['id'] ?>]" value="0"<?php if ($cur_solution['enable'] == '0') echo ' checked="checked"' ?> /></span>
							<label for="fld<?php echo $forum_page['fld_count'] ?>"><?php echo $lang_anycode['Disable'] ?></label>	
						</div>
					</div>							
				</div>				
<?php ($hook = get_hook('anycode_pre_edit_cur_sol_fieldset_end')) ? eval($hook) : null; ?>
			</fieldset>
<?php

		($hook = get_hook('anycode_edit_cur_sol_fieldset_end')) ? eval($hook) : null;
	}

	($hook = get_hook('anycode_edit_sol_fieldsets_end')) ? eval($hook) : null;

?>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="update" value="<?php echo $lang_anycode['Update all solutions'] ?>" /></span>
			</div>
		</form>
	</div>
<?php

	($hook = get_hook('anycode_post_edit_sol_form')) ? eval($hook) : null;	
}

($hook = get_hook('anycode_solution_end')) ? eval($hook) : null;

$tpl_temp = forum_trim(ob_get_contents());
$tpl_main = str_replace('<!-- forum_main -->', $tpl_temp, $tpl_main);
ob_end_clean();
// END SUBST - <!-- forum_main -->

require FORUM_ROOT.'footer.php';