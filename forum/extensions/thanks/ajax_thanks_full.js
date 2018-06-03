function thank(postId)
{
	makeRequest(postId, {post: postId}, 'thank');
	jQuery('#thanks_button' + postId).hide();
}


function thanksSpoiler(postId)
{
	makeRequest(postId, {po: postId}, 'thanks_spoiler');
}

function makeRequest(postId, data, type) { 
	
	$.ajax({
		type: 'get',
		url: base_url_thanks + '/misc.php?action='+type,
		data: data,
		success: function(response) {
			jQuery('#spoiler_caption' + postId).hide();
			jQuery('#thanks' + postId).hide();
			jQuery('#spoiler_text' + postId).html(response).show();
		}
	});
}