"""
Credo API functions
"""
from typing import List

from credoai.utils import global_logger
from requests.exceptions import HTTPError

from .credo_api_client import CredoApiClient


class CredoApi:
    """
    CredoApi holds Credo API functions
    """

    def __init__(self, client: CredoApiClient = None):
        self._client = client

    def set_client(self, client: CredoApiClient):
        """
        Sets Credo Api Client

        Parameters
        ----------
        client : CredoApiClient
            Credo API client
        """
        self._client = client

    def get_assessment_plan_url(self, use_case_name: str, policy_pack_key: str = None):
        """
        Convert use_case_name and policy_pack_key to assessment_plan_url

        Parameters
        ----------
        use_case_name : str
            name of a use case
        policy_pack_key : str
            policy pack key, ie: FAIR
            If it is None, it gets the first resgisterd policy pack in use case

        Returns
        -------
        None
            When use_case_name does not exist or policy_pack_key is not registered to the use_case
        str
            assessment_plan_url

        Raises
        ------
        HTTPError
            When API request returns error other than 404
        """

        try:
            path = f"assessment_plan_url?use_case_name={use_case_name}"
            if policy_pack_key:
                path += f"&policy_pack_key={policy_pack_key}"
            response = self._client.get(path)
            return response["url"]
        except HTTPError as error:
            if policy_pack_key is not None:
                global_logger.info(
                    f"Use case ({use_case_name}) with policy pack ({policy_pack_key}) does not exist"
                )
            else:
                global_logger.info(
                    f"Cannot find assessment plan URL of use case {use_case_name}"
                )
            data = error.response.json()
            errors = data.get("errors", None)
            if errors:
                detail = errors[0]["detail"]
                if error:
                    global_logger.info(f"Error : {detail}")
                else:
                    raise error

                return None
            else:
                raise error

    def get_assessment_plan(self, url: str):
        """
        Get assessment plan from API server and returns it.

        Parameters
        ----------
        url : str
            assessment plan URL

        Returns
        -------
        dict
            evidence_requirements(list): list of evidence requirements
            policy_pack_id(str): policy pack id(key+version), ie: FAIR+1
            use_case_id(str): use case id

        Raises
        ------
        HTTPError
            When API request returns error
        """

        return self._client.get(url)

    def create_assessment(self, use_case_id: str, data: dict):
        """
        Upload evidences to API server.

        Parameters
        ----------
        use_case_id : str
            use case id
        data : dict
            assessment data generated by Governance

        Raises
        ------
        HTTPError
            When API request returns error
        """

        path = f"use_cases/{use_case_id}/assessments"
        return self._client.post(path, data)
