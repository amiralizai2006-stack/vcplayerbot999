from dotenv import dotenv_values
import argparse
import os

from utils.Singleton import Singleton


class Config(metaclass=Singleton):
    def getCLIParser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "-env",
            "--Environment",
            help="[optional]Provide environment (local/prod)",
        )
        return parser

    def __init__(self) -> None:
        self.args = self.getCLIParser().parse_args()

        # Load .env if it exists, but ALWAYS let Faable/container
        # environment variables override values from the file.
        if self.args.Environment == "prod":
            file_config = dotenv_values(".env")
            environment = "prod"
        else:
            file_config = dotenv_values(".env.local")
            environment = "local"

        self.config = {
            **file_config,
            **os.environ,
        }

        self.config["env"] = environment
        self.config["source"] = "tgcalls"
        self.config["server"] = "tgserver-beta"

        self.config["ALLOWED_CHAT_TYPES"] = [
            "channel",
            "groups",
            "group",
            "supergroup",
            "supergroups",
            "megagroup",
        ]

        # Default URLs
        if not self.config.get("BOT_URL"):
            self.config["BOT_URL"] = "https://t.me/vcplayerbot"

        if not self.config.get("PARENT_URL"):
            self.config["PARENT_URL"] = "https://t.me/sktechhub"

        if not self.config.get("SUPPORT_GROUP"):
            self.config["SUPPORT_GROUP"] = "https://t.me/voicechatsupport"

        if not self.config.get("GITHUB_REPO"):
            self.config["GITHUB_REPO"] = (
                "https://github.com/kshubham506/vcplayerbot"
            )

        self.config["SUDO_USER"] = [563365858]
        self.config["PROMOTIONAL_DATA"] = {}

        # Number of simultaneous playbacks
        if not self.config.get("SIMULTANEOUS_CALLS"):
            self.config["SIMULTANEOUS_CALLS"] = 5

        # Footer text
        if "PLAYBACK_FOOTER" not in self.config:
            self.config["PLAYBACK_FOOTER"] = ""

        # Maximum queue size
        if not self.config.get("PLAYLIST_SIZE"):
            self.config["PLAYLIST_SIZE"] = 10

        # Maximum song/video duration
        if not self.config.get("ALLOWED_SONG_DURATION_IN_SEC"):
            self.config["ALLOWED_SONG_DURATION_IN_SEC"] = 13 * 60

        # Session string instructions
        if not self.config.get("SESSION_STRING_STEPS"):
            self.config["SESSION_STRING_STEPS"] = (
                "https://github.com/kshubham506/vcplayerbot/"
                "blob/master/get_session_string.md"
            )

        # Minimum members
        if "MIN_MEMBERS_REQUIRED" not in self.config:
            self.config["MIN_MEMBERS_REQUIRED"] = 0

        # Audio/video settings
        if "ALLOW_VIDEO" not in self.config:
            self.config["ALLOW_VIDEO"] = True

        if "ALLOW_AUDIO" not in self.config:
            self.config["ALLOW_AUDIO"] = True

        if "ALLOW_YOUTUBE" not in self.config:
            self.config["ALLOW_YOUTUBE"] = True

        if "ALLOW_OTHERS" not in self.config:
            self.config["ALLOW_OTHERS"] = True

        if "MAX_VIDEO_RES" not in self.config:
            self.config["MAX_VIDEO_RES"] = 1920

        if "MAX_AUDIO_RES" not in self.config:
            self.config["MAX_AUDIO_RES"] = 1920

        if "ALLOW_REPEAT" not in self.config:
            self.config["ALLOW_REPEAT"] = True

        # Allow the bot to work in multiple chats
        if "ALLOW_MULTIPLE_CHATS" not in self.config:
            self.config["ALLOW_MULTIPLE_CHATS"] = 1

    def get(self, key):
        return self.config.get(key)

    def getAll(self):
        return self.config

    def setExtraData(self, key, value):
        self.config[key] = value

    def setBotId(self, value):
        self.config["BOT_ID"] = value

    def setBotUsername(self, value):
        self.config["BOT_USERNAME"] = value
