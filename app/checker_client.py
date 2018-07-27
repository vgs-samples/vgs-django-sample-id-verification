from datetime import datetime
from time import sleep

import requests


class CheckerServiceException(Exception):
    def __init__(self, status_code, error):
        self.status_code = status_code
        self.error = error


class CheckerClientException(Exception):
    def __init__(self, error):
        self.error = error


class CheckerClient:
    report_gen_timeout = 10000

    def __init__(self, host, api_key):
        self.host = host
        self.api_key = api_key

    def create_candidate(self,
                         ssn,
                         dln,
                         geo_id
                         ):
        candidate_data = {
            'first_name': "testName",
            'no_middle_name': True,
            'last_name': "TestLastName",
            'email': "test.email@vgs.io",
            'phone': "5555555555",
            'zipcode': "85001",
            'dob': "1970-01-22",
            'ssn': ssn,
            'driver_license_number': dln,
            'driver_license_state': "CA",
            "geo_ids": [geo_id]
        }

        r = requests.post(
            self.host + '/v1/candidates',
            json=candidate_data,
            auth=(self.api_key, ''),
        )

        if r.status_code != 201:
            raise CheckerServiceException(r.status_code, r.json()['error'])

        return r.json()['id']

    def create_report(self, candidate_id):
        candidate_data = {
            'package': "driver_standard",
            'candidate_id': candidate_id
        }

        r = requests.post(
            self.host + '/v1/reports',
            json=candidate_data,
            auth=(self.api_key, '')
        )

        if r.status_code != 201:
            raise CheckerServiceException(r.status_code, r.json()['error'])

        return r.json()['id']

    def get_geos(self):
        r = requests.get(
            self.host + '/v1/geos',
            auth=(self.api_key, '')
        )

        if r.status_code != 200:
            raise CheckerServiceException(r.status_code, r.json()['error'])

        return r.json()['data']

    def create_geo(self, name, city, state):
        candidate_data = {
            'name': name,
            'city': city,
            'state': state
        }

        r = requests.post(
            self.host + '/v1/geos',
            json=candidate_data,
            auth=(self.api_key, '')
        )

        if r.status_code != 201:
            raise CheckerServiceException(r.status_code, r.json()['error'])

        return r.json()['id']

    def retrieve_report(self, report_id):
        return self.__retrieve_report(report_id, self.report_gen_timeout)

    def __retrieve_report(self, report_id, timeout_sec):
        if timeout_sec < 0:
            raise TimeoutError("Requested report were not generated in time")

        start = datetime.now()
        r = requests.get(
            self.host + '/v1/reports/' + report_id,
            auth=(self.api_key, '')
        )

        if r.status_code != 200:
            raise CheckerServiceException(r.status_code, r.json()['error'])

        if r.json()["status"] == "pending":
            sleep(1)
            spending_time = datetime.now() - start
            spending_time_microsec = spending_time.seconds + 1000 + spending_time.microseconds / 1000
            remaining_timeout = timeout_sec - spending_time_microsec
            return self.__retrieve_report(report_id, remaining_timeout)

        if r.json()["status"] in ["clear", "consider"]:
            return r.json()

        raise CheckerClientException("Could not generate report")
