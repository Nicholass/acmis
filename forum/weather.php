<?php

	//if ($argc == 1) exit;
	
	include_once("weather.inc.php"); 
	$gis = new gismeteo_presentation_layer(); 
	$gis->wfo->get(true);

?>
