<?php
if (isset($_COOKIE['firststart-foz'])){
	header('Location: /bs');
}
else {
	SetCookie("firststart_isseseinfach");
	header('Location: /firststart');
}
?>
