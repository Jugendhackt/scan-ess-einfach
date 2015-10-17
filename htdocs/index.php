<?php
if (isset($_COOKIE['firststart-foz'])){
	header('Location: http://100.100.205.146/BS');
}
else {
	SetCookie("firststart-foz");
	header('Location: http://100.100.205.146/firststart');
}
?>