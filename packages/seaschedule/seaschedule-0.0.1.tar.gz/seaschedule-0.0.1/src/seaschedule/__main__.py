import json
import logging
import os
import pandas as pd
import timeit
import traceback

from pathlib import Path
from string import Template
from time import sleep

from config import CFG, RUN_TIME
from seaschedule import maeu
from utils.email import send_mail
from utils.log import get_logger, format_log_message
from utils.sftp import put_files


RUN_TIME_STR = RUN_TIME.strftime("%Y%m%d_%H%M%S")
STATUS_PENDING = "PENDING"
STATUS_DISABLED = "DISABLED"
STATUS_SKIPPED = "SKIPPED"
STATUS_FAILED = "FAILED"
STATUS_SUCCESSFUL = "SUCCESSFUL"


def get_log_dir() -> Path:
    # Use path in config.toml if available, otherwise use <home-path>\seaschedule\log
    if CFG["environment"]["directory"]["log"]:
        log_dir = Path(CFG["environment"]["directory"]["log"])
    else:
        log_dir = Path.home().joinpath("seaschedule", "log")
    return log_dir


def get_data_dir() -> Path:
    # Use path in config.toml if available, otherwise use <home-path>\seaschedule\data
    if CFG["environment"]["directory"]["data"]:
        data_dir = Path(CFG["environment"]["directory"]["data"])
    else:
        data_dir = Path.home().joinpath("seaschedule", "data")
    return data_dir


def get_api_key(carrier: str) -> str:
    api_key = CFG[carrier]["api_key"]
    if not api_key:
        api_key = os.environ[CFG["environment"][carrier]["api_key"]]
    return api_key


def get_sftp_credential(app: str) -> tuple:
    sftp_credential = (os.environ[CFG["environment"][app]["sftp"]["username"]],
                        os.environ[CFG["environment"][app]["sftp"]["password"]])
    return sftp_credential


def get_smtp_host() -> str:
    smtp_host = os.environ[CFG["environment"]["smtp"]["host"]]
    return smtp_host


def main() -> None:
    # Init
    # Logging
    execution_start = timeit.default_timer()
    execution_elapsed = timeit.default_timer() - execution_start
    execution_successful = False
    task_step = 0
    task_name = ""
    task_start = timeit.default_timer()
    task_elapsed = timeit.default_timer() - task_start
    task_logs = []
    # Get directories and create them if not exists
    log_dir = get_log_dir()
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir.joinpath(CFG["logging"]["filename"].format(RUN_TIME_STR))
    data_dir = get_data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    # Initialize logger
    logger = get_logger(name=CFG["logging"]["logger"], log_file=str(log_file),
                        log_level=CFG["logging"]["level"], log_format=CFG["logging"]["format"])
    logger.info("Process started!")

    try:
        api_key = get_api_key("maeu")

        # Step-1: Retrieving active vessels
        task_step += 1
        task_name = "Retrieving active vessels"
        task_start = timeit.default_timer()
        vessels_file = data_dir.joinpath(CFG["maeu"]["vessels"]["filename"].format(RUN_TIME_STR, ".csv"))
        vessels_source_file = data_dir.joinpath(CFG["maeu"]["vessels"]["filename"].format(RUN_TIME_STR, ".txt"))
        vessel_master = pd.DataFrame()
        vessel_source_master = ""
        imos = []
        max_try = CFG["maeu"]["vessels"]["max_try"]
        retry_second = CFG["maeu"]["vessels"]["retry_second"]

        for i in range(1, max_try + 1):
            res_code = 0
            try:
                vessel_master, res_code, vessel_source_master = maeu.get_active_vessels(api_key)
                if not vessel_master.empty:
                    imos = vessel_master["imo"].tolist()
                    vessel_master.to_csv(vessels_file, encoding="utf-8", index=False)
                    with open(str(vessels_source_file), "w", encoding="utf-8") as f:
                        f.write(vessel_source_master)
                    task_elapsed = timeit.default_timer() - task_start
                    logger.info(
                        f"Step-{task_step}: {task_name} completed successfully in {task_elapsed:.2f} seconds"
                        f", # of active vessels = {len(imos)}.")
                    task_logs.append({"step": str(task_step), "name": task_name, "status": STATUS_SUCCESSFUL,
                                      "remarks": f"# of active vessels = {len(imos)}", "seconds": task_elapsed})
                    break
                else:
                    raise ValueError(vessel_source_master)
            except Exception as e:
                if i >= max_try:
                    # Stop retry and rethrow exception if this is the last try
                    raise
                else:
                    logger.warning(
                        f"Step-{task_step}: {task_name} try #{i} failed: {e}. Retry in {retry_second} seconds.")
                    sleep(retry_second)

        # Step-2: Retrieving vessel schedules
        task_step += 1
        task_name = "Retrieving vessel schedules"
        task_start = timeit.default_timer()
        schedules_file = data_dir.joinpath(CFG["maeu"]["schedules"]["filename"].format(RUN_TIME_STR, ".csv"))
        schedules_source_file = data_dir.joinpath(CFG["maeu"]["schedules"]["filename"].format(RUN_TIME_STR, ".json"))
        schedule_master = pd.DataFrame()
        schedule_source_master = ""
        carriers = CFG["maeu"]["schedules"]["carriers"]
        max_imo = CFG["maeu"]["schedules"]["max_imo"]
        imo_count = 0
        request_count = 0
        schedule_count = 0
        max_try = CFG["maeu"]["schedules"]["max_try"]
        retry_second = CFG["maeu"]["schedules"]["retry_second"]

        # DEBUG
        # max_imo = 20
        # imos = ["9857157"]
        # carriers = ["MAEU"]

        for imo in imos:
            if max_imo != -1 and imo_count >= max_imo:
                break
            for carrier in carriers:
                for i in range(1, max_try + 1):
                    schedule_data = pd.DataFrame()
                    res_code = 0
                    res_text = ""
                    try:
                        request_count += 1
                        logger.info(f"> [{request_count}] Retrieving schedule of {imo}/{carrier}.")
                        # Get schedule by imo + carrier
                        schedule_data, res_code, res_text = \
                            maeu.get_vessel_schedule(api_key, imo, carrier, RUN_TIME.strftime("%Y-%m-%d"),
                                                     CFG["maeu"]["schedules"]["data_range"])
                        if not schedule_data.empty:
                            if not schedule_source_master:
                                schedule_source_master = res_text
                            else:
                                schedule_source_master = schedule_source_master + ",\n" + res_text
                            # Append schedule to master
                            schedule_master = pd.concat([schedule_master, schedule_data], ignore_index=True)
                            logger.info(f"> [{request_count}] Retrieving schedule of {imo}/{carrier} completed.")
                            schedule_count += 1
                            break
                        else:
                            raise ValueError(res_text)
                    except Exception as e:
                        if i >= max_try or "Data not found" in str(e):
                            # Stop retry if this is the last try or no data for this imo
                            # error_msg = format_log_message(traceback.format_exc() + " --- " + str(e))
                            logger.error(
                                f"> [{request_count}] Retrieving schedule of {imo}/{carrier} failed.")
                            break
                        else:
                            logger.warning(
                                f"> [{request_count}] Retrieving schedule of {imo}/{carrier} failed. Retry in {retry_second} seconds.")
                            sleep(retry_second)
            imo_count += 1
        if not schedule_master.empty:
            schedule_master.to_csv(schedules_file, encoding="utf-8", index=False)
            with open(str(schedules_source_file), "w", encoding="utf-8") as f:
                # Add square brackets to make the consolidated responses a valid json document
                f.write("[" + schedule_source_master + "]")
            task_elapsed = timeit.default_timer() - task_start
            logger.info(
                f"Step-{task_step}: {task_name} completed successfully in {task_elapsed:.2f} seconds"
                f", # of schedules retrieved = {schedule_count}.")
            task_logs.append({"step": str(task_step), "name": task_name, "status": STATUS_SUCCESSFUL,
                              "remarks": f"# of schedules retrieved = {schedule_count}", "seconds": task_elapsed})
        else:
            raise ValueError("No vessel schedule can be retrieved.")

        # Task-3: Uploading to SFTP
        task_step += 1
        task_name = "Uploading to SFTP"
        task_start = timeit.default_timer()
        if not CFG["ib"]["sftp"]["enable"]:
            task_logs.append({"step": str(task_step), "name": task_name, "status": STATUS_DISABLED, "remarks": "",
                              "seconds": float("nan")})
        elif not schedules_file.exists():
            raise ValueError("No schedule file can be found for uploading.")
        else:
            max_try = 5
            retry_second = 5

            for i in range(1, max_try + 1):
                try:
                    sftp_username, sftp_password = get_sftp_credential("ib")
                    put_files(CFG["ib"]["sftp"]["host"], CFG["ib"]["sftp"]["port"], sftp_username, sftp_password,
                              [schedules_file], CFG["ib"]["sftp"]["remote_directory"])
                    task_elapsed = timeit.default_timer() - task_start
                    logger.info(
                        f"Step-{task_step}: {task_name} completed successfully in {task_elapsed:.2f} seconds.")
                    task_logs.append({"step": str(task_step), "name": task_name, "status": STATUS_SUCCESSFUL,
                                      "remarks": f"uploaded file = {Path(schedules_file).name}", "seconds": task_elapsed})
                    break
                except Exception as e:
                    if i >= max_try:
                        # Stop retry and rethrow exception if this is the last try
                        raise
                    else:
                        logger.warning(f"Step-{task_step}: {task_name} try #{i} failed: {e}. Retry in {retry_second} seconds.")
                        sleep(retry_second)
        execution_successful = True
    except Exception as e:  # AssertionError
        # logger.error(format_log_message(traceback.format_exc() + " --- " + str(e)))
        error_msg = format_log_message(traceback.format_exc() + " --- " + str(e))
        task_elapsed = timeit.default_timer() - task_start
        logger.error(f"Step-{task_step}: {task_name} failed: {error_msg}.")
        task_logs.append({"step": str(task_step), "name": task_name, "status": STATUS_FAILED,
                          "remarks": "", "seconds": task_elapsed})
    finally:
        # End
        execution_elapsed = timeit.default_timer() - execution_start
        logger.info(f"Process completed in {execution_elapsed:.2f} seconds.")

    # Sending notification email
    try:
        host = get_smtp_host()
        from_addr = CFG["email"]["from"]
        to_addrs = CFG["email"]["to"]
        cc_addrs = CFG["email"]["cc"]
        subject = CFG["email"]["subject"]
        body_template = Template(CFG["email"]["body"])
        if execution_successful:
            result_line = f'The process is completed <span style="font-weight:bold; color:green">' \
                          f'SUCCESSFULLY</span> in {execution_elapsed:.2f} seconds.'
        else:
            result_line = f'The process is <span style="font-weight:bold; color:red">' \
                          f'FAILED</span>. Please check the attached log for details.'
        log_summary = ""
        for task_log in task_logs:
            log_summary = log_summary + f'- Step-{task_log["step"]}: {task_log["name"]}' \
                                        f'......... {task_log["status"]} ({task_log["remarks"]})<br>'
        body = body_template.substitute({"result_line": result_line, "log_summary": log_summary})
        attachments = []
        if log_file.exists():
            attachments = [str(log_file)]
        send_mail(host=host, port=25, from_addr=from_addr, to_addrs=to_addrs, cc_addrs=cc_addrs,
                  subject=subject, body=body, files=attachments)
    except Exception as e:
        error_msg = format_log_message(traceback.format_exc() + " --- " + str(e))
        logger.error(f"Sending notification email failed: {error_msg}.")


if __name__ == "__main__":
    main()
