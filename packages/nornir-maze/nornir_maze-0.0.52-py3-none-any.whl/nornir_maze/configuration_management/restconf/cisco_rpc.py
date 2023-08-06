#!/usr/bin/env python3
"""
This module contains Cisco specific RESTCONF operation RPC tasks and functions for Nornir. Other custom
RESTCONF tasks for the /data url are not part of this helper file. Please take a look to nr_restconf.

The functions are ordered as followed:
- Single Nornir RESTCONF tasks
- Nornir RESTCONF tasks in regular function
"""

import sys
import json
import time
import requests
from colorama import Fore, Style, init
from nornir.core.task import Task, Result
from nornir_maze.utils import print_task_name, task_host, task_info, task_error

init(autoreset=True, strip=False)


#### Single Nornir RESTCONF Tasks ############################################################################


def rc_cisco_operation_rpc_task(task: Task, rpc: str, payload: dict) -> Result:
    """
    This Nornir task is a wrapper for the Cisco specifiy operations RPCs with RESTCONF. All RPCs are POST
    operations and needs the RPC part of the URL e.g. cisco-ia:save-config and the payload as JSON encoded.
    """
    # RESTCONF HTTP URL
    operations = "/restconf/operations/"
    url = f"https://{task.host.hostname}:{task.host['restconf_port']}{operations}{rpc}"

    # RESTCONF HTTP header
    headers = {
        "Accept": "application/yang-data+json",
        "Content-Type": "application/yang-data+json",
    }

    # RESTCONF HTTP API call
    rc_response = requests.post(
        url=url,
        headers=headers,
        data=json.dumps(payload),
        auth=(task.host.username, task.host.password),
        verify=False,  # nosec
        timeout=120,
    )

    # Result dict to return as task result
    result = {
        "rpc": rpc,
        "url": url,
        "method": rc_response.request,
        "response": rc_response,
        "status_code": rc_response.status_code,
        "text": rc_response.text,
        "elapsed": rc_response.elapsed.total_seconds(),
    }

    return Result(host=task.host, result=result)


def rc_cisco_rpc_is_syncing_task(task: Task) -> Result:
    """
    This Nornir task executes the Cisco specific operations RESTCONF RPC cisco-ia:is-syncing to check if the
    configuration datastore is ready. If a sync is active the task backoff and try again until the datastore
    is ready. A dict with the task result will be returned at the end of the task.
    """
    # Backoff sleep and attempt values
    max_attempts = 5
    sleep = 10
    sleep_multiplier = 1.5

    # Result dict to return as task result
    result = {"result": ""}

    for _ in range(max_attempts):
        # Run the Nornir Task rc_cisco_operation_rpc_task cisco-ia:is-syncing
        rc_response = task.run(task=rc_cisco_operation_rpc_task, rpc="cisco-ia:is-syncing", payload={})

        # Verify RESTCONF response and update the task result variable
        if "Sync in progress" in rc_response.result["text"]:
            result["result"] += f"'Datastore sync in progress' -> OSResponse: <Sleep for {sleep}s>\n"
            time.sleep(sleep)
            sleep = sleep * sleep_multiplier

        else:
            # No datastore sync -> Return the result and end the task
            result["result"] += "'No datastore sync in progress' -> OSResponse: <Continue execution>"
            result.update(rc_response.result)

            return Result(host=task.host, result=result)

    # Datastore not ready after max_attempts -> Return failed result
    result["result"] = f"Datastore not ready after {max_attempts} retries OSResponse: <Sleep for {sleep}s>"
    result.update(rc_response.result)

    return Result(host=task.host, result=result, failed=True)


def rc_software_install_one_shot_task(task: Task) -> Result:
    """
    This custom Nornir task loads the software destination file which have to be installed from the Nornir
    inventory executes the Cisco specific operations RESTCONF RPC Cisco-IOS-XE-install-rpc:install to install
    a software file in a one-shot approach which will install, commit and reload the switch. The Nornir
    result object will be returned.
    """

    # Get the host destination file from the Nornir inventory
    dest_file = task.host["software"]["dest_file"]

    # Run the Nornir Task rc_cisco_operation_rpc_task with the rpc Cisco-IOS-XE-install-rpc:install
    result = task.run(
        task=rc_cisco_operation_rpc_task,
        rpc="Cisco-IOS-XE-install-rpc:install",
        payload={
            "Cisco-IOS-XE-install-rpc:input": {
                "uuid": f"Install {dest_file}",
                "one-shot": True,
                "path": f"flash:{dest_file}",
            }
        },
    )

    return Result(host=task.host, result=result)


def rc_install_remove_inactive_task(task: Task) -> Result:
    """
    This Nornir task executes the Cisco specific operations RESTCONF RPC Cisco-IOS-XE-install-rpc:remove to
    remove all not needed software packages and files on the filesystem. The custom Nornir result from the
    task rc_cisco_operation_rpc_task is returned for futher processing.
    """

    # Run the Nornir Task rc_cisco_operation_rpc_task with the rpc Cisco-IOS-XE-install-rpc:remove
    result = task.run(
        task=rc_cisco_operation_rpc_task,
        rpc="Cisco-IOS-XE-install-rpc:remove",
        payload={
            "Cisco-IOS-XE-install-rpc:input": {
                "uuid": "Install remove inactive",
                "inactive": True,
            },
        },
    )

    return Result(host=task.host, result=result)


#### Nornir RESTCONF tasks in regular Function ###############################################################


def print_rc_cisco_rpc_result(task_text, task_result, add_result=False, verbose=False):
    """
    This is a helper function to print the result of the Nornir tasks rc_cisco_operation_rpc_task. Task_result
    is the Nornir result object and with add_result a list will additional result strings can be added.
    """
    # Set the config_sttus to True
    config_status = True

    # Print results for each host
    for host in task_result:
        print(task_host(host=host, changed=task_result[host].changed))

        # If the task fails -> A Traceback is the result
        if isinstance(task_result[host].result, str):
            print(task_result[host].result)
            return False

        # If its a task result
        if isinstance(task_result[host].result, dict):
            index = 0
        # If its a sub-task result
        elif isinstance(task_result[host][1].result, dict):
            index = 1

        # Prepare all values for printing
        response = task_result[host][index].result["response"]
        elapsed = task_result[host][index].result["elapsed"]
        result = (
            f"\nRPC: {task_result[host][index].result['rpc']}\n"
            + f"URL: {task_result[host][index].result['url']}\n"
            + f"Method: {task_result[host][index].result['method']}\n"
            + f"Response: {response}\n"
            + f"Text: {task_result[host][index].result['text']}"
        )

        if (
            task_result[host][index].result["status_code"] == 200
            or task_result[host][index].result["status_code"] == 204
        ):
            print(task_info(text=task_text, changed=task_result[host].changed))
            print(f"'{task_text}' -> RestconfResponse {response} in {elapsed}s")
            # If add_result is True -> Print every list item
            if add_result:
                for item in add_result:
                    print(item)
            # If verbose is True -> Print the whole result
            if verbose:
                print(result)

        # cisco-ia:rollback success but with some not working rollback commands
        # This happen when commands change between software releases
        elif (task_result[host][index].result["status_code"] == 400) and (
            ("cisco-ia:rollback" and "inconsistent value") in result
        ):
            print(task_info(text=task_text, changed=task_result[host].changed))
            print(f"'{task_text}' -> RestconfResponse {response} in {elapsed}s")
            # If add_result is True -> Print every list item
            if add_result:
                for item in add_result:
                    print(item)
            # If verbose is True -> Print the whole result
            if verbose:
                print(result)

        else:
            print(task_error(text=task_text, changed=task_result[host].changed))
            print(f"'{task_text}' -> RestconfResponse {response} in {elapsed}s")
            # If add_result is True -> Print every list item
            if add_result:
                for item in add_result:
                    print(item)
            # Print the whole result
            print(result)
            # Set the config_sttus to False
            config_status = False

    return config_status


def rc_cisco_rpc_is_syncing(nr_obj, silent=False, verbose=False):
    """
    This function runs the custom Nornir task rc_cisco_rpc_is_syncing_task to verify the configuration
    datastore sync state on a Cisco device with RESTCONF. Its a Cisco specific RPC that is sent to the device.
    The result will be printed to std-out in custom Nornir style.
    """
    # Print the task name
    task_text = "RESTCONF verify is-syncing"
    print_task_name(task_text)

    # Run the Nornir Task rc_cisco_rpc_is_syncing_task
    task = nr_obj.run(task=rc_cisco_rpc_is_syncing_task, on_failed=True)

    # Print results for each host if silent is False
    for host in task:
        result = (
            f"\nRPC: {task[host].result['rpc']}\n"
            + f"URL: {task[host].result['url']}\n"
            + f"Method: {task[host].result['method']}\n"
            + f"Response: {task[host].result['response']}\n"
            + f"Text: {task[host].result['text']}"
        )

        # Print only failed results for each host if silent is True
        if silent:
            if task[host].failed:
                print(task_host(host=host, changed=task[host].changed))
                print(task_error(text=task_text, changed=task[host].changed))
                print(task[host].result["result"])
                print(result)
                # Set the config_sttus to False
                config_status = False

        elif task[host].failed:
            print(task_host(host=host, changed=task[host].changed))
            print(task_error(text=task_text, changed=task[host].changed))
            print(task[host].result["result"])
            print(result)
            # Set the config_sttus to False
            config_status = False

        else:
            print(task_host(host=host, changed=task[host].changed))
            print(task_info(text=task_text, changed=task[host].changed))
            print(task[host].result["result"])
            # If verbose is True
            if verbose:
                print(result)
            # Set the config_sttus to True
            config_status = True

    return config_status


def rc_cisco_rpc_save_config(nr_obj, verbose=False):
    """
    This function runs the custom Nornir task rc_cisco_operation_rpc_task to save the configuration on a Cisco
    device with RESTCONF. Its a Cisco specific RPC that is sent to the device. The result will be printed to
    std-out in Nornir style and the function return True or False depending wheather the task was successful.
    """
    # To verify the config status of each subtask and as function return
    config_status = True

    # Set the task name, info and error text
    task_text = "RESTCONF save config"

    # Print the task name
    print_task_name(text=task_text)

    # Run the Nornir Task rc_cisco_operation_rpc_task cisco-ia:save-config
    task = nr_obj.run(
        task=rc_cisco_operation_rpc_task, rpc="cisco-ia:save-config", payload={}, on_failed=True
    )

    # Print results for each host
    config_status = print_rc_cisco_rpc_result(task_text=task_text, task_result=task, verbose=verbose)

    return config_status


def rc_cisco_rpc_copy_file(nr_obj, task_name, source, destination, verbose=False):
    """
    This function runs the custom Nornir task rc_cisco_operation_rpc_task to copy a file from or to a Cisco
    device with RESTCONF. Its a Cisco specific RPC that is sent to the device. The result will be printed to
    std-out in  Nornir style and the function return True or False depending wheather the task was successful.
    """
    # To verify the config status of each subtask and as function return
    config_status = True

    # Set the task name, info and error text
    task_text = "RESTCONF copy file"

    # Print the task name
    print_task_name(text=task_name)

    # Run the Nornir Task rc_cisco_operation_rpc_task Cisco-IOS-XE-rpc:copy
    task = nr_obj.run(
        task=rc_cisco_operation_rpc_task,
        rpc="Cisco-IOS-XE-rpc:copy",
        payload={
            "Cisco-IOS-XE-rpc:input": {
                "source-drop-node-name": source,
                "destination-drop-node-name": destination,
            }
        },
        on_failed=True,
    )

    # Prepare the add_result list for printing
    add_result = [f"-> Source: '{source}'", f"-> Destination: '{destination}'"]

    # Print results for each host
    config_status = print_rc_cisco_rpc_result(
        task_text=task_text, task_result=task, add_result=add_result, verbose=verbose
    )

    return config_status


def rc_cisco_rpc_rollback_config(nr_obj, task_name, target_url, verbose=False):
    """
    This function runs the custom Nornir task rc_cisco_operation_rpc_task to rollback the copy of a Cisco
    device to a config specified by a target-url with RESTCONF. Its a Cisco specific RPC that is sent to the
    device. The result will be printed to std-out in custom Nornir style and the function return True or False
    depending wheather the task was successful.
    """
    # To verify the config status of each subtask and as function return
    config_status = True

    # Set the task name, info and error text
    task_text = "RESTCONF rollback config"

    # Print the task name
    print_task_name(text=task_name)

    # Run the Nornir Task rc_cisco_operation_rpc_task Cisco-IOS-XE-rpc:copy
    task = nr_obj.run(
        task=rc_cisco_operation_rpc_task,
        rpc="cisco-ia:rollback",
        payload={
            "cisco-ia:input": {
                "target-url": target_url,
                "verbose": True,
            }
        },
        on_failed=True,
    )

    # Prepare the add_result list for printing
    add_result = [f"-> Target-URL: '{target_url}'"]

    # Print results for each host
    config_status = print_rc_cisco_rpc_result(
        task_text=task_text, task_result=task, add_result=add_result, verbose=verbose
    )

    return config_status


def rc_software_install_one_shot(nr_obj, verbose=False):
    """
    This function takes the result of the function host_dict as an argument andruns the custom
    Nornir task rc_software_install_one_shot_task to start the one-shot installation process of the desired
    software version. The result will be printed to std-out in custom Nornir style and the script terminates
    with an info message in case of an error.
    """

    # Print the task name
    task_text = "RESTCONF one-shot install"
    print_task_name(task_text)

    # Run the custom Nornir task rc_software_install_one_shot_task
    task = nr_obj.run(task=rc_software_install_one_shot_task, on_failed=True)

    # Print results for each host
    install_status = print_rc_cisco_rpc_result(task_text=task_text, task_result=task, verbose=verbose)

    if not install_status:
        print("\n")
        print(task_error(text=task_text, changed=False))
        print("\U0001f4a5 ALERT: RESTCONF ONE-SHOT INSTALL FAILED! \U0001f4a5")
        print(
            f"\n{Style.BRIGHT}{Fore.RED}-> Analyse the Nornir output for failed task results\n"
            "-> May apply Nornir inventory changes and run the script again\n"
        )
        sys.exit(1)


def rc_install_remove_inactive(nr_obj, verbose=False):
    """
    This function runs the Nornir task rc_install_remove_inactive_task to to remove all not needed software
    packages and files on the filesystem with RESTCONF. The result will be printed to std-out in custom Nornir
    style and the script terminates with an info message in case of an error.
    """

    # Print the task name
    task_text = "RESTCONF install remove inactive"
    print_task_name(task_text)

    # Run the custom Nornir task rc_install_remove_inactive_task
    task = nr_obj.run(task=rc_install_remove_inactive_task, on_failed=True)

    # Print results for each host
    install_status = print_rc_cisco_rpc_result(task_text=task_text, task_result=task, verbose=verbose)

    if not install_status:
        print("\n")
        print(task_error(text=task_text, changed=False))
        print("\U0001f4a5 ALERT: RESTCONF INSTALL REMOVE INACTIVE FAILED! \U0001f4a5")
        print(
            f"\n{Style.BRIGHT}{Fore.RED}-> Analyse the Nornir output for failed task results\n"
            "-> May apply Nornir inventory changes and run the script again\n"
        )
        sys.exit()
