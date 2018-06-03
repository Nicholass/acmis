<?php
function get_word_at($phrase,$index){
	$word=" ";
	$i=-1;

	for($c=0;$c<$index;$c++){
		$j=$i;
		$word="";
		for($i=$j+1;$i<strlen($phrase);$i++){
			if($phrase[$i] == " ") break;
			else $word=$word.$phrase[$i];
		}
	}
	return $word;
}
?>