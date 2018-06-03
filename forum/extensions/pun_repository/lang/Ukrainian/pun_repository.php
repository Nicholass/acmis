<?php

/**
 * PunBB Repository extension language file
 *
 * @copyright Copyright (C) 2008 PunBB, partially based on code copyright (C) 2008 FluxBB.org
 * @license http://www.gnu.org/licenses/gpl.html GPL version 2 or higher
 * @package pun_repository
 */

if (!defined('FORUM')) die();

$lang_pun_repository = array(
	'Can\'t access repository'		=> '<strong>ПОМИЛКА!</strong> Сховище PunBB наразі недоступне. Спробуйте перевірити його пізніше.',
	'PunBB Repository'				=> 'Сховище PunBB',
	'Files mode and owner'			=> '<strong>ПРИМІТКА!</strong> Користувача системи вебсерверу буде встановлено як власника файлів і директорій, створених при завантаженні та встановленні розширень. Для створених директорій буде встановлено режим доступу  0777.',
	'Download and install'			=> 'Завантажити та встановити розширення',
	'Can\'t create directory'		=> '<strong>ПОМИЛКА!</strong> Неможливо створити підкаталог. Ймовірно, директорія \'extensions\' не має достатньо прав.',
	'Directory already exists'		=> '<strong>ПОМИЛКА!</strong> Директорія \'%s\' вже існує.',
	'Extension download failed'		=> '<strong>ПОМИЛКА!</strong> Невдале завантаження розширення.',
	'No writting right'				=> '<strong>ПОМИЛКА!</strong> Директорія \'extensions\' не має достатньо прав для створення файлів.',
	'Can\'t extract'				=> '<strong>ПОМИЛКА!</strong> Неможливо розпакувати файли із завантаженого архіву.',
	'Download successful'			=> 'Завантаження архіву пройшло успішно. Розширення готове до встановлення.',
	'Incorrect manifest.xml'		=> 'Завантаження архіву пройшло успішно, проте manifest.xml є хибним.',
	'Extract errors:'				=> 'При розпакуванні трапилися наступні помилки:',
	'Direct download links:'		=> 'Прямі посилання для завантаження:',
	'Can\'t write to cache file'	=> '<strong>ПОМИЛКА!</strong> Неможливо записати файл до кешу.',
	'All installed or downloaded'	=> '<strong>ПРИМІТКА!</strong> Ви встановили або завантажили всі доступні розширення. Вітаємо!',
	'Download and update'			=> 'Завантажити та оновити',
	'Unable to rename old dir'		=> '<strong>ПОМИЛКА!</strong>. Неможливо перейменувати директорію \'%s\' для оновлення розширення.',
	'Dependencies:'					=> 'Залежності:',
	'Resolve dependencies:'			=> 'Для встановлення цього розширення, будь ласка, розв\'яжіть спочатку наступні залежності:',
	'Clear cache'					=> 'Очистити кеш',
	'Unable to remove cached file'	=> 'Неможливо перенести кешований файл.',
	'Cache has been successfully cleared' => 'Кеш було успішно очищено',

	'Unsupported compression type'	=>	'Тип стискання не підтримується',
	'Supported types are'			=>	'Підтримуваними типами є \'gz\' та \'bz2\'',
	'The extension couldn\'t be found'	=>	'Розширення \'%s\' не може бути знайдене',
	'Please make sure your version of PHP was built with'	=>	'Будь ласка, переконайтеся, що ваша версія PHP підтримує\'%s\'',
	'Invalid string list'			=>	'Хибний список строк',
	'Unable to open in read mode'	=>	'Неможливо відкрити в режимі читання',
	'Unable to open in write mode'	=>	'Неможливо відкрити в режимі запису',
	'Unknown or missing compression type'	=>	'Тип стискання невідомий або відсутній',
	'Invalid file descriptor'		=>	'Хибний дескриптор файлу',
	'File does not exist'			=>	'Файл \'%s\' не існує',
	'Directory can not be read'		=>	'Неможливо прочитати директорію \'%s\'',
	'Invalid file name'				=>	'Хибне ім\'я файлу',
	'Unable to open file in binary read mode'	=>	'Файл \'%s\' неможливо відкрити в бінарному режимі читання',
	'Invalid block size'			=>	'Хибний розмір блоку',
	'Invalid checksum for file'		=>	'Хибне значення контрольної суми файлу',
	'calculated'					=>	'розрахунково',
	'expected'						=>	'очікувано',
	'Malicious .tar detected, file'	=>	'Виявлено небезпечний .tar, файл \' %s \' не встановлено в бажаному дереві директорій',
	'Invalid extract mode'			=>	'Хибний метод розпакування',
	'File already exists as a directory'	=>	'Файл \'%s\' вже існує як директорія',
	'Directory already exists as a file'	=>	'Директорія \'%s\' вже існує як файл',
	'File already exists and is write protected'	=>	'Файл \'%s\' наразі існує та захищений від запису',
	'Unable to create path for'		=>	'Неможливо створити шлях',
	'Unable to create directory'	=>	'Неможливо створити директорію',
	'Unable to extract symbolic link'	=>	'Неможливо розпакувати символьне посилання',
	'Error while opening {} in write binary mode'	=>	'Помилка при відкритті файлу {\'%s\'} в бінарному режимі запису',
	'Extracted file does not have the correct file size'	=>	'Хибний розмір файлу \'%s\' після розпакування',
	'Archive may be corrupted'		=>	'Архів, можливо, ушкоджено.',
	'Copy fail'						=>	'Неможливо скопіювати нові файли розширення до старої директорії %s.',

);

?>
