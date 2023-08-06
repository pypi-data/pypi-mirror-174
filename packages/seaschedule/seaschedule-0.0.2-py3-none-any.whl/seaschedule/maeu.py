import json
import pandas as pd
import requests

from datetime import datetime
from operator import itemgetter

RUN_TIME = datetime.now()
RUN_TIME_STR = RUN_TIME.strftime("%Y-%m-%dT%H:%M:%S")
INTERNAL_FACILITY_TERMINAL_GEOID = ["2ON3JDAEYWYES", "3UIO1T0SG68FO", "1NEO0LDYASVG4"]


def get_active_vessels(api_key: str) -> tuple:
    assert api_key, "The maeu_api_key is empty."

    endpoint = "https://api.maersk.com/schedules/active-vessels"
    request_headers = {'Consumer-Key': api_key, 'accept': 'application/stream+json'}
    vessel_cols = ["imo", "name"]
    vessel_data = pd.DataFrame()

    # TODO: Add certificates, verify=False, verify="www-maersk-com-chain.pem"
    res = requests.get(endpoint, headers=request_headers, verify=False)
    res_code = res.status_code
    res_text = res.text
    if res.ok:
        vessels= res_text.split("\n")
        for index, line in enumerate(vessels):
            # Skip the empty lines and vessels without IMO
            if line and 'vesselIMONumber' in line:
                vessel = json.loads(line)
                if vessel:
                    row_df = pd.DataFrame([[vessel.get("vesselIMONumber", ""), vessel.get("vesselName", "")]],
                                          columns=vessel_cols)
                    vessel_data = pd.concat([vessel_data, row_df], ignore_index=True)
    return vessel_data, res_code, res_text


def get_vessel_schedule(api_key: str, imo: str, carrier: str, start_date: str, date_range: str = "P12W") -> tuple:
    assert api_key, "The maeu_api_key is empty."

    endpoint = "https://api.maersk.com/schedules/vessel-schedules"
    request_headers = {'Consumer-Key': api_key, 'accept': 'application/stream+json'}
    url_params = {"vesselIMONumber": imo, "startDate": start_date, "dateRange": date_range, "carrierCodes": carrier}
    schedule_cols = ["carrierCode", "vesselFlagCode", "vesselIMONumber", "vesselName", "vesselCallOrder",
                   "estimatedDepartureTime", "actualDepartureTime", "estimatedArrivalTime", "actualArrivalTime", "facilityCode",
                   "facilityCityGeoID", "facilityTerminalCode", "facilityTerminalGeoID", "facilityCityName", "facilityCountryCode",
                   "facilityCountryName", "facilityLocationName", "facilityPortName", "serviceCode", "serviceName",
                   "inboundVoyageNumber", "voyageNumber"]
    # schedule_data = pd.DataFrame([], columns=schedule_cols)
    schedule_data = pd.DataFrame()

    # TODO: Add certificates
    res = requests.get(endpoint, headers=request_headers, params=url_params, verify=False)
    res_code = res.status_code
    res_text = res.text
    if res.ok:
        stops = []
        schedule = json.loads(res_text)
        # carrier
        carrierCode = carrier
        # vessel
        vessel = schedule["vessel"]
        # vesselCode = schedule["vessel"].get("carrierVesselCode", "")
        # vesselCallSign = vessel.get("vesselCallSign", "")
        vesselFlagCode = vessel.get("vesselFlagCode", "")
        vesselIMONumber = vessel.get("vesselIMONumber", "")
        vesselName = vessel.get("vesselName", "")
        # vesselCalls
        vesselCalls = schedule["vesselCalls"]
        for vesselCall in vesselCalls:
            vesselCallOrder = "TBD"
            # callSchedules
            callSchedules = vesselCall["callSchedules"]
            estimatedDepartureTime = ""
            actualDepartureTime = ""
            estimatedArrivalTime = ""
            actualArrivalTime = ""
            for callSchedule in callSchedules:
                # Parse ETD / ATD / ETA / ATA based on 'eventClassifierCode' and 'transportEventTypeCode'
                if callSchedule.get("eventClassifierCode", "") == "EST" and callSchedule.get("transportEventTypeCode",
                                                                                             "") == "DEPA":
                    estimatedDepartureTime = callSchedule.get("classifierDateTime", "")
                elif callSchedule.get("eventClassifierCode", "") == "EST" and callSchedule.get("transportEventTypeCode",
                                                                                               "") == "ARRI":
                    estimatedArrivalTime = callSchedule.get("classifierDateTime", "")
                elif callSchedule.get("eventClassifierCode", "") == "ACT" and callSchedule.get("transportEventTypeCode",
                                                                                               "") == "DEPT":
                    actualDepartureTime = callSchedule.get("classifierDateTime", "")
                elif callSchedule.get("eventClassifierCode", "") == "ACT" and callSchedule.get("transportEventTypeCode",
                                                                                               "") == "ARRI":
                    actualArrivalTime = callSchedule.get("classifierDateTime", "")
            # According to https://developer.maersk.com/api-catalogue/Vessel%20Schedules, this version of the API
            # classifies all events as EST Estimated and makes no distinction whether or not the event has been actualised.
            # Generally, if an event is reported for a past date, it is assumed to be actualised.
            # Therefore assume ATD/ATA equals to ETD/ETA if ETD/ETA is reported a past date.
            if (not actualDepartureTime) and estimatedDepartureTime and estimatedDepartureTime < RUN_TIME_STR:
                actualDepartureTime = estimatedDepartureTime
            if (not actualArrivalTime) and estimatedArrivalTime and estimatedArrivalTime < RUN_TIME_STR:
                actualArrivalTime = estimatedArrivalTime
            # facility
            facilityCode = vesselCall["facility"].get("UNLocationCode", "")
            facilityCityGeoID = vesselCall["facility"].get("carrierCityGeoID", "")
            facilityTerminalCode = vesselCall["facility"].get("carrierTerminalCode", "")
            facilityTerminalGeoID = vesselCall["facility"].get("carrierTerminalGeoID", "")
            facilityCityName = vesselCall["facility"].get("cityName", "")
            facilityCountryCode = vesselCall["facility"].get("countryCode", "")
            facilityCountryName = vesselCall["facility"].get("countryName", "")
            facilityLocationName = vesselCall["facility"].get("locationName", "")
            # facilityLocationType = vesselCall["facility"].get("locationType", "")
            facilityPortName = vesselCall["facility"].get("portName", "")
            # transport
            inboundServiceCode = vesselCall["transport"]["inboundService"].get("carrierServiceCode", "")
            inboundServiceName = vesselCall["transport"]["inboundService"].get("carrierServiceName", "")
            inboundVoyageNumber = vesselCall["transport"]["inboundService"].get("carrierVoyageNumber", "")
            # outboundServiceCode = vesselCall["transport"]["outboundService"].get("carrierServiceCode", "")
            # outboundServiceName = vesselCall["transport"]["outboundService"].get("carrierServiceName", "")
            outboundVoyageNumber = vesselCall["transport"]["outboundService"].get("carrierVoyageNumber", "")
            # Ignore Maersk internal locations (e.g., "Off Hire Site", "On Hire Site", "Repair Yard Site")
            if not (facilityTerminalGeoID in INTERNAL_FACILITY_TERMINAL_GEOID):
                stop = [carrierCode, vesselFlagCode, vesselIMONumber, vesselName,
                        vesselCallOrder, estimatedDepartureTime, actualDepartureTime, estimatedArrivalTime,
                        actualArrivalTime, facilityCode, facilityCityGeoID, facilityTerminalCode,
                        facilityTerminalGeoID, facilityCityName, facilityCountryCode, facilityCountryName,
                        facilityLocationName, facilityPortName, inboundServiceCode, inboundServiceName,
                        inboundVoyageNumber, inboundVoyageNumber]
                stops.append(stop)
                if inboundVoyageNumber != outboundVoyageNumber:
                    stop_ob_voyage = [carrierCode, vesselFlagCode, vesselIMONumber, vesselName,
                                      vesselCallOrder, estimatedDepartureTime, actualDepartureTime, estimatedArrivalTime,
                                      actualArrivalTime, facilityCode, facilityCityGeoID, facilityTerminalCode,
                                      facilityTerminalGeoID, facilityCityName, facilityCountryCode, facilityCountryName,
                                      facilityLocationName, facilityPortName, inboundServiceCode, inboundServiceName,
                                      inboundVoyageNumber, outboundVoyageNumber]
                    stops.append(stop_ob_voyage)

        # Sort by voyageNumber and estimatedDepartureTime
        stops.sort(key=itemgetter(21, 5))

        # Assign vesselCallOrder after sorting
        vessel_call_order = 0
        this_voyage = ""
        prev_voyage = ""
        for index, stop in enumerate(stops):
            this_voyage = stop[21]
            if this_voyage != prev_voyage:
                # Restart order for a new voyage
                vessel_call_order = 0
                prev_voyage = this_voyage
            else:
                vessel_call_order += 1
            # Assign vesselCallOrder
            stop[4] = str(vessel_call_order)

        # row_df = pd.DataFrame([["val1", "val2", "val3"]], columns=schedule_cols)
        # schedule_data = pd.concat([schedule_data, row_df], ignore_index=True)
        schedule_data = pd.DataFrame(stops, columns=schedule_cols)
    return schedule_data, res_code, res_text
