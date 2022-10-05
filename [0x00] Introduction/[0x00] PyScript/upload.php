<?php
    if(!isset($_FILES["file"]))
        highlight_file(__file__) && die();
    $flag = file_get_contents('./flag');
    print($flag);
    print(gettype($flag));
    print_r( $_FILES["file"] );
    $node = @`node {$_FILES["file"]["tmp_name"]} 2>&1`;
    $python = @`python3 {$_FILES["file"]["tmp_name"]} 2>&1`;
    print($node);
    print(gettype($node));
    print("python here:");
    print($python);
    print(gettype($node));
    if($flag === $node && $flag === $python)
        echo 'Here is your Flag: '.$flag;
    else
        echo 'Fail :(';
?>
