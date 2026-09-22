from extras.dbhandler import handle_db_calls
from extras.remove_old_files import removeOldFiles
from extras.shutdown import shutdown
from pyrogram import Client
from utils import config, logInfo, logWarning, logException
import signal
import sys
import asyncio
import os
import threading
import schedule


def run_threaded(job_func, arg):
    job_thread = threading.Thread(target=job_func, args=arg)
    job_thread.start()
    if len(arg) >= 3 and arg[2] is True:
        return schedule.CancelJob


def check_environment():
    print("========== FAABLE ENV TEST ==========")

    variables = [
        "API_ID",
        "API_HASH",
        "BOT_TOKEN",
        "USERBOT_SESSION",
        "MONGO_URL",
    ]

    for name in variables:
        value = os.environ.get(name)

        if value is not None and str(value).strip():
            print(f"{name}: PRESENT")
        else:
            print(f"{name}: MISSING")

    print("---------- CONFIG TEST ----------")

    for name in variables:
        value = config.get(name)

        if value is not None and str(value).strip():
            print(f"config.{name}: PRESENT")
        else:
            print(f"config.{name}: MISSING")

    print("====================================")


def main():
    loop = None
    bot = None

    try:
        # Test environment variables without printing their values
        check_environment()

        if (
            not config.get("API_ID")
            or not config.get("API_HASH")
            or not config.get("BOT_TOKEN")
            or (
                not config.get("USERBOT_SESSION")
                and not config.get("MONGO_URL")
            )
        ):
            print("RESULT: REQUIRED VARIABLE IS MISSING")

            logWarning(
                f"Please provide the required values in .env file, "
                f"Please check {config.get('SESSION_STRING_STEPS')} "
                f"on how to get the values"
            )

            sys.exit(0)

        print("RESULT: ALL REQUIRED VARIABLES ARE PRESENT")

        folders = ["images", "Logs"]

        for f in folders:
            if not os.path.exists(f):
                os.makedirs(f)

        loop = asyncio.get_event_loop()

        if config.get("env") == "prod":
            schedule.every(3).hours.do(
                run_threaded,
                removeOldFiles,
                ()
            )

        bot = Client(
            ":memory:",
            api_id=config.get("API_ID"),
            api_hash=config.get("API_HASH"),
            bot_token=config.get("BOT_TOKEN"),
            plugins=dict(root="modules"),
        )

        def sig_handler(signum, frame):
            logException(
                f"Segmentation Fault : {signum} : {frame}",
                True
            )

        signal.signal(signal.SIGSEGV, sig_handler)

        try:
            for signame in {"SIGINT", "SIGTERM"}:
                s = getattr(signal, signame)
                loop.add_signal_handler(
                    s,
                    lambda s=s: asyncio.create_task(
                        shutdown(s, loop)
                    )
                )
        except NotImplementedError:
            logWarning(
                "Not implemented on windows device. Can safely ignore."
            )

        bot.start()

        bot_details = bot.get_me()

        config.setBotId(bot_details.id)
        config.setBotUsername(bot_details.username)

        if config.get("MONGO_URL"):
            loop.create_task(handle_db_calls())

        loop.run_forever()

    except KeyboardInterrupt:
        logWarning(
            "Client Keyboard Interrupt, Exiting Service."
        )

    except Exception as ex:
        logException(
            f"Error in main method : {ex}",
            True
        )

    finally:
        logException(
            "Closed the service :)"
        )

        if bot is not None and bot.is_connected:
            bot.stop()


if __name__ == "__main__":
    try:
        logInfo(
            "Started the Backend Server For Voice Chat Music Player | "
            "A SkTechHub Product"
        )

        main()

    except Exception as ex:
        logException(
            f"Error in main start : {ex}",
            True
        )

    finally:
        logInfo("Closing the service :)")
        sys.exit(0)
