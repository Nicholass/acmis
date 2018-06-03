<?php

if (!defined('FORUM')) die();

$lang_smilies = array(
	'Smilies'				=> 'Smilies',
	
	'Title'					=> 'Smiley sets administration',
	'Forum default'			=> '(Forum\'s default)',
	'Default'				=> 'Default',
	'Edit'					=> 'Edit',
	'Delete'				=> 'Delete',
	'Download'				=> 'Download',
	'Upload'				=> 'Upload',
	
	'Editing'				=> 'Editing <strong>%s</strong>',
	'Edit dont'				=> '<strong>Note:</strong> Do <b>not</b> to use a single smiley more than once.</p><p class="warn"><strong>Help:</strong> To delete an image, delete its smileys and save the changes.</p>',
	'Edit save'				=> 'Save changes',
	'Edit duped'			=> 'You used the "%s" smiley twice.',
	'Edit add'				=> 'Add smiley',
	'Edit how'				=> '<strong>Help:</strong> Separate each smiley with a comma and space. I.e. ":), =)". Also, the image can\'t be bigger than the size set for avatars.',
	'Edit pic'				=> 'Image',
	'Edit combos'			=> 'Smileys',
	'Edit add'				=> 'Add smiley',
	'Edit no combos'		=> 'You did not specify any smilies for the uploaded image.',
	'Edit no image'			=> 'You did not select any image for upload.',
	'Edit used'				=> 'The "%s" smiley is already being used.',
	'Edit exists'			=> 'An image named "%s" already exists in that set.',
	
	'Successful default'	=> 'The default smiley set has been successfully changed.',
	'Successful delete'		=> 'The set has been successfully deleted.',
	'Successful edit'		=> 'The set has been successfully edited.',
	'Successful add'		=> 'The smiley has been successfully added.',
	
	'Errors'				=> '<strong>Important!</strong> The following errors occurred:',
	'Error no manifest'		=> 'The set "%1$s" doesn\'t have a manifest (\'%1$s.php\') on its folder.',
	'Error no combos'		=> 'The set "%s" doesn\'t have any smileys defined on its manifest.',
	'Error missing'			=> 'The set "%s" is missing a smiley \'%s\'.',
	'Error no sets'			=> 'There are no sets!',
	'Error no set'			=> 'This set does not exist!',
	'Invalid action'		=> 'Invalid action!',
	'Invalid set'			=> 'Invalid set!',
	'Change default'		=> 'The set you\'re trying to delete is the forum\'s default set. Please make another set the forum\'s default before deleting this set.',
	'No zip'				=> '<strong>Note:</strong> the script has dectected that your PHP instance doesn\'t have the ZIP extension, which is required for downloading and uploading sets as ZIP archives (these are not critical functions).',
	'No zip 2'				=> 'Your PHP instance doesn\'t have the ZIP extension.',
	
	'Back'					=> ' <a href="%s" onclick="history.go(-1);return false">Back</a>.',
)

?>