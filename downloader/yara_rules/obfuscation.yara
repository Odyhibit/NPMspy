rule three_byte_hex_obfuscation {
    meta:
        description = "lots of stuff like _0x012bef "
        DB_entry = "Suspicious"
        author = "Josh Bloom"

    strings:
        $hex_string = /_0x[a-fA-F0-9]{6}/

    condition:
        #hex_string > 20
}