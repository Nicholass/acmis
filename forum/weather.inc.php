<?php
// www.ACIS.org.ua :: weather informer
// (c) 2006 sashman@gmail.com for ACIS.
//
// парсер данных гисметео.ру сдёрт со страницы:
// http://ptifun.kiev.ua/index.php?option=com_content&task=view&id=23&Itemid=1&pop=1&page=0&date=2005-08-01    
xx_init_gt();

if(isset($_GET['src']))
{
         highlight_file(__FILE__);
    die();
}

class weather_forecast
{
    var $fca        = false;
    var $town_id;
    var $file;
    var $http;
    //-//
    function weather_forecast($town=33345)
    {
        //echo 'crea';
        $suffix = "{$town}_1.xml";
        $this->town_id = $town;
        $this->file = $suffix;
        $this->http = "http://informer.gismeteo.ru/xml/$suffix";
	//$this->http = "http://xml.meteoservice.ru/export/gismeteo/point/25.xml";
    }
    //-//
    function is_stale()
    {
        if(!$this->fca) return true;
        $acdate = mktime ($this->fca[0]["HOUR"],0,0,$this->fca[0]["MONTH"],$this->fca[0]["DAY"],$this->fca[0]["YEAR"]);
        $now      = time();
        return ($acdate < $now);
    }
    //-//
    function fetch($force=false, $load = false)
    {
        $tl = time();
        //$tf = 
        if($force || !file_exists($this->file) || @ filectime($this->file) + 2*3600 < time() || time() < @ filectime($this->file))
        {
					if ($load) { //Ghost
						$ch = curl_init();
						curl_setopt ($ch, CURLOPT_URL, $this->http);
						curl_setopt ($ch, CURLOPT_RETURNTRANSFER, 1);
						$result = curl_exec ($ch);
						curl_close($ch);
						//echo $result;
						if (file_put_contents ($this->file, $result))
							return true;
						else return false;
								//return 	@ copy($result, $this->file);
					}
        }
        return true; //file exists and is not 2 hrs stale or not in future;
    }
    //-//
    function parse()
    {
        //echo ' x ' ;
        $this->fca = parseForecast($this->file);
        //print_r($fca);
        return $this->fca ? true:false;
        
    }
    //-//
    function get($load = false)
    {
        $this->fetch();
        if(!$this->parse())
        { 
            if(!$this->fetch(true, $load))    return false;
            if(!$this->parse())     return false;
        }
        elseif($this->is_stale())
        { 
            if(!$this->fetch(true, $load)) return false;
            if(!$this->parse())     return false;
        }
        return $this->fca;
    }
}
class gismeteo_presentation_layer
{
    /// Class for working with gismeteo xml parsed by the code block below and html output -- the w-data presentation
    var $rc = array();
    //var $town_id;
    var $wfo;
    var $forecast;
    function gismeteo_presentation_layer($town = 33345)
    {
        $this->wfo = new weather_forecast($town);
        
        $this->rc['days']         = array ('воскресенье', 'понедельник', 'вторник', 'среда', 'четверг', 'тяпница', 'суббота', '');
        $this->rc['daysp']         = array ('воскресенье', 'понедельник', 'вторник', 'среду', 'четверг', 'тяпницу', 'субботу', '');
        $this->rc['months']     = array ('нулебря','января','февраля','марта','апреля','мая','июня','июля','августа','сентября','октября','ноября','декабря','глюкобря');
        $this->rc['tod']         = array ('ночь', 'утро ','день ','вечер');
        $this->rc['precip']        = array ('4' => 'дождь', '5' => 'ливень', '6' => 'снег',  '7' => 'снег!',  '8' => 'гроза', '9' => 'нет данных об осадках', '10' => 'без осадков');
        $this->rc['precip_warn']= array (    '4' => 'Не ходите в коллекторы подземных рек и легкозатопляемые объекты', 
                                            '5'=>'Откажитесь от любых походов под землю.',
                                            '8'=>'Откажитесь от любых походов под землю и избегайте открытых пространств и металлических предметов', 
                                            '9'=>'Нет данных об осадках на этот период. Будьте бдительны', 
                                            -1 =>'Нет данных о погоде на этот период. Будьте бдительны');
        $this->rc['cloud']        = array ('0' => 'ясно', '1' => 'малооблачно', '2' => 'облачно', '3' => 'пасмурно');
        $this->rc['windd']        = array ('сев', 'c-вост', 'вост', 'ю-вост', 'ю', 'ю-зап', 'зап', 'с-зап', 'xx', '', '', '', '', '', '', '', '', '', '', '', '' );
        $this->rc['wind']        = array ('северный', 'cеверо-восточный', 'восточный', 'юго-восточный', 'южный', 'юго-западный', 'западный', 'северо-западный', 'xx', '', '', '', '', '', '', '', '', '', '', '', '' );
        $this->rc['winds']       = array ('северный', 'c-вост.', 'восточный', 'ю-вост.', 'южный', 'ю-зап.', 'западный', 'с-зап.', 'xx', '', '', '', '', '', '', '', '', '', '', '', '' );
        $this->rc['winde']        = array ('N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'xx', '', '', '', '', '', '', '', '', '', '', '', '' );
        $this->rc['pos_thunder']= array ('гроза возможна', 'гроза будет');
        $this->rc['pos_precip']    = array ('возможно', 'будет');
    }


    //////////////////////////////////////////////////////////////////////////
    function advisor($title,$body)
    {
        return    '<div class="acis">'.
                "<div class=\"pun\" > $title </div>".
                "<div class=\"acis_content\"> $body </div>".
                '</div>';
    }
    //////////////////////////////////////////////////////////////////////////
    function present($size=2, $advisor=1)
    // size:0 - no regular display (advisor only, if allowed)
    //        1 - small (one liner)
    //        2 - big
    //advisor:    0 - off
    //            1 - on (will warn users of bad weather conditions)
    {
        $warning_hours = -1;
        $warning_level = 10;
        $result = '';

        if(!($size||$advisor)) return;
        
            
        if(!$forecast = $this->wfo->get())
        {
            $result  .= $this->advisor("Прогноз погоды недоступен",$this->rc['precip_warn'][-1]);
            return $result ;
            
            $warning_level=-1;
            $advisor = 1;
            $size=0;
        }
        
    
        
	date_default_timezone_set('Europe/Kiev');//$forecast['TOWN']['SNAME']
        $ttb = 'Прогноз погоды для г. Киев, '.
		    (@ date('d.m.Y H:i', filectime($this->wfo->file))).
		    '  предоставлен <a href="http://www.gismeteo.ua/city/daily/4944/">Gismeteo.ua</a> | Другие сайты с прогнозом погоды: <a href="http://meteoinfo.by/5/?city=33345">meteoinfo.by</a> | <a href="http://rp5.ua/233/ru">rp5.ua</a> | <a href="http://radar.apphb.com/#Kiev:h:6:50.35247:30.97046">Карта погоды в текущий момент</a>';
        $bdy = '';
        $cnt = 0;
        
        //echo count($forecast);
        if($size>1)
            {
                //echo 'meh';
            foreach ($forecast as $k=>$v)
            {
                //echo 'x';
                //if(isset($_GET['snow'])) $v['PHENOMENA']['PRECIPITATION'] = 6;
				//$v['PHENOMENA']['PRECIPITATION'] = 6;
                if(!is_numeric($k)) continue;
                $arr_phen = $v['PHENOMENA'];
                $precip   = $arr_phen['PRECIPITATION'];
                $arr_pres = $v['PRESSURE'];
                $arr_temp = $v['TEMPERATURE'];
                $arr_wind = $v['WIND'];
                $arr_feel = $v['HEAT'];
                $arr_humi = $v['RELWET'];
                
                if($size>=1)
                {
                    $bdy.='<div style="float:left; padding:5px; width:250px;" class="acis_'.((++$cnt %2)?'odd':'even').'">';
                    
                    //if(!empty($bdy)) {$bdy .= '<hr/>';}
                    
                    //$bdy .=  "<div style=\"font-family: Verdana, Arial, Clean, Helvetica, sans-serif; font-size: 12px; height:100px; border:1px solid black;\">";

		    if(array_key_exists('old_informer',$_REQUEST))
		    {

                    $bdy .=  "<div style=\"margin-right:5px;float:left;clear:left;height:50px;width:50px;background-image:url('img/weather/cloud{$v['TOD']}{$arr_phen['CLOUDINESS']}.png');\">
                                        <img src=\"img/weather/prec{$v['PHENOMENA']['PRECIPITATION']}.gif\" alt=\"{$this->rc['precip'][$v['PHENOMENA']['PRECIPITATION']]}, {$this->rc['cloud'][$v['PHENOMENA']['CLOUDINESS']]} ({$this->rc['tod'][$v['TOD']]})\" title=\"{$this->rc['precip'][$v['PHENOMENA']['PRECIPITATION']]}, {$this->rc['cloud'][$v['PHENOMENA']['CLOUDINESS']]} ({$this->rc['tod'][$v['TOD']]})\" />

                                        </div>";

                    $bdy .=  "<div>{$this->rc['tod'][$v['TOD']]} ({$v['HOUR']}:00) ${v['DAY']} {$this->rc['months'][(int)$v['MONTH']]} </div>\n";
                    $bdy .=  "<div>{$this->rc['cloud'][$v['PHENOMENA']['CLOUDINESS']]} &mdash; {$this->rc['precip'][$v['PHENOMENA']['PRECIPITATION']]}; </div>\n";
                    $bdy .=  "<div>t = {$arr_temp['MIN']}&hellip;{$arr_temp['MAX']} &deg;C; P = {$arr_pres['MIN']}&hellip;{$arr_pres['MAX']} мм рт.ст.</div>\n";
                    $bdy .=  "<div>t &asymp; {$arr_feel['MIN']}&hellip;{$arr_feel['MAX']} &deg;C; H = {$arr_humi['MIN']}&hellip;{$arr_humi['MAX']} %</div>\n";
                    $bdy .=  "<div>Ветер {$this->rc['windd'][$arr_wind['DIRECTION']]}, {$arr_wind['MIN']}&hellip;{$arr_wind['MAX']} м/с</div>\n";
                    $bdy .='</div>';


		    }
		    else

		    {

		    $ta = sly_round($arr_temp['MIN'],$arr_temp['MAX'], 19, '&deg;', '&deg; C');
		    $tc = sly_round($arr_feel['MIN'],$arr_feel['MAX'], 19, '&deg;', '&deg; C');
		    $pr = sly_round($arr_pres['MIN'],$arr_pres['MAX'], 760, ' мм',' мм рт. ст.');
		    $hu = sly_round($arr_humi['MIN'],$arr_humi['MAX'], 60, '%', '%');
		    $wi = sly_round($arr_wind['MIN'],$arr_wind['MAX'], 2, ' м/с', ' м/с');
		    $alt = "{$this->rc['precip'][$v['PHENOMENA']['PRECIPITATION']]}, {$this->rc['cloud'][$v['PHENOMENA']['CLOUDINESS']]} ({$this->rc['tod'][$v['TOD']]})";

                    $bdy .=  
#				"<div style=\"margin-right:5px;float:left;clear:left;height:50px;width:50px;background-image:url('img/weather/cloud{$v['TOD']}{$arr_phen['CLOUDINESS']}.png');\">".
				"<div style=\"margin-right:5px;float:left;clear:left;height:50px;width:50px;background-repeat:no-repeat;background-position:center;background-image:url('img/weather/cl{$v['TOD']}{$arr_phen['CLOUDINESS']}.png');\">".
					"<img src=\"img/weather/prec{$v['PHENOMENA']['PRECIPITATION']}.gif\" ".
					" alt=\"{$alt}\" title=\"{$alt}\" /></div>";
                    
                    $bdy .=  "<div><span class=\"wx_has_title\" title=\"{$v['HOUR']}:00\">{$this->rc['tod'][$v['TOD']]}</span> ${v['DAY']} {$this->rc['months'][(int)$v['MONTH']]} </div>\n";
                    $bdy .=  "<div>{$ta}, {$this->rc['cloud'][$v['PHENOMENA']['CLOUDINESS']]}, {$this->rc['precip'][$v['PHENOMENA']['PRECIPITATION']]}</div>\n";

                    $bdy .=  "<div>давление {$pr}</div>\n";
                    $bdy .=  "<div>комфорт {$tc}, влажность {$hu}</div>\n";
                    $bdy .=  "<div>ветер {$this->rc['winds'][$arr_wind['DIRECTION']]}, {$wi}</div>\n";
                    $bdy .='</div>';

		    }
                }

                if($precip<9 && $warning_hours< 0 &&$precip!=6&&$precip!=7)
                {
                    $warning_level = $precip;
                    $warning_hours = $v['HOUR'];
                    $warning_prob  = $arr_phen['RPOWER'];
                }
            }

	    $result = '<style type="text/css">.wx_has_title {border-bottom: 1px dotted rgba(192,192,192,0.5);}</style>' . $result;
            $result.=$this->advisor($ttb,$bdy);
        }

        if($advisor&&($warning_hours >=0&&$warning_level<9&&$warning_level>3))
        {
			$warn= "<b>Внимание! Ожидается {$this->rc['precip'][$warning_level]}</b>";
        } else $warn= "";
		$result .= "<div style=\"clear:both;\"></div>".$this->advisor($warn,(@ $this->rc['precip_warn'][$warning_level]));
        return $result;
        
    }
}







/// /// /// /// PARSER CODE BELOW THIS LINE /// /// /// ///


function startElement($parser, $name, $attrs)
{
//    echo         'gax';
    global $current,$forecast,$fore_town;
    if($name=="TOWN")
    {
        $fore_town = $attrs;
        //$fore_town['SNAME'] = iconv("Windows-1251", "UTF-8", (urldecode($fore_town['SNAME'])));    
	$fore_town['SNAME'] = urldecode($fore_town['SNAME']);
    }
    if($name=="FORECAST")
        $forecast[count($forecast)]=$attrs;
        
    if(end($current)=="FORECAST")
        $forecast[count($forecast)-1][$name]=$attrs;
    array_push($current,"$name");
}
function endElement($parser, $name)
{
    global $current;
    array_pop($current);
}
function parseForecast($file)
{
    
    global $current,$forecast,$fore_town;
    $current = array();
    $forecast= array();
    $fore_town      = array();

		if (file_exists($file)) {
			$fp =  fopen($file, "r");
		} else {
        //echo 'bad file';
        return false;
    }

    $xml_parser = xml_parser_create();
    if(!$xml_parser) return false; //("bad xml parser");
    xml_set_element_handler($xml_parser, "startElement", "endElement");
    while ($data = fread($fp, 4096))
    {
        if (!xml_parse($xml_parser, $data, feof($fp))) 
        {
            return false;
        }
    }
    fclose($fp);
    xml_parser_free($xml_parser);
    //print_r($fore_town);
    $forecast['TOWN'] = $fore_town;
    return $forecast;
}

function checkVersion()
{
    global $forecast;
    //print_r($forecast);
    $acdate = mktime ($forecast[0]["HOUR"],0,0,$forecast[0]["MONTH"],$forecast[0]["DAY"],$forecast[0]["YEAR"]);
    $now  = time(); //mktime(date("h"), 0, 0, date("m")  , date("d"), date("Y"));
    if($now>$acdate)
    {
        //echo "- $now&gt;$acdate - file got stale -";
        return false;
    }
    else return true;
}
 
 
function getForecast($id=33345)
{
    if(!parseForecast($id)) return false;
    if(!checkVersion())
    {
        if(!parseForecast($id,true)) return false;
    }
    return true;
}

/// /// /// /// UTILITY CODE BELOW THIS LINE /// /// /// /// /// /// 
function get_hours($hrs)
{
    $hr = "ч";
    switch( $hrs %20 )
    {
        case 1:{$hr = "час" ;break;}
        case 2:
        case 3:
        case 4:{$hr = "часа" ;break;}
        default: {$hr="часов"; break;}
    }
    ;
    return $hr;
}


function xx_init_gt()
{
    global $xx_timer;
    $xx_timer = @microtime_float();
}
function sanitize_int($n)
{
        $n+=-10;
        $n = $n + 10;
        return $n;
}

function microtime_float()
{
   list($usec, $sec) = explode(" ", microtime());
   return ((float)$usec + (float)$sec);
}
function xx_print_gt()
{
    global $xx_timer;
    echo "<div style=\"color:#ccc;\">[GT :".(microtime_float() - $xx_timer).' s|<a href="http://validator.w3.org/check/referer">xhtml</a>|<a href="http://jigsaw.w3.org/css-validator/check/referer">css</a>]</div>';
}

function sly_round($a, $b, $thr=19, $units="", $units_full="")
{
    $avg = ($a+$b)/2;
    $dif = abs($a-$b);
    $rmo =  ($avg>$thr)?PHP_ROUND_HALF_UP:PHP_ROUND_HALF_DOWN;
    if($a == $b)
        return "{$a}{$units}";
    else
        return libsashman_format(
	    $dif>2?
	    '{1} &ndash; {2}{3}':
	    '<span class="wx_has_title" title="{1} &hellip; {2} {4}">{0}{3}</span>',
        round($avg,0,$rmo), min($a,$b), max($a,$b), $units, $units_full
    );
}

function libsashman_format($str)
{
    $arg_v = func_get_args();
    $arg_c = func_num_args();
    for($i = 1; $i< $arg_c; $i++)
    {
	$a = func_get_arg($i);
	$b = '{'.($i-1).'}';
	$str = str_replace($b,$a,$str);
    }
    return $str;
}


?> 
