<?php
header("Access-Control-Allow-Origin: *");
header("Content-Type: application/json");

if (isset($_GET['url'])) {
  $csv_url = $_GET['url'];
  $csv_file = file_get_contents($csv_url);
  $csv_data = array_map('str_getcsv', explode("\n", $csv_file));
  $header = array_shift($csv_data);
  $output = array();
  
  foreach ($csv_data as $row) {
    $item = array();
    foreach ($row as $key => $value) {
      $item[$header[$key]] = $value;
    }
    $output[] = $item;
  }
  
  echo json_encode($output);
} else {
  echo "Error: CSV URL not provided";
}
?>
