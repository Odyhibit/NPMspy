rule stage_two_downloader {
    meta:
        description = "download then make executable "
        category = "malicious"
        author = "Josh Bloom"

    strings:
        $wget_string = "sudo wget HTTPS" ascii
        $chmod_string = "chmod +x" ascii

    condition:
        $wget_string and $chmod_string
}