#!/usr/bin/env python3
"""
This module contains functions to prepare Cisco Support API data to generate reports.

The functions are ordered as followed:
- Prepare Cisco Support API data for Pandas Dataframe
- Prepare IBM TSS data for Pandas Dataframe
- Create Pandas Dataframe with report data
- Excel Report Generation
"""

import os
import json
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from xlsxwriter.utility import xl_col_to_name
from nornir_maze.utils import (
    print_task_name,
    task_info,
    get_pandas_column_width,
    construct_filename_with_current_date,
)


#### Prepare Cisco Support API data for Pandas Dataframe #####################################################


def prepare_report_data_host(serials_dict: dict) -> dict:
    """
    This function takes the serials_dict which has been filled with data by various functions and creates a
    host dict with the key "host" and a list of all hostnames as the value. The key will be the pandas
    dataframe column name and the value which is a list will be the colums cell content. The host dict will
    be returned.
    """
    # Define dict key for the hostnames
    host = {}
    host["host"] = []
    # Add all hostnames to the list
    for item in serials_dict.values():
        host["host"].append(item["host"])

    return host


def prepare_report_data_owner_coverage_by_serial_number(serials_dict: dict) -> dict:
    """
    This function takes the serials_dict which has been filled with data by various functions and creates a
    owner_coverage_status with key-value pairs. The key will be the pandas dataframe column name and the
    value which is a list will be the colums cell content. The host dict will be returned.
    """
    # pylint: disable=consider-using-dict-items

    # Define dict keys for SNIgetOwnerCoverageStatusBySerialNumbers
    owner_coverage_status = {}
    owner_coverage_status["sr_no_owner"] = []
    owner_coverage_status["coverage_end_date"] = []
    # Append the SNIgetOwnerCoverageStatusBySerialNumbers values for each defined dict key
    for header in owner_coverage_status:
        for sr_no in serials_dict.values():
            success = False
            for key, value in sr_no["SNIgetOwnerCoverageStatusBySerialNumbers"].items():
                if header == key:
                    if key in owner_coverage_status:
                        owner_coverage_status[key].append(value)
                        success = True
        # If nothing was appended to the owner_coverage_status dict, append an empty string
        if not success:
            owner_coverage_status[header].append("")

    return owner_coverage_status


def prepare_report_data_coverage_summary_by_serial_numbers(serials_dict: dict) -> dict:
    """
    This function takes the serials_dict which has been filled with data by various functions and creates a
    coverage_summary with key-value pairs. The key will be the pandas dataframe column name and the value
    which is a list will be the colums cell content. The host dict will be returned.
    """
    # pylint: disable=consider-using-dict-items

    # Define dict keys for SNIgetCoverageSummaryBySerialNumbers
    coverage_summary = {}
    coverage_summary["sr_no"] = []
    coverage_summary["is_covered"] = []
    coverage_summary["contract_site_customer_name"] = []
    coverage_summary["contract_site_address1"] = []
    coverage_summary["contract_site_city"] = []
    coverage_summary["contract_site_state_province"] = []
    coverage_summary["contract_site_country"] = []
    coverage_summary["covered_product_line_end_date"] = []
    coverage_summary["service_contract_number"] = []
    coverage_summary["service_line_descr"] = []
    coverage_summary["warranty_end_date"] = []
    coverage_summary["warranty_type"] = []
    coverage_summary["warranty_type_description"] = []
    coverage_summary["item_description"] = []
    coverage_summary["item_type"] = []
    coverage_summary["orderable_pid"] = []
    # Append the SNIgetCoverageSummaryBySerialNumbers values for each defined dict key
    for header in coverage_summary:
        for sr_no in serials_dict.values():
            success = False
            # Append all general coverage details
            for key, value in sr_no["SNIgetCoverageSummaryBySerialNumbers"].items():
                if header == key:
                    if key in coverage_summary:
                        coverage_summary[key].append(value)
                        success = True
            # Append all the orderable pid details
            for key, value in sr_no["SNIgetCoverageSummaryBySerialNumbers"]["orderable_pid_list"][0].items():
                if header == key:
                    if key in coverage_summary:
                        coverage_summary[key].append(value)
                        success = True
            # If nothing was appended to the coverage_summary dict, append an empty string
            if not success:
                coverage_summary[header].append("")

    return coverage_summary


def prepare_report_data_eox_by_serial_numbers(serials_dict: dict) -> dict:
    """
    This function takes the serials_dict which has been filled with data by various functions and creates a
    end_of_life with key-value pairs. The key will be the pandas dataframe column name and the value which is
    a list will be the colums cell content. The host dict will be returned.
    """
    # pylint: disable=too-many-nested-blocks,consider-using-dict-items

    # Define dict keys for EOXgetBySerialNumbers
    end_of_life = {}
    end_of_life["EOXExternalAnnouncementDate"] = []
    end_of_life["EndOfSaleDate"] = []
    end_of_life["EndOfSWMaintenanceReleases"] = []
    end_of_life["EndOfSecurityVulSupportDate"] = []
    end_of_life["EndOfRoutineFailureAnalysisDate"] = []
    end_of_life["EndOfServiceContractRenewal"] = []
    end_of_life["LastDateOfSupport"] = []
    end_of_life["EndOfSvcAttachDate"] = []
    end_of_life["UpdatedTimeStamp"] = []
    end_of_life["MigrationInformation"] = []
    end_of_life["MigrationProductId"] = []
    end_of_life["MigrationProductName"] = []
    end_of_life["MigrationStrategy"] = []
    end_of_life["MigrationProductInfoURL"] = []
    end_of_life["ErrorDescription"] = []
    end_of_life["ErrorDataType"] = []
    end_of_life["ErrorDataValue"] = []

    # Append the EOXgetBySerialNumbers values for each defined dict key
    for header in end_of_life:
        for sr_no in serials_dict.values():
            success = False

            # Append all end of life dates
            for key, value in sr_no["EOXgetBySerialNumbers"].items():
                if header == key:
                    if isinstance(value, dict):
                        if "value" in value:
                            end_of_life[key].append(value["value"])
                            success = True
            # Append all migration details
            for key, value in sr_no["EOXgetBySerialNumbers"]["EOXMigrationDetails"].items():
                if header == key:
                    if key in end_of_life:
                        end_of_life[key].append(value)
                        success = True
            # If EOXError exists append the error reason, else append an empty string
            if "EOXError" in sr_no["EOXgetBySerialNumbers"]:
                for key, value in sr_no["EOXgetBySerialNumbers"]["EOXError"].items():
                    if header == key:
                        if key in end_of_life:
                            end_of_life[key].append(value)
                            success = True

            # If nothing was appended to the end_of_life dict, append an empty string
            if not success:
                end_of_life[header].append("")

    return end_of_life


def prepare_report_data_act_needed(serials_dict: dict) -> dict:
    """
    This function takes the serials_dict an argument and creates a dictionary named act_needed will be
    returned which contains the key value pairs "coverage_action_needed" and "api_action_needed" to create a
    Pandas dataframe later.
    """
    # Define the coverage_action_needed dict and its key value pairs to return as the end of the function
    act_needed = {}
    act_needed["coverage_action_needed"] = []
    act_needed["api_action_needed"] = []

    for records in serials_dict.values():
        # Verify if the user has the correct access rights to access the serial API data
        if "YES" in records["SNIgetOwnerCoverageStatusBySerialNumbers"]["sr_no_owner"]:
            act_needed["api_action_needed"].append(
                "No action needed (API user is associated with contract and device)"
            )
        else:
            act_needed["api_action_needed"].append(
                "Action needed (No associattion between api user, contract and device)"
            )

        # Verify if the serial is covered by Cisco add the coverage_action_needed variable to tss_info
        if "YES" in records["SNIgetCoverageSummaryBySerialNumbers"]["is_covered"]:
            act_needed["coverage_action_needed"].append(
                "No action needed (Device is covered by a maintenance contract)"
            )
        else:
            act_needed["coverage_action_needed"].append(
                "Action needed (Device is not covered by a maintenance contract)"
            )

    return act_needed


#### Prepare IBM TSS data for Pandas Dataframe ###############################################################


def prepare_report_data_tss(serials_dict: dict, df_order: list[str], file: str) -> dict:
    """
    This function takes the serials_dict and a source file which is the IBM TSS report as arguments. The only
    mandatory column is the "Serials" which will be normalized to tss_serial. All other columns can be
    specified with their order and the prefix "tss_" in the EXCEL_COLUMN_ORDER_WITH_TSS constant. A dictionary
    named tss_info will be returned which contains the key value pairs "coverage_action_needed",
    "api_action_needed" and all TSS data to create a Pandas dataframe later.
    """
    # pylint: disable=invalid-name,too-many-branches

    # Define the tss_info dict and its key value pairs to return as the end of the function
    tss_info = {}
    tss_info["coverage_action_needed"] = []
    tss_info["api_action_needed"] = []
    for column in df_order:
        if column.startswith("tss_"):
            tss_info[column] = []

    # Read the excel file into a pandas dataframe -> Row 0 is the title row
    df = pd.read_excel(rf"{file}")

    # Make some data normalization of the TSS report file column headers
    # Make column written in lowercase letters
    df.columns = df.columns.str.lower()
    # Replace column name whitespace with underscore
    df.columns = df.columns.str.replace(" ", "_")
    # Add a prefix to the column name to identify the TSS report columns
    df = df.add_prefix("tss_")

    # Make all serial numbers written in uppercase letters
    df.tss_serial = df.tss_serial.str.upper()

    # The first fillna will replace all of (None, NAT, np.nan, etc) with Numpy's NaN, then replace
    # Numpy's NaN with python's None
    df = df.fillna(np.nan).replace([np.nan], [None])

    # Delete all rows which have not the value "Cisco" in the OEM column
    df = df[df.tss_oem == "Cisco"]

    # Create a list with all IBM TSS serial numbers
    tss_serial_list = df["tss_serial"].tolist()

    # Look for inventory serials which are covered by IBM TSS and add them to the serial_dict
    # It's important to match IBM TSS serials to inventory serials first for the correct order
    for sr_no, records in serials_dict.items():
        records["tss_info"] = {}

        # Covered by IBM TSS if inventory serial number is in all IBM TSS serial numbers
        if sr_no in tss_serial_list:
            # Verify if the user has the correct access rights to access the serial API data
            if "YES" in records["SNIgetOwnerCoverageStatusBySerialNumbers"]["sr_no_owner"]:
                tss_info["api_action_needed"].append(
                    "No action needed (API user is associated with contract and device)"
                )
            else:
                tss_info["api_action_needed"].append(
                    "Action needed (No associattion between api user, contract and device)"
                )

            # Verify if the inventory serial is covered by IBM TSS and is also covered by Cisco
            # Verify if the serial is covered by Cisco add the coverage_action_needed variable to tss_info
            if "YES" in records["SNIgetCoverageSummaryBySerialNumbers"]["is_covered"]:
                tss_info["coverage_action_needed"].append("No action needed (Covered by IBM TSS and Cisco)")
            else:
                tss_info["coverage_action_needed"].append(
                    "Action needed (Covered by IBM TSS, but Cisco coverage missing)"
                )

            # Get the index of the list item and assign the element from the TSS dataframe by its index
            index = tss_serial_list.index(sr_no)
            # Add the data from the TSS dataframe to tss_info
            for column, value in tss_info.items():
                if column.startswith("tss_"):
                    value.append(df[column].values[index])

        # Inventory serial number is not in all IBM TSS serial numbers
        else:
            # Verify if the user has the correct access rights to access the serial API data
            if "YES" in records["SNIgetOwnerCoverageStatusBySerialNumbers"]["sr_no_owner"]:
                tss_info["api_action_needed"].append(
                    "No action needed (API user is associated with contract and device)"
                )
            else:
                tss_info["api_action_needed"].append(
                    "Action needed (No associattion between api user, contract and device)"
                )

            # Verify if the inventory serial is covered by Cisco
            # Add the coverage_action_needed variable to tss_info
            if "YES" in records["SNIgetCoverageSummaryBySerialNumbers"]["is_covered"]:
                tss_info["coverage_action_needed"].append("No action needed (Covered by Cisco SmartNet)")
            else:
                tss_info["coverage_action_needed"].append(
                    "Action needed (Cisco SmartNet or IBM TSS coverage missing)"
                )

            # Add the empty strings for all additional IBM TSS serials to tss_info
            for column, value in tss_info.items():
                if column.startswith("tss_"):
                    value.append("")

    # After the inventory serials have been processed
    # Add IBM TSS serials to tss_info which are not part of the inventory serials
    for tss_serial in tss_serial_list:
        if tss_serial not in serials_dict.keys():
            # Add the coverage_action_needed variable to tss_info
            tss_info["coverage_action_needed"].append(
                "Action needed (Remove serial from IBM TSS inventory as device is decommissioned)"
            )
            tss_info["api_action_needed"].append("No Cisco API data as serial is not part of column sr_no")

            # Get the index of the list item and assign the element from the TSS dataframe by its index
            index = tss_serial_list.index(tss_serial)
            # Add the data from the TSS dataframe to tss_info
            for column, value in tss_info.items():
                if column.startswith("tss_"):
                    value.append(df[column].values[index])

    return tss_info


#### Create Pandas Dataframe with report data ################################################################


def create_pandas_dataframe_for_report(
    serials_dict: dict,
    df_order: list[str],
    df_date_columns: list[str],
    tss_report: bool = False,
    verbose: bool = False,
) -> pd.DataFrame:
    """
    Prepare the report data and create a pandas dataframe. The pandas dataframe will be returned
    """
    # pylint: disable=invalid-name

    print_task_name(text="PYTHON prepare report data")

    # Create an empty dict and append the previous dicts to create later the pandas dataframe
    report_data = {}

    # Prepare the needed data for the report from the serials dict. The serials dict contains all data
    # that the Cisco support API sent. These functions return a dictionary with the needed data only
    host = prepare_report_data_host(serials_dict=serials_dict)
    owner_coverage_status = prepare_report_data_owner_coverage_by_serial_number(serials_dict=serials_dict)
    coverage_summary = prepare_report_data_coverage_summary_by_serial_numbers(serials_dict=serials_dict)
    end_of_life = prepare_report_data_eox_by_serial_numbers(serials_dict=serials_dict)

    if tss_report:
        # Analyze the IBM TSS report file and create the tss_info dict
        tss_info = prepare_report_data_tss(serials_dict=serials_dict, df_order=df_order, file=tss_report)

        # The tss_info dict may have more list elements as TSS serials have been found which are not inside
        # the customer inventory -> Add the differente to all other lists as empty strings
        for _ in range(len(tss_info["tss_serial"]) - len(host["host"])):
            for column in host.values():
                column.append("")
            for column in owner_coverage_status.values():
                column.append("")
            for column in coverage_summary.values():
                column.append("")
            for column in end_of_life.values():
                column.append("")

        # Update the report_data dict with all prepared data dicts
        report_data.update(**host, **owner_coverage_status, **coverage_summary, **end_of_life, **tss_info)
    else:
        # Analyze if actions are needed for serial number or user
        act_needed = prepare_report_data_act_needed(serials_dict=serials_dict)

        # Update the report_data dict with all prepared data dicts
        report_data.update(**host, **owner_coverage_status, **coverage_summary, **end_of_life, **act_needed)

    print(task_info(text="PYTHON prepare report data dict", changed=False))
    print("'PYTHON prepare report data dict' -> PythonResult <Success: True>")
    if verbose:
        print("\n" + json.dumps(report_data, indent=4))

    # Reorder the data dict according to the key_order list -> This needs Python >= 3.6
    report_data = {key: report_data[key] for key in df_order}

    print(task_info(text="PYTHON order report data dict", changed=False))
    print("'PYTHON order report data dict' -> PythonResult <Success: True>")
    if verbose:
        print("\n" + json.dumps(report_data, indent=4))

    # Create a Pandas dataframe for the data dict
    df = pd.DataFrame(report_data)

    # Format each column in the list to a pandas date type for later conditional formatting
    for column in df_date_columns:
        df[column] = pd.to_datetime(df[column], format="%Y-%m-%d")

    print(task_info(text="PYTHON create pandas dataframe from dict", changed=False))
    print("'PANDAS create dataframe' -> PandasResult <Success: True>")
    if verbose:
        print(df)

    return df


#### Excel Report Generation #################################################################################


def generate_cisco_maintenance_report(
    report_vars: dict, report_file: str, df: pd.DataFrame, tss_report: bool = False
) -> None:
    """
    Generate the Cisco Maintenance report Excel file specified by the report_file with the pandas dataframe.
    The function returns None, but saves the Excel file to the local disk.
    """
    # pylint: disable=invalid-name,too-many-locals

    print_task_name(text="PYTHON process report data")

    #### Set the report file path and name with the current date #############################################

    # Construct the new destination path and filename from the report_file string variable
    report_file = construct_filename_with_current_date(
        filename=report_file,
        name="PYTHON construct destination file",
        silent=False,
    )

    #### Create the xlsx writer, workbook and worksheet objects ##############################################

    # Create a Pandas excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(  # pylint: disable=abstract-class-instantiated
        report_file, engine="xlsxwriter", date_format="yyyy-mm-dd", datetime_format="yyyy-mm-dd"
    )

    # Write the dataframe data to XlsxWriter. Turn off the default header and index and skip one row to allow
    # us to insert a user defined header.
    df.to_excel(writer, sheet_name="Cisco_Maintenance_Report", startrow=2, header=False, index=False)

    # Get the xlsxwriter workbook and worksheet objects.
    workbook = writer.book
    worksheet = writer.sheets["Cisco_Maintenance_Report"]

    # Setting for the whole worksheet
    worksheet.set_zoom(110)
    worksheet.freeze_panes(2, 3)

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape
    # Max_row + 2 because the first two rows are used for title and header
    max_row = max_row + 2
    # Max_com -1 otherwise would be one column to much
    max_col = max_col - 1

    print(task_info(text="PYTHON create pandas writer object using XlsxWriter engine", changed=False))
    print("'PYTHON create pandas writer object using XlsxWriter engine' -> PythonResult <Success: True>")

    #### Create the top title row ############################################################################

    # Set the top row height
    worksheet.set_row(0, report_vars["title_row_height"])
    # Create a format to use for the merged top row
    title_format = workbook.add_format(
        {
            "font_name": report_vars["title_font_name"],
            "font_size": report_vars["title_font_size"],
            "font_color": report_vars["title_font_color"],
            "align": "left",
            "valign": "vcenter",
            "bold": 1,
            "bottom": 1,
            "bg_color": report_vars["title_background_color"],
        }
    )
    # Merge the first three cells in the top row to insert a logo
    worksheet.merge_range(0, 0, 0, 2, None, title_format)
    # Insert a logo to the top row
    worksheet.insert_image(
        "A1",
        report_vars["title_logo"],
        {
            "x_scale": report_vars["title_logo_x_scale"],
            "y_scale": report_vars["title_logo_y_scale"],
            "x_offset": report_vars["title_logo_x_offset"],
            "y_offset": report_vars["title_logo_y_offset"],
        },
    )
    # Merge from the cell 4 to the max_col and write a title
    if tss_report:
        title_text = f"{report_vars['title_text_with_tss']} (generated by {os.path.basename(__file__)})"
    else:
        title_text = f"{report_vars['title_text']} (generated by {os.path.basename(__file__)})"
    worksheet.merge_range(0, 3, 0, max_col, title_text, title_format)

    print(task_info(text="PYTHON create XlsxWriter title row", changed=False))
    print("'PYTHON create XlsxWriter title row' -> PythonResult <Success: True>")

    ### Create a Excel table structure and add the Pandas dataframe

    # Create a list of column headers, to use in add_table().
    column_settings = [{"header": column} for column in df.columns]

    # Add the Excel table structure. Pandas will add the data.
    # fmt: off
    worksheet.add_table(1, 0, max_row - 1, max_col,
        {
            "columns": column_settings,
            "style": report_vars["excel_table_style"],
        },
    )
    # fmt: on

    table_format = workbook.add_format(
        {
            "font_name": report_vars["table_font_name"],
            "font_size": report_vars["table_font_size"],
            "align": "left",
            "valign": "vcenter",
        }
    )
    # Auto-adjust each column width -> +5 on the width makes space for the filter icon
    for index, width in enumerate(get_pandas_column_width(df)):
        worksheet.set_column(index, index - 1, width + 5, table_format)

    print(task_info(text="PYTHON create XlsxWriter table and add pandas dataframe", changed=False))
    print("'PYTHON create XlsxWriter table and add pandas dataframe' -> PythonResult <Success: True>")

    #### Create conditional formating ########################################################################

    # Create a red background format for the conditional formatting
    red_format = workbook.add_format({"bg_color": "#C0504D"})
    # Create a orange background format for the conditional formatting
    orange_format = workbook.add_format({"bg_color": "#F79646"})
    # Create a green background format for the conditional formatting
    green_format = workbook.add_format({"bg_color": "#9BBB59"})

    # Create a conditional formatting for each column in the list.
    column_list = ["sr_no_owner", "is_covered", "coverage_action_needed", "api_action_needed"]
    for column in column_list:
        # Get the column letter by the column name
        target_col = xl_col_to_name(df.columns.get_loc(column))
        # -> Excel requires the value for type cell to be double quoted
        worksheet.conditional_format(
            f"{target_col}3:{target_col}{max_row}",
            {"type": "cell", "criteria": "equal to", "value": '"NO"', "format": red_format},
        )
        worksheet.conditional_format(
            f"{target_col}3:{target_col}{max_row}",
            {"type": "cell", "criteria": "equal to", "value": '"YES"', "format": green_format},
        )
        worksheet.conditional_format(
            f"{target_col}3:{target_col}{max_row}",
            {"type": "text", "criteria": "containing", "value": "No action needed", "format": green_format},
        )
        worksheet.conditional_format(
            f"{target_col}3:{target_col}{max_row}",
            {"type": "text", "criteria": "containing", "value": "Action needed", "format": red_format},
        )

    # Create a conditional formatting for each column with a date. Get the column letter by the column name
    for column in report_vars["date_column_list"]:
        target_col = xl_col_to_name(df.columns.get_loc(column))
        worksheet.conditional_format(
            f"{target_col}3:{target_col}{max_row}",
            {
                "type": "date",
                "criteria": "between",
                "minimum": report_vars["date_today"] + timedelta(days=report_vars["date_grace_period"]),
                "maximum": datetime.strptime("2999-01-01", "%Y-%m-%d"),
                "format": green_format,
            },
        )
        worksheet.conditional_format(
            f"{target_col}3:{target_col}{max_row}",
            {
                "type": "date",
                "criteria": "between",
                "minimum": report_vars["date_today"],
                "maximum": report_vars["date_today"] + timedelta(days=report_vars["date_grace_period"]),
                "format": orange_format,
            },
        )
        worksheet.conditional_format(
            f"{target_col}3:{target_col}{max_row}",
            {
                "type": "date",
                "criteria": "between",
                "minimum": datetime.strptime("1999-01-01", "%Y-%m-%d"),
                "maximum": report_vars["date_today"] - timedelta(days=1),
                "format": red_format,
            },
        )

    print(task_info(text="PYTHON create XlsxWriter conditional formating", changed=False))
    print("'PYTHON create XlsxWriter conditional formating' -> PythonResult <Success: True>")

    #### Save the Excel report file to disk ##################################################################

    print_task_name(text="PYTHON generate report Excel file")

    # Close the Pandas Excel writer and output the Excel file.
    writer.close()

    print(task_info(text="PYTHON generate report Excel file", changed=False))
    print("'PYTHON generate report Excel file' -> PythonResult <Success: True>")
    print(f"\n-> Saved information about {df.shape[0]} serials to {report_file}")
