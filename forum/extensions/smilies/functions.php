<?php

//For uninstall
function recursive_unlink($dir)
{
	if ($handle = opendir($dir))
	{
		while (false !== ($file = readdir($handle)))
		{
			if ($file != "." && $file != "..")
			{
				chmod($dir.'/'.$file, 0777);
				if(is_dir($dir.$file))
					recursive_unlink($dir.'/'.$file);
				else
					@unlink($dir.'/'.$file);
			}
		}
		closedir($handle);
		@rmdir($dir);
	}
}

function create_manifest($array, $fname)
{
	if(!$fh = @fopen($fname, 'wb'))
		die('Unable to create \''.$fname.'\'. Please make sure PHP has write access.');
	fwrite($fh, '<?php'."\n\n".'$combos = '.var_export($array, true).';'."\n\n".'?>');
	fclose($fh);
}

function get_sets($specific = false)
{
	global $lang_smilies, $base_url;
	
	$errors = $sets = array();
	
	if ($handle = opendir(FORUM_ROOT.'img/smilies'))
	{
		while (false !== ($file = readdir($handle)))
		{
			if ($file != "." && $file != ".." && is_dir(FORUM_ROOT.'img/smilies/'.$file) && substr($file, 0, 1) != '.')
			{
				if($specific !== false && $specific != $file)
					continue;
				
				if(!file_exists(FORUM_ROOT.'img/smilies/'.$file.'/'.$file.'.php'))
				{
					$errors[] = sprintf($lang_smilies['Error no manifest'], $file);
					continue;
				}
				
				include FORUM_ROOT.'img/smilies/'.$file.'/'.$file.'.php';
				
				if(!isset($combos) || !is_array($combos) || empty($combos))
				{
					$errors[] = sprintf($lang_smilies['Error no combos'], $file);
					continue;
				}
				
				foreach($combos as $k => $v)
				{
					if(!file_exists(FORUM_ROOT.'img/smilies/'.$file.'/'.$v))
						$errors[] = sprintf($lang_smilies['Error missing'], $file, $v);
					else
						$sets[$file][$k] = $v;
				}
			}
		}
		closedir($handle);
	}
	else
		return array('sets'=>$sets, 'errors'=>array('Could not read directory.'));
	
	if(empty($sets))
		$errors[] = $lang_smilies['Error no sets'];
	
	if(empty($sets) && $specific !== false)
		$errors[] = $lang_smilies['Error no set'];
	
	return array('sets'=>$sets, 'errors'=>$errors);
}

function group_combos($array)
{
	foreach($array as $k=>$v)
		$return[$v][] = $k;
	
	return $return;
}

function ungroup_combos($array)
{
	foreach($array as $k=>$v)
		foreach($v as $key)
			$return[$key] = $k;
	
	return $return;
}

function parse_form_combos($array)
{
	foreach($array as $k=>$v)
		foreach(explode(', ', $v) as $key)
			$return[$key] = $k;
	
	return $return;
}

function edit_page()
{
	global $lang_smilies, $result, $set, $forum_url, $forum_page;
	
	ob_start();
?>
	<div class="main-subhead">
		<h2 class="hn"><span><?php echo sprintf($lang_smilies['Editing'], $set) ?></span></h2>
	</div>
	<div class="main-content main-frm">
		<form class="frm-form" method="post" accept-charset="utf-8" action="<?php echo forum_link($forum_url['admin_settings_smilies_action2'], array('edit', $set)) ?>">
			<div class="hidden">
				<input type="hidden" name="csrf_token" value="<?php echo generate_form_token(forum_link($forum_url['admin_settings_smilies_action2'], array('edit', $set))) ?>" />
			</div>
			<div class="content-head">
				<h2 class="hn"><span><?php echo $lang_smilies['Smilies'] ?></span></h2>
			</div>
			<div class="ct-box">
				<p class="warn"><?php echo $lang_smilies['Edit dont'] ?></p>
			</div>
			<fieldset class="frm-group group<?php echo ++$forum_page['group_count'] ?>">
<?php
	foreach(group_combos($result['sets'][$set]) as $k=>$v)
	{
?>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="sf-box text">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><img src="<?php echo FORUM_ROOT.'img/smilies/'.$set.'/'.$k ?>" alt="<?php echo $k ?>"/></span></label><br />
						<span class="fld-input"><input type="text" id="fld<?php echo $forum_page['fld_count'] ?>" name="smilies[<?php echo $k ?>]" size="35" maxlength="50" value="<?php echo forum_htmlencode(implode(", ", $v)) ?>" />
					</div>
				</div>
<?php
	}
	$forum_page['group_count'] = $forum_page['item_count'] = 0;
?>
			</fieldset>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="save" value="<?php echo $lang_smilies['Edit save'] ?>" /></span>
			</div>
		</form>
		<form enctype="multipart/form-data" action="<?php echo forum_link($forum_url['admin_settings_smilies_action2'], array('edit', $set)) ?>" accept-charset="utf-8" method="post" class="frm-form">
			<div class="hidden">
				<input type="hidden" name="csrf_token" value="<?php echo generate_form_token(forum_link($forum_url['admin_settings_smilies_action2'], array('edit', $set))) ?>" />
			</div>
			<div class="content-head">
				<h2 class="hn"><span><?php echo $lang_smilies['Edit add'] ?></span></h2>
			</div>
			<div class="ct-box">
				<p class="warn"><?php echo $lang_smilies['Edit how'] ?></p>
			</div>
			<fieldset class="frm-group group<?php echo ++$forum_page['group_count'] ?>">
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="sf-box text">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_smilies['Edit pic'] ?></span></label><br />
						<span class="fld-input"><input type="file" id="fld<?php echo $forum_page['fld_count'] ?>" name="image" size="40" /></span>
					</div>
				</div>
				<div class="sf-set set<?php echo ++$forum_page['item_count'] ?>">
					<div class="sf-box text">
						<label for="fld<?php echo ++$forum_page['fld_count'] ?>"><span><?php echo $lang_smilies['Edit combos'] ?></span></label><br />
						<span class="fld-input"><input type="text" id="fld<?php echo $forum_page['fld_count'] ?>" name="smiley[combos]" size="35" maxlength="50" value="" /></span>
					</div>
				</div>
			</fieldset>
			<div class="frm-buttons">
				<span class="submit"><input type="submit" name="save" value="<?php echo $lang_smilies['Edit add'] ?>" /></span>
			</div>
		</form>
	</div>
<?php
	$return = forum_trim(ob_get_contents());
	ob_end_clean();
	
	return $return;
}