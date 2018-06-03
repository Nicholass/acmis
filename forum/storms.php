<?php 

$disallowed_warnings = array (
  'заморозки' => 21,
  'вітер' => 8,
  'хуртовина' => 15,
  'ожеледиця' => 13,
  
);

header('Content-Type: text/html; charset=utf-8');

$url = "http://meteo.gov.ua/ua/33345/storms/0/UA-30";

$ch = curl_init();

curl_setopt($ch, CURLOPT_URL, $url);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

$result = curl_exec($ch);
libxml_use_internal_errors(true);

$doc = new DOMDocument();
$doc->loadHTML($result);

$xpath = new DOMXpath($doc);

$elements = $xpath->query(".//div[@class='warn_wr']");

$result = '';

if (!is_null($elements)) {
  foreach ($elements as $key => $element) {
    $nodes = $element->childNodes;

    foreach ($nodes as $node) {
      if ($node->attributes) {
        $attributes = $node->attributes;
      
        for ($k=0; $k < $attributes->length; $k++) {
          if ($attributes->item($k)->nodeName == 'class' && strpos($attributes->item($k)->nodeValue, 'warn_cube') !== false) {
            //warn_cube1 = жовтий або заморозки? 
            if ($attributes->item($k+1)->nodeName == 'style' && strpos($attributes->item($k+1)->nodeValue, 'background-image') !== false) {
              //шукаємо style="background-image: url('http://meteo.gov.ua/pic/icons_storm/##.svg');
              
              if (preg_match('/.*('.implode('|',$disallowed_warnings).')\.svg.*/', $attributes->item($k+1)->nodeValue)) {
                continue 3;
              }
            }
          }
 
          if ($attributes->item($k)->nodeName == 'class' && strpos($attributes->item($k)->nodeValue, 'warn_cont') !== false) {
            //текст попередження
            $text = preg_replace('/^\h*\v+/m', '', $node->nodeValue);
            $result .= str_replace("\n", '', nl2br($text));
          }
        }
      }
    }
    if ($key < $elements->length - 1)
    $result .= "\n";
  }
}
file_put_contents('test.txt', $result);

echo file_get_contents('test.txt');
