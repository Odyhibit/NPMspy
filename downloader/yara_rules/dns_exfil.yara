rule dns_exfil {
    meta:
        description = "dig used to exfiltrate info"
        category = "downloader"
        author = "Josh Bloom"

    strings:
        $dig = "dig `hostname|base64`" ascii

    condition:
        $dig
}

rule sideloading_package_from_url {
    meta:
    description = "install package using package.json -> install"
    category = "downloader"
    author = "Josh Bloom"

    strings:
        $installer = "\"install\": \"npm install http" ascii

    condition:
        $installer
}