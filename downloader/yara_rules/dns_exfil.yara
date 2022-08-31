rule dns_exfil {
    meta:
        description = "dig used to exfiltrate info"
        directory = "malware"
        author = "Josh Bloom"

    strings:
        $dig = "dig `hostname|base64`" ascii

    condition:
        $dig
}