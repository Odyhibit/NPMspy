rule shell_to_nc {
    meta:
        description = "interactive shell piped to nc "
        category = "malicious"
        author = "Josh Bloom"

    strings:
        $reverse_shell_string_1 = "bin/sh -i 2>&1|nc" ascii nocase
        $reverse_shell_string_2 = "bin/sh -i |nc" ascii nocase

    condition:
        $reverse_shell_string_1 or
        $reverse_shell_string_2
}