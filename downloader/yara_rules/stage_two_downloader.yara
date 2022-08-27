rule download_then_execute {
    meta:
        description = "download then make a file executable "
        author = "Josh Bloom"

    strings:
        $wget_string = "sudo wget HTTPS" ascii
        $chmod_string = "chmod +x" ascii

    condition:
        $wget_string and $chmod_string
}