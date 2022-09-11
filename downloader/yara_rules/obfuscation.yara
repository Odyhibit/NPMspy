rule two_byte_hex_obfuscation {
    meta:
        description = "lots of stuff like _0x012bef "
        category = "suspicious"
        author = "Josh Bloom"

    strings:
        $hex_string = /_0x[a-fA-F0-9]{4}/

    condition:
        #hex_string > 20
}

rule too_many_parameters_obfuscation {
    meta:
        description = "multiple functions with more than 80 parameters"
        category = "suspicious"
        author = "Josh Bloom"

    strings:
        $too_many_parameters = /function [A-Za-z]{2}\(([A-Za-z0-9]{1,2},){80}/

    condition:
        #too_many_parameters > 5
}

rule url_encode_control_chars {
    meta:
        description = "URL encoded control characters %00 - %09"
        category = "suspicious"
        author = "Josh Bloom"

    strings:
        $url_control_chars = /%0[0-9]/

    condition:
        #url_control_chars > 500
}

rule hex_escape_codes {
    meta:
        description = "lots of hex encoded characters"
        category = "suspicious"
        author = "Josh Bloom"

    strings:
        $url_control_chars = /\\x[A-Za-z0-9]{2}/

    condition:
        #url_control_chars > 500
}

rule double_backslash {
    meta:
        description = "double backslash and number"
        category = "suspicious"
        author = "Josh Bloom"

    strings:
        $double_backslash = /\\\\[0-9]{1,2}/

    condition:
        #double_backslash > 500
}
