<?php
if (!defined('FORUM'))
	die();

if (!defined('FORUM_ROOT'))
	define('FORUM_ROOT', '../../');
require_once FORUM_ROOT.'include/common.php';
require_once FORUM_ROOT.'include/common_admin.php';

//define('FUNCTIONS_PATH', $base_url.'/extensions/pun_warning/functions.php');
define('EXTENSION_PATH', FORUM_ROOT.'extensions/pun_warning');	

function pun_warn_admin_menu(){
	global $ext_info, $forum_url, $forum_page, $forum_db, $forum_user, $lang_pun_warning, $warning_config;

}

function pun_warn_admin_section(){
	global $ext_info, $forum_url, $forum_page, $forum_db, $forum_user, $lang_pun_warning, $warning_config,$lang_common;
	
	if ($forum_user['g_id'] != FORUM_ADMIN)
	message($lang_common['No permission']);
	
	
	$warning_config=pun_warn_get_config();
?>	
		<div class="main-subhead">
			<h2 class="hn"><span><?php echo $lang_pun_warning['config_description'] ?></span></h2>
		</div>
		<div class="main-content main-frm">
			<?php pun_warn_admin_menu(); ?>
			<form action="<?php echo forum_link($forum_url['admin_extensions_pun_warning'].'?action=update_config') ?>" method="post" class="frm-form">

				<fieldset class="sf-set set1">
					<div class="sf-box text">
						<label for="fld_temp_ban">
							<span><?php echo $lang_pun_warning['temp_ban']?></span>
							<small><?php echo $lang_pun_warning['temp_ban_description']?></small>
						</label>
							<span class="fld-input"><input type="text" id="fld_temp_ban" name="temp_ban" value="<?php echo ($warning_config['temp_ban'] != '') ? $warning_config['temp_ban'] : ''; ?>"/></span>
					</div>
					<div class="sf-box text">
						<label for="fld_temp_ban_len">
							<span><?php echo $lang_pun_warning['temp_ban_len']?></span>
							<small><?php echo $lang_pun_warning['temp_ban_len_description']?></small>
						</label>
							<span class="fld-input"><input type="text" id="fld_temp_ban_len" name="temp_ban_len" value="<?php echo !empty($warning_config['temp_ban_len']) ? $warning_config['temp_ban_len'] : ''; ?>"/></span><br/>
					</div>
					<div class="sf-box text">
						<label for="fld_perm_ban">
							<span><?php echo $lang_pun_warning['perm_ban'] ?></span>
							<small><?php echo $lang_pun_warning['perm_ban_description']?></small>
						</label>
							<span class="fld-input"><input type="text" id="fld_perm_ban" name="perm_ban" value="<?php echo ($warning_config['perm_ban'] != '') ? $warning_config['perm_ban'] : ''; ?>"/></span><br/>
					</div>		
					<div class="sf-box checkbox">
						<label for="fld_email_user">
							<span><?php echo $lang_pun_warning['email_user']?></span>
							<?php echo $lang_pun_warning['email_user_description'] ?>
						</label>
							<span class="fld-input"><input type="radio" id="fld_email_user" name="notify" value="email" <?php echo ($warning_config['notify'] == 'email') ? 'checked="checked"' : ''; ?>/></span><br/>
					</div>
					<div class="sf-box checkbox">
						<label for="fld_email_user">
							<span><?php echo $lang_pun_warning['pm_user']?></span>
							<?php echo $lang_pun_warning['pm_user_description'] ?>
						</label>
							<span class="fld-input"><input type="radio" id="fld_pm_user" name="notify" value="pm" <?php echo ($warning_config['notify'] == 'pm') ? 'checked="checked"' : ''; ?>/></span><br/>
					</div>
					<div class="sf-box checkbox">
						<label for="fld_clear_warns">
							<span><?php echo $lang_pun_warning['clear_warns']?></span>
							<?php echo $lang_pun_warning['clear_warns_description'] ?>
						</label>
							<span class="fld-input"><input type="checkbox" id="fld_clear_warns" name="clear_warns" value="1" <?php echo !empty($warning_config['clear_warns']) ? 'checked="checked"' : ''; ?>/></span><br/>
					</div>					
					<div class="hidden">
						<input type="hidden" name="csrf_token" value="<?php echo generate_form_token(forum_link($forum_url['admin_extensions_pun_warning'].'?action=update_config')); ?>" />
					</div>
				</fieldset>
				<div class="frm-buttons">
						<span class="submit">
							<input type="submit" name="pun_warning_config_form" value="<?php echo $lang_pun_warning['save_settings'] ?>" />
						</span>
					</div>
			</form>
		</div>

<?php
}

function pun_warn_admin_crumbs(){
		global $ext_info, $forum_url, $forum_page, $forum_db, $forum_user;
		

?>

<?php
}

function pun_warn_topic_link(){
	global $forum_db, $lang_pun_warning,$ext_info,$forum_url,$cur_post,$forum_page,$forum_user,$cur_topic;
	
	//show user's number of current warnings
	$query=array('SELECT'	=>	'count(id) AS num_warnings',
				'FROM'		=>	'warning',
				'WHERE'		=>	'user_id='. intval($cur_post['poster_id']) . " AND affect_ban_counter = '1' AND expired = 0"
	);
	$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__FILE__);
//var_dump($forum_db->query_build($query,true));
	$result_luk=$forum_db->result($query);
	//var_dump($result_luk);
	$warns = '';
    	#    for ($i=0;$i<$result_luk['num_warnings'];$i++) {
        for ($i=0;$i<$result_luk;$i++) {
		$warns .= '<img src="'.$ext_info['url'].'/style/'.$forum_user['style'].'/luk.gif' .'" border="0" title="'.$lang_pun_warning['img_alt'].'" alt="'.$lang_pun_warning['img_alt'].'"/>';
	}
	
	return $forum_page['author_info']['warn'] = $warns;
		//print_r($forum_page['user_info']);
	
}

function pun_warn_update_config(){
	global $forum_db,$forum_url,$lang_pun_warning;
	
	if(isset($_POST['pun_warning_config_form'])){
		//form is sent. now update them
		
		//perform validation
		$conf['temp_ban']=($_POST['temp_ban'] != '') ? intval($forum_db->escape($_POST['temp_ban'])) : '1';
		$conf['perm_ban']=($_POST['perm_ban'] != '') ? intval($forum_db->escape($_POST['perm_ban'])) : '2';
		$conf['notify']=isset($_POST['notify']) ? $_POST['notify'] : 'email';
		$conf['clear_warns']=isset($_POST['clear_warns']) ? '1' : 0;
		$conf['temp_ban_len']=isset($_POST['temp_ban_len']) ? intval($forum_db->escape($_POST['temp_ban_len'])) : '1';
		
	
		foreach($conf as $key=>$value){
			$query=array(
					'UPDATE'	=>	'warning_config',
					'SET'		=>	"`conf_value`='".$value."'",
					'WHERE'		=>	"`conf_name`='".$key."'");
			$result=($forum_db->query_build($query));
			if($result){
				continue;
			} else {
				error($forum_db->error(),__FILE__,__LINE__);
			}
		}
		redirect(forum_link($forum_url['admin_extensions_pun_warning']), $lang_pun_warning['redirect']);
	}
}


//fetch configurations from database
function pun_warn_get_config(){
	global $forum_db;

	$query=array(
			'SELECT'=>'`conf_name`,`conf_value`',
			'FROM'=>'warning_config');
	$result=$forum_db->query_build($query) or error(__FILE__,__LINE__);
	
	$warning_config=array();
	while($conf=$forum_db->fetch_assoc($result)){
		$warning_config[$conf['conf_name']]=$conf['conf_value'];
	}
	return $warning_config;
}

function pun_warn_add(){ 
	global $ext_info, $forum_url, $forum_page, $forum_db, $forum_user, $lang_pun_warning, $warning_config;
	pun_warn_admin_crumbs();
?>
		
		<div class="main-content frm">
			<div class="main-subhead">
				<h2 class="hn"><span><?php echo $lang_pun_warning['add_warn'];?></span></h2>
			</div>
			<form action="<?php echo forum_link($forum_url['admin_extensions_pun_warning'].'?action=add_warn') ?>" method="post" class="frm-form">
				<div class="ct-box">
					<?php
					echo '<p>'.$lang_pun_warning['userid'].' : <a href="'.forum_link($forum_url['profile_about'],$_GET['uid']).'">'.urldecode($_GET['uid']).'</a></p>';
					echo '<p>'.$lang_pun_warning['username'].' : <a href="'.forum_link($forum_url['profile_about'],$_GET['uid']).'">'.urldecode($_GET['username']).'</a></p>';
					echo '<p>'.$lang_pun_warning['topic'].' : <a href="'.forum_link($forum_url['post'],$_GET['postid']).'">'.urldecode($_GET['topic']).'</a></p>';
					
					//show user's number of current warnings
					$query=array('SELECT'	=>	'count(id) AS num_warnings',
								'FROM'		=>	'warning',
								'WHERE'		=>	'user_id='. intval($_GET['uid']) . " AND affect_ban_counter = '1' AND expired = 0"
					);
					$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__FILE__);
					$result_luk=$forum_db->result($query);
					
					$query=array('SELECT'	=>	'count(id) AS num_warnings',
								'FROM'		=>	'warning',
								'WHERE'		=>	'user_id='. intval($_GET['uid']) . " AND affect_ban_counter != '1' AND expired = 0"
					);
					$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__FILE__);
					$result_klizma=$forum_db->result($query);
					echo '<p>'.$lang_pun_warning['num_warnings'].' : <a href="'.forum_link($forum_url['admin_extensions_pun_warning'].'?action=list_warn&uid='.$_GET['uid']).'">'.$result_luk['num_warnings'].'/'.$result_klizma['num_warnings'].' </a>';
					
					?>
				</div>
				<fieldset class="frm-group group1">
					<div class="txt-set set1">
						<div class="txt-box textarea">
							<label for="fld_warn_description">
								<span><?php echo $lang_pun_warning['warn_description']?></span>
							</label>
								<div class="txt-input"><span class="fld-input">
								<textarea id="fld_warn_description" name="warn_description" rows="10" cols="20"><?php
									$query=array('SELECT'	=>	'message',
											'FROM'		=>	'posts',
											'WHERE'		=>	'id='. intval($_GET['postid'])
									);
									$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__FILE__);
									$message = $forum_db->result($query);
									echo '[quote='.urldecode($_GET['username']).']' . forum_htmlencode($message) . '[/quote]';
								?></textarea></span></div><br/>
						</div>	
					</div>
					<div class="sf-set set1">
						<div class="sf-box checkbox">
							<label for="fld_affect_ban_counter"><span><?php echo $lang_pun_warning['affect_ban_counter']?></span><?php echo $lang_pun_warning['affect_ban_counter_description'] ?>	</label>
							<span class="fld-input"><input type="checkbox" id="fld_affect_ban_counter" name="affect_ban_counter" value="1" /> </span>
						</div>
					</div>
					<div class="hidden">
						<input type="hidden" name="csrf_token" value="<?php echo generate_form_token(forum_link($forum_url['admin_extensions_pun_warning'].'?action=add_warn')); ?>" />
						<input type="hidden" name="user_id" value="<?php echo !empty($_GET['uid']) ? $_GET['uid'] : ''; ?>" />
						<input type="hidden" name="post_id" value="<?php echo !empty($_GET['postid']) ? $_GET['postid'] : ''; ?>" />
						<input type="hidden" name="action" value="addwarning" />
					</div>
				</fieldset>
				<div class="frm-buttons">
						<span class="submit">
							<input type="submit" name="pun_warning_config_form" value="<?php echo $lang_pun_warning['save_settings'] ?>" />
						</span>
				</div>
			</form>
		</div>
	
<?php
}

function pun_warn_add2(){
	global $ext_info, $forum_url, $forum_page, $forum_db, $forum_user, $lang_pun_warning, $warning_config;
	//validate the values
	if(empty($_POST['user_id'])) message($lang_pun_warning['val_no_user']);
	if(empty($_POST['post_id'])) message($lang_pun_warning['val_no_post']);
	if(empty($_POST['warn_description'])) message($lang_pun_warning['val_no_description']);
	if($_POST['user_id']==$forum_user['id']) message($lang_pun_warning['same_user']);
	
	$affect_ban_counter = isset($_POST['affect_ban_counter']) ? ($_POST['affect_ban_counter']) : 0;
	
	$query=array('INSERT'	=>	'user_id,warned_by,post_id,description,created,modified,affect_ban_counter',
				'INTO'		=>	'warning',
				'VALUES'	=>	"'".$forum_db->escape($_POST['user_id'])."',
								'".$forum_db->escape($forum_user['id'])."',
								'".$forum_db->escape($_POST['post_id'])."',
								'".$forum_db->escape($_POST['warn_description'])."',
								'".time()."','".time()."',
								'".$forum_db->escape($affect_ban_counter)."'"
				);
	$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__LINE__);
	if($query){
		pun_warn_notify_user($forum_db->insert_id());
		pun_warn_process_ban($_POST['user_id']);
		//redirect(forum_link($forum_url['admin_extensions_pun_warning'].'?action=list_warn&uid='.$_POST['user_id']),$lang_pun_warning['warn_added']);
	} else {
		error($forum_db->error(),__FILE__,__LINE__);
	}
}
//edit function will be employed later
function pun_warn_edit($id=NULL){ //$id is the value of current ban record (if applicable)
	global $ext_info, $forum_url, $forum_page, $forum_db, $forum_user, $lang_pun_warning, $warning_config;
	pun_warn_admin_crumbs();
?>
		
		<div class="main-content frm">
			<div class="frm-head">
				<h2><span><?php echo $lang_pun_warning['add_warn'];?></span></h2>
			</div>
			<form action="<?php echo forum_link($forum_url['admin_extensions_pun_warning'].'?action=update_config') ?>" method="post" class="frm-form">
				<div class="frm-info">
					<?php
					echo '<p>'.$lang_pun_warning['userid'].' : <a href="'.forum_link($forum_url['profile_about'],$_GET['uid']).'">'.urldecode($_GET['uid']).'</a></p>';
					echo '<p>'.$lang_pun_warning['username'].' : <a href="'.forum_link($forum_url['profile_about'],$_GET['uid']).'">'.urldecode($_GET['username']).'</a></p>';
					echo '<p>'.$lang_pun_warning['topic'].' : <a href="'.forum_link($forum_url['post'],$_GET['postid']).'">'.urldecode($_GET['topic']).'</a></p>';
					
					//show number of current warnings
					$query=array('SELECT'	=>	'count(id) AS num_warnings',
								'FROM'		=>	'warning',
								'WHERE'		=>	'user_id='.intval($_GET['uid'])
					);
					$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__FILE__);
					$result=$forum_db->result($query);
					echo '<p>'.$lang_pun_warning['num_warnings'].' : <a href="'.forum_link($forum_url['admin_extensions_pun_warning'].'?action=listwarn&uid='.$_GET['uid']).'">'.$result['num_warnings'].'</a>';
					
					//fetch current ban information
					if(!empty($id)){
						$query=array('SELECT'	=>	'*',
									'FROM'		=>	'warning',
									'WHERE'		=>	'id='.$forum_db->escape($id),
									'LIMIT'		=>	1);
						$query=$forum_db->query_build($query);
						if($forum_db->num_rows($query))
							$cur_warn=$forum_db->fetch_assoc($query);	
					}
						
					
					?>
					</div>
					<fieldset class="frm-set set1">
					<div class="frm-fld text">
						<label for="fld_warn_description">
							<span class="fld-label"><?php echo $lang_pun_warning['warn_description']?></span>
							<span class="fld-input"><input type="text" id="fld_warn_description" name="warn_description" value="<?php echo !empty($cur_warn['description']) ? $cur_warn['description'] : ''; ?>"/></span><br/>
							
						</label>
					</div>	
					<div class="radbox checkbox">
						<label for="fld_affect_ban_counter">
							<span class="fld-label"><?php echo $lang_pun_warning['affect_ban_counter']?></span>
							<span class="fld-input"><input type="checkbox" id="fld_affect_ban_counter" name="affect_ban_counter" value="1" <?php echo !empty($cur_warn['affect_ban_counter']) ? 'checked="checked"' : ''; ?>/></span><br/>
							<span class="fld-extra"><?php echo $lang_pun_warning['affect_ban_counter_description'] ?></span>
							
						</label>
					</div>					
					<div class="hidden">
						<input type="hidden" name="csrf_token" value="<?php echo generate_form_token(forum_link($forum_url['admin_extensions_pun_warning'].'?action=add_')); ?>" />
						<input type="hidden" name="warn_id" value="<?php echo !empty($cur_warn['id']) ? $cur_warn['id'] : ''?>" />
					</div>
				</fieldset>
				<div class="frm-buttons">
						<span class="submit">
							<input type="submit" name="pun_warning_config_form" value="<?php echo $lang_pun_warning['save_settings'] ?>" />
						</span>
				</div>
					
				
				
			</form>
		</div>
	</div>
<?php
}

function pun_warn_notify_user($warn_id){
	global $ext_info, $forum_url, $forum_page, $forum_db, $forum_user, $lang_pun_warning, $warning_config, $forum_config, $lang_common, $affect_ban_counter;
	if(!$warn_id) error($lang_pun_warning['val_no_user'],__FILE__,__LINE__);
	
	//check notification setting
	$conf=pun_warn_get_config();

	//retrieve warning related data
	$query=array('SELECT'	=>	'*',
				'FROM'		=>	'warning',
				'WHERE'		=>	'id='.$forum_db->escape($warn_id),
				'LIMIT'		=>	1);
	$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__LINE__);
	$warn_info=$forum_db->fetch_assoc($query);
	
	//fetch user's total warning info
	$query=array('SELECT'	=>	'count(*) as num_warnings',
				'FROM'		=>	'warning',
				'WHERE'		=>	'user_id='.$forum_db->escape($warn_info['user_id'])." AND affect_ban_counter = '1' AND expired = '0'",
				'LIMIT'		=>	1);
	$query=$forum_db->query_build($query);
	$query=$forum_db->fetch_assoc($query);
	$warn_info['num_warnings']=$query['num_warnings'];
	
	$query=array('SELECT'	=>	'id, username, email, language',
				'FROM'		=>	'users',
				'WHERE'		=>	'id='.$forum_db->escape($warn_info['user_id']));
	$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__LINE__);
	$user_info=$forum_db->fetch_assoc($query);

	if($conf['notify'] == 'email' || $warn_info['num_warnings'] == $conf['temp_ban']) {
		//process the mail template.
		if (file_exists(EXTENSION_PATH.'/lang/'.$user_info['language'].'/'.$user_info['language'].'.mail.tpl')){
			$template=file_get_contents(EXTENSION_PATH.'/lang/'.$user_info['language'].'/'.$user_info['language'].'.mail.tpl');
		} else {
			$template=file_get_contents(EXTENSION_PATH.'/lang/English/English.mail.tpl');
		}

		if($template){
			//replace the template variables
			$template=str_replace('<username>',forum_htmlencode(forum_linebreaks($user_info['username'])),$template);
			$template=str_replace('<warning_type>',forum_htmlencode($affect_ban_counter == 0 ? $lang_pun_warning['enema'] : $lang_pun_warning['hatch']),$template);
			$template=str_replace('<warning_reason>',forum_htmlencode(forum_linebreaks($warn_info['description'])),$template);
			$template=str_replace('<post_url>',forum_link($forum_url['post'],$warn_info['post_id']),$template);
			$template=str_replace('<total_warnings>',$warn_info['num_warnings'],$template);
			$template=str_replace('<total_max_warnings>',$conf['temp_ban'],$template);
			$template=str_replace('<admin_email>',$forum_config['o_admin_email'],$template);
			$template=str_replace('<board_mailer>',sprintf($lang_common['Forum mailer'],$forum_config['o_board_title']),$template);
			
			
			//template is ready now. we can now email it
			@require_once(FORUM_ROOT.'include/email.php');
			@forum_mail($user_info['email'],$lang_pun_warning['mail_subject'],$template);
			return true;;			
		} else {
			message($lang_pun_warning['template_missing']);
			return false;
		}

	} elseif ($conf['notify'] == 'pm') {
		//send PM
		if (file_exists(EXTENSION_PATH.'/lang/'.$user_info['language'].'/'.$user_info['language'].'.pm.tpl')){
			$template=file_get_contents(EXTENSION_PATH.'/lang/'.$user_info['language'].'/'.$user_info['language'].'.pm.tpl');
		} else {
			$template=file_get_contents(EXTENSION_PATH.'/lang/English/English.pm.tpl');
		}

		if($template){
			//replace the template variables
			$template=str_replace('<username>',forum_htmlencode(forum_linebreaks($user_info['username'])),$template);
			$template=str_replace('<warning_type>',forum_htmlencode($affect_ban_counter == 0 ? $lang_pun_warning['enema'] : $lang_pun_warning['hatch']),$template);
			$template=str_replace('<warning_reason>',forum_htmlencode(forum_linebreaks($warn_info['description'])),$template);
			$template=str_replace('<post_url>',forum_link($forum_url['post'],$warn_info['post_id']),$template);
			$template=str_replace('<total_warnings>',$warn_info['num_warnings'],$template);
			$template=str_replace('<total_max_warnings>',$conf['temp_ban'],$template);
			$template=str_replace('<admin_email>',$forum_config['o_admin_email'],$template);
			$template=str_replace('<board_mailer>',sprintf($lang_common['Forum mailer'],$forum_config['o_board_title']),$template);


			//template is ready now. we can now email it
			pun_warn_send_pm($user_info['id'], $lang_pun_warning['mail_subject'], $template);
			return true;
		} else {
			message($lang_pun_warning['template_missing']);
			return false;
		}
	}
}

function pun_warn_send_pm($receiver_id, $subject, $body) {
	global $forum_user, $forum_db, $forum_config;
	// Save to DB
	$query = array(
			'INSERT'		=> 'sender_id, receiver_id, status, lastedited_at, read_at, subject, body',
			'INTO'			=> 'pun_pm_messages',
			'VALUES'		=> $forum_user['id'].', '.$receiver_id.', \'sent\', '.time().', 0, \''.$forum_db->escape($subject).'\', \''.$forum_db->escape($body).'\''
	);
	
	($hook = get_hook('pun_pm_fn_send_message_pre_new_send_query')) ? eval($hook) : null;
	
	$result = $forum_db->query_build($query) or error(__FILE__, __LINE__);
	
	pun_pm_clear_cache($receiver_id); // Clear cached 'New messages' in the user table
	
	($hook = get_hook('pun_pm_fn_send_message_pre_redirect')) ? eval($hook) : null;
	
}

function pun_warn_list_show_form()
{
	global $ext_info, $forum_url, $forum_page, $forum_db, $forum_user, $lang_pun_warning, $warning_config;
	pun_warn_admin_crumbs();
	pun_warn_admin_menu();
?>
	<div class="main-content frm">	
		<form action="<?php echo forum_link($forum_url['admin_extensions_pun_warning'].'?action=list_warn') ?>" method="post" class="frm-form">
			<div class="main-subhead">
				<h2 class="hn"><span><?php echo $lang_pun_warning['list_warn_info'] ?></span></h2>
			</div>
			<fieldset class="sf-set set1">
				<div class="frm-fld text">
					<label for="fld_user_id">
						<span class="fld-label"><?php echo $lang_pun_warning['userid']?></span>
						<span class="fld-input"><input type="text" id="fld_user_id" name="uid" value=""/></span><br/>
						
					</label>
				</div>						
				<div class="hidden">
					<input type="hidden" name="csrf_token" value="<?php echo generate_form_token(forum_link($forum_url['admin_extensions_pun_warning']).'?action=list_warn'); ?>" />
				</div>
			</fieldset>
			<div class="frm-buttons">
					<span class="submit">
						<input type="submit" name="pun_warning_list_warn_form" value="<?php echo $lang_pun_warning['list_warnings'] ?>" />
					</span>
			</div>

		</form>
	</div>
	
<?php
}
function pun_warn_list($uid='all'){
	global $ext_info, $forum_url, $forum_page, $forum_db, $forum_user, $lang_pun_warning, $warning_config;
	pun_warn_admin_crumbs();
	pun_warn_admin_menu();
	if(empty($uid)) message($lang_pun_warning['val_no_user']);
	
	if(strtolower($uid)=='all') {	
		$query=array('SELECT'	=>	'w.*,u.username',
				'FROM'		=>	'warning AS w,'.$forum_db->prefix.'users AS u',
				'WHERE'		=>	'w.user_id=u.id');
	} else {
		$query=array('SELECT'	=>	'w.*,u.username',
				'FROM'		=>	'warning AS w,'.$forum_db->prefix.'users AS u',
				'WHERE'		=>	'w.user_id=u.id AND w.user_id='.$forum_db->escape($uid));
	}
	$query['ORDER BY'] = 'created DESC';
				
	$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__LINE__);
	
	if(!$forum_db->num_rows($query)) message($lang_pun_warning['no_warning']);
	
?>
		<div class="main-content main-frm">
			<?php pun_warn_admin_menu(); ?>
		<div class="ct-box">	
			<?php
				echo '<p><b>'.$lang_pun_warning['list_account'] .'</b>: '.strtoupper($uid) .'</p><br/>';
				echo '<p><b>'.$lang_pun_warning['list_items'] .'</b>: '.$forum_db->num_rows($query) .'</p>'
			?>	
		</div>
	<div class="ct-group">
<?php
	//echo $forum_db->num_rows($query);
	$forum_page['item_num'] = 0;
	while($row=$forum_db->fetch_assoc($query)){
		//fetch details of each warning. we need username of warned_by, topic subject
		$query2=array('SELECT'=>'u.username as warned_by_name,t.id,t.subject',
					'FROM'	=>	'users AS u, '.$forum_db->prefix.'warning AS w',
					'JOINS'		=> array(
						array(
							'LEFT JOIN'	=> 'posts AS p',
							'ON'		=> 'p.id=w.post_id '
						),
						array(
							'LEFT JOIN'	=> 'topics AS t',
							'ON'		=> 't.id = p.topic_id'
						)
					),
					'WHERE'	=>	'w.id='.$forum_db->escape($row['id']).' AND u.id=w.warned_by',
					'LIMIT'	=>	1);
					
		$query2=$forum_db->query_build($query2) or error($forum_db->error(),__FILE__,__LINE__);
		$winfo=$forum_db->fetch_assoc($query2);
		
		$warn_type = 0;
		if ((int)$row["affect_ban_counter"] == 0) { //klizma
			$box_class = "klizma";
		} elseif ($row["expired"] == 0) {
			$box_class = "luk-active";
			$warn_type = 1;
		} else {
			$box_class = "luk-inactive";
			$warn_type = -1;
		}
?>	
		<div class="ct-set set<?php echo ++$forum_page['item_num'] ?>">
				<div class="ct-box <?php echo $box_class ?>">
					<div class="ct-legend">
						<h3 class="legend"><span><?php echo $lang_pun_warning['warned_by'].': <a href="'.forum_link($forum_url['profile_about'],$row['warned_by']).'"><b>'.forum_htmlencode($winfo['warned_by_name']).'</b></a>';?> </span></h3>
						<h3 class="legend"><span><?php echo $lang_pun_warning['warning_type'].': <b>'.($warn_type == 0 ? $lang_pun_warning['enema'] : $lang_pun_warning['hatch'] . ' ' . ($warn_type == 1 ? $lang_pun_warning['active'] : $lang_pun_warning['inactive'])).'</b>';?> </span></h3>
					</div>
				<?php 
				$user=!empty($row['username']) ? forum_htmlencode(forum_htmlencode($row['username'])) : $row['user_id'];
				?>
				<span><?php echo '<b>'.$lang_pun_warning['user'].'</b>: <a href="'.forum_link($forum_url['profile_about'],$row['user_id']).'">'.$user.'</a>';?> ::</span>
				<span><?php echo '<b>'.$lang_pun_warning['topic'].'</b> : <a href="'.forum_link($forum_url['post'],$row['post_id']).'">'.forum_htmlencode($winfo['subject']).'</a>';?></span>
				
				<h3 class="legend"></h3>
				<?php echo forum_htmlencode(forum_linebreaks($row['description']));?>
				
						<h3 class="legend"><span><?php echo '<b>'.$lang_pun_warning['add_date'] .'</b> : '. date('d M Y, h:ia',$row['created']); ?></span></h3>
					<?php if ($warn_type == -1) { ?>
						<h3 class="legend"><span><?php echo '<b>'.$lang_pun_warning['expire_date'] .'</b> : '. (($row['expired'] > 0) ? date('d M Y, h:ia', $row['modified']) : $lang_pun_warning['never']); ?></span></h3>
					<?php } ?>
				</div>
		</div>		
<?php				
	}
	?>
	</div>
	</div>
	<?php
}


function pun_warn_process_ban($uid=NULL){
		global $ext_info, $forum_url, $forum_page, $forum_db, $forum_user, $lang_pun_warning, $warning_config;
		
		if(empty($uid)) message($lang_pun_warning['val_no_user'].__FILE__.__LINE__);
		
		//check number of warnings
		$query=array('SELECT'	=>	'count(*) as num_warnings',
					'FROM'		=>	'warning',
					'WHERE'		=>	"affect_ban_counter='1' AND user_id='".$forum_db->escape($uid)."'  AND expired = 0"
		);
		$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__LINE__);
		$result=$forum_db->fetch_assoc($query);
		$config=pun_warn_get_config();
		
		//fetch userinfo
		$userinfo=array('SELECT'=>'username,email',
						'FROM'	=>'users',
						'WHERE'	=>	"id='".$forum_db->escape($uid)."'");
		$userinfo=$forum_db->query_build($userinfo) or error($forum_db->error(),__FILE__,__LINE__);
		$userinfo=$forum_db->fetch_assoc($userinfo);
		
		//before adding a new ban, we should clear any existing ban so that our latest ban works
		$query=array("DELETE"	=>	"bans",
					"WHERE"		=>	"username='".$forum_db->escape($userinfo['username'])."'");
		$query=$forum_db->query_build($query) or error($forum_db->error(),__FILE__,__LINE__);
		
		//check whether the user crossed the limit of permanent warning
		if (($config['perm_ban'] != 0) && ($result['num_warnings'] >= $config['perm_ban'])) {
			$query = array(
					'INSERT'	=> 'username, ip, email, message, expire, ban_creator',
					'INTO'		=> 'bans',
					'VALUES'	=> "'".$forum_db->escape($userinfo['username'])."','NULL', '".$forum_db->escape($userinfo['email'])."','".$forum_db->escape($lang_pun_warning['ban_perm_message'])."','NULL','".$forum_db->escape($forum_user['id'])."'");
			$query=$forum_db->query_build($query);
			if($query){
				//clear the ban cache
				include_once(FORUM_ROOT.'/include/cache.php');
				forum_clear_cache();
				redirect(forum_link($forum_url['admin_bans']),$lang_pun_warning['banned_perm']);
			} else {
				error($forum_db->error(),__FILE__,__LINE__);	
			}
			
		} elseif(($config['temp_ban'] != 0) && ($result['num_warnings'] >= $config['temp_ban'])) {
			//user has crossed temporary ban limit. so ban him
			//ban expire time
			$ban_expire=time()+(intval($config['temp_ban_len'])*24*60*60);
			$query = array(
					'INSERT'	=> 'username, ip, email, message, expire, ban_creator',
					'INTO'		=> 'bans',
					'VALUES'	=> "'".$userinfo['username']."','NULL', '".$userinfo['email']."','".$lang_pun_warning['ban_temp_message']."','".$ban_expire."','".$forum_user['id']."'");
			$query=$forum_db->query_build($query);
			if($query){
				//clear the ban cache
				include_once(FORUM_ROOT.'/include/cache.php');
				generate_bans_cache();
				redirect(forum_link($forum_url['admin_bans']),$lang_pun_warning['banned_temp']);
			} else {
				error($forum_db->error(),__FILE__,__LINE__);	
			}

		} else {
			redirect(forum_link($forum_url['admin_extensions_pun_warning'].'?action=list_warn&uid='.$uid),$lang_pun_warning['warn_added']);
		}
}

function pun_warn_clear_warns($ban_id){
	global $forum_db;
	
	//the ban will be removed. so we need to catch the value of $ban_id	 and fetch required information. if ban is removed, we can do nothing
	$conf=pun_warn_get_config();
	if($conf['clear_warns']){
		$query=array('SELECT'	=>	'u.id',
					'FROM'		=>	'users AS u,'.$forum_db->prefix.'bans AS b',
					'WHERE'		=>	'u.username=b.username AND b.id='.$forum_db->escape($ban_id)
		);

		$query = $forum_db->query_build($query) or error($forum_db->error(),__FILE__,__LINE__);
		
		$uid = $forum_db->fetch_assoc($query);

		$query=array('SELECT'	=>	'COUNT(*) AS cnt',
					'FROM'		=>	'warning',
					'WHERE'		=>	"user_id=".$forum_db->escape($uid['id'])." AND `expired`= 0 AND `affect_ban_counter` = '1'"
		);

		$query = $forum_db->query_build($query) or error($forum_db->error(),__FILE__,__LINE__);
		
		$count = $forum_db->fetch_assoc($query);
		
		if ($count['cnt'] >= $conf['temp_ban']) {
			//we have fetch the user id whose ban is going to be cleared. now remove all his/her warnings
			$query=array(
						'UPDATE'	=>	'warning',
						'SET'		=>	"`expired` = 1, modified = UNIX_TIMESTAMP()",
						'WHERE'  =>	"user_id=".$forum_db->escape($uid['id'])." AND `expired`= 0 AND `affect_ban_counter` = '1'"
			);

			$query = $forum_db->query_build($query) or error($forum_db->error(),__FILE__,__LINE__);
		}
		return;
	}
}

?>
