<?php
if (isset($_COOKIE['firststart-foz'])){
	header('Location: /bs');
}
else {
	SetCookie("firststart-foz");
	header('Location: /firststart');
}
?>
