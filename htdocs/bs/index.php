<?php
if (isset($_COOKIE['firststart-foz'])){
	header('Location: /BS');
}
else {
	SetCookie("firststart-foz");
	header('Location: /firststart');
}
?>
