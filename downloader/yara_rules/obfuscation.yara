rule three_byte_hex_obfuscation {
    meta:
        description = "lots of stuff like _0x012bef "
        directory = "suspicious"
        author = "Josh Bloom"

    strings:
        $hex_string = /_0x[a-fA-F0-9]{4}/

    condition:
        #hex_string > 20
}