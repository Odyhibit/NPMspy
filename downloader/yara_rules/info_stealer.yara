rule system_information_stealer {
    meta:
        description = "sends information it should not to someone "
        category = "info stealer"
        author = "Josh Bloom"

    strings:
        $process_string = "JSON.stringify(process)" ascii

        $info_1 = "os.hostname()" ascii
        $info_2 = "os.os.uptime()" ascii
        $info_3 = "os.networkInterfaces()" ascii

    condition:
        $process_string or 2 of ($info_*)
}

rule discord_information_stealer {
    meta:
        description = "steals discord information"
        category = "info stealer"
        author = "Josh Bloom"

    strings:
        $discord_1 = "/AppData/Roaming/discord/Local Storage/leveldb" ascii
        $discord_2 = "/AppData/Local/Google/Chrome/User Data/Default/Local Storage/leveldb"
        $discord_3 = "/AppData/Roaming/discordcanary/Local Storage/leveldb"
        $discord_4 = "/AppData/Roaming/Opera Software/Opera Stable/Local Storage/leveldb"
        $discord_5 = "/AppData/Local/BraveSoftware/Brave-Browser/User Data/Default/Local Storage/leveldb"
        $discord_6 = "/AppData/Local/Yandex/YandexBrowser/User Data/Default/Local Storage/leveldb"
    condition:
    2 of ($discord_*)
}