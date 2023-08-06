import logging
from typing import List, Union

import requests

from . import models
from .auth import LGAuth

logger = logging.getLogger(__name__)


def list_to_comma_str(data_list: List[int]) -> str:
    """Convert list to a comma separated string.

    Args:
        data_list: list of elements

    Returns:
        String converted list.
        Example ['a','b','c',1,2] -> 'a,b,c,1,2'.
    """
    if data_list:
        ret_ = ",".join(map(str, data_list))
    else:
        ret_ = data_list
    return ret_


class LGApi:
    """Cimcon Lightning Gale (LG) API Interface.

    Few scenarios where LG APIs may be used:

    - Retrieving all the inventory information.
    - Managing SLC inventory basic operations including adding, editing, and
        deleting the SLCs.
    - Fetching latest data of fixture.
    - Setting multiple modes to the fixture.
    - Tracking the status of the commands sent.
    - Managing the schedules for the lamps turning on/off/dim at the user
        preferred time.

    Attributes:
        ssl_verifiy: SSL Certificate Verification.
            Defaults to lg_auth.ssl_verify but can be changed.

    Args:
        lg_auth: LG Auth data (session)
    """

    def __init__(self, lg_auth: LGAuth) -> None:
        self.__lg_auth = lg_auth
        self.__access_token: str = lg_auth.get_auth_token()
        self.__ssl_verify: bool = lg_auth.ssl_verify

    @property
    def ssl_verify(self) -> bool:
        return self.__ssl_verify

    @ssl_verify.setter
    def ssl_verify(self, value: bool) -> None:
        self.__ssl_verify = value

    def headers(self, pageno: int = 1, pagesize: int = 50, **extra_headers):
        """Generate default Auth headers, pageno and pagesize params

        Args:
            pageno: Page number that is needed from the result data.
            pagesize: Page size that you want to specify for the result data.
            **extra_headers: add extra kwarg headers
        """
        return {
            'Authorization': f'Bearer {self.__access_token}',
            'pageno': str(pageno),
            'pagesize': str(pagesize),
            **extra_headers
        }

    def _request(self, *args, **kwargs) -> dict:
        """This method is a wrapper for requests

        Make HTTP request

        Args:
            Use args and kwargs to requests(args, kwargs)

        Returns:
            HTTP Response data as dict or raise errors

        Raises:
            HTTP errors.
        """
        if 'verify' not in kwargs:
            kwargs.update({'verify': self.__ssl_verify})
        response = requests.request(*args, **kwargs)
        # # Debug point
        # from pprint import pprint
        # a = 1
        # pprint(response.json())
        # # import pdb; pdb.set_trace()
        # #
        response.raise_for_status()
        return response.json()

    def get_all_slcs(self, pageno: int = 1,
                     pagesize: int = 50) -> models.SLCResponse:
        """Get All SLCs (Zigbee and Cisco)

        Args:
            pageno: Page number that is needed from the result data.
            pagesize: Page size that you want to specify for the result data.

        Returns:
            SLC.

        Raises:
            HTTP Errors.
        """
        url = self.__lg_auth.base_url + '/SLCs/GetAllSLCs'
        headers = self.headers(pageno, pagesize)
        data = self._request('get', url, headers=headers)
        return models.SLCResponse(**data)

    def get_all_slc_data(self, slc_id: Union[List[int], None] = None,
                         pageno: int = 1,
                         pagesize: int = 50) -> models.SLCDataResponse:
        """

        Args:
            slc_id: SLCId will be optional , user can add comma seprated SLCs.
            pageno: Page number that is needed from the result data.
            pagesize: Page size that you want to specify for the result data.

        Returns:
            SLC data.

        Raises:
            HTTP Errors.
        """
        url = self.__lg_auth.base_url + '/SLCs/GetAllSLCData'
        headers = self.headers(
            pageno, pagesize, sLCId=list_to_comma_str(slc_id)
        )
        data = self._request('get', url, headers=headers)
        return models.SLCDataResponse(**data)

    def get_all_gateway_list(self,
                             pageno: int = 1,
                             pagesize: int = 50) -> models.GatewayResponse:
        url = self.__lg_auth.base_url + '/Gateways/GetAllGatewayList'
        headers = self.headers(pageno, pagesize)
        data = self._request('get', url, headers=headers)
        return models.GatewayResponse(**data)

    def get_slc_by_dcuid(self, gateway_id: int,
                         pageno: int = 1,
                         pagesize: int = 50) -> models.SLCResponse:
        """Get All SLCs by GatewayID (Zigbee)

        Args:
            gateway_id: Gateway ID
            pageno: Page number that is needed from the result data.
            pagesize: Page size that you want to specify for the result data.

        Returns:
            SLC.

        Raises:
            HTTP errors.
        """
        url = self.__lg_auth.base_url + '/SLCs/GetSLCByDCUID'
        headers = self.headers(
            pageno, pagesize,
            GatewayId=str(gateway_id)
        )
        data = self._request('get', url, headers=headers)
        return models.SLCResponse(**data)

    def switch_on_off_slc(self, turn_on: bool,
                          slc_id_list: List[int]) -> models.CommandResponse:
        """Switch On/Off SLC (Zigbee and Cisco)

        Args:
            turn_on: True for ON, False for OFF

        Returns:
            Switch response.

        Raises:
            HTTP errors.
        """
        url = self.__lg_auth.base_url + '/Commands/SwitchONOFFSLC'
        if isinstance(turn_on, bool) and turn_on is True:
            command = 'ON'
        elif isinstance(turn_on, bool) and turn_on is False:
            command = 'OFF'
        else:
            raise ValueError(f'Invalid type: {type(turn_on)}')
        headers = self.headers()  # headers docs do not use: pageno pagesize
        data = {
            "SwitchONOFF": [
                {
                    "SLCIdList": list_to_comma_str(slc_id_list),
                    "Command": command
                }
            ]
        }
        data = self._request('post', url, headers=headers, json=data)
        return models.CommandResponse(**data)

    def get_latitude_longitude_slc(self, slc_id_list: List[int]) -> dict:
        """Get Latitude Longitude SLC (Zigbee and Cisco).

        Get SLC coordinates by id.

        WARNING: The endpoint URL is not working. 404 returned.

        Args:
            slc_id_list: Pass multiple SLCs separated by comma.
                Example: [33, 34]

        Returns:
            Coordinates data.

        Raises:
            HTTP 404 always.
        """
        logger.warning('WARNING: Vendor LG API Endpoint is current not working')
        url = self.__lg_auth.base_url + '/Commands/GetLatitudeLongitudeCommand'
        headers = {
            'Authorization': f'Bearer {self.__access_token}',
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        data = {
            "GetLatitudeLongitudeCommand": [
                {"SLCIdList": list_to_comma_str(slc_id_list)}
            ]
        }
        data = self._request('post', url, headers=headers, json=data)
        return data

    def dim_slcs(self, slc_id_list: List[int],
                 value: Union[int, str]) -> models.CommandResponse:
        """Set Dimming on SLC (Zigbee and Cisco).

        To Dim SLCs manually, the SLC must be in Manual Mode and lamp status
        should be ON.

        Args:
            slc_id_list: Pass multiple SLCs separated by comma.
            value: must represent a intenger 0-100 to set dimmer.

        Raises:
            HTTP Errors. 400 Bad request
            DIMValue must be an integer value between 0 and 100.
            SLCIdList must be unique and should not contain a zero value.
            SLCs must be assigned to the client.
            Invalid JSON entered.
        """
        url = self.__lg_auth.base_url + '/Commands/DIMSLCs'
        if isinstance(value, int):
            _val = str(value)
        if isinstance(value, str):
            int(value)
            _val = value
        headers = self.headers()
        data = {
            "DIMSLC": [
                {
                    "SLCIdList": list_to_comma_str(slc_id_list),
                    "DIMValue": _val
                }
            ]
        }
        response = self._request('post', url, headers=headers, json=data)
        return models.CommandResponse(**response)

    # No related directly with API endpoint
    def get_all_slc(self, slc_id: Union[List[int], None] = None,
                    pageno: int = 1,
                    pagesize: int = 50) -> List[models.SLCInfo]:
        """Obtain all SLC.

        NOTE: This method is not related directy with any endpoint.
        Join to different endpoint data for: 1. SLC and 2. SLCData.
        This method make at least 2 requests

        Args:
            slc_id: List of integers
            pageno: Page number that is needed from the result data.
            pagesize: Page size that you want to specify for the result data.

        Returns:
            List of SLCInfo joined by related ID

        Raises:
            HTTP Errors.
        """
        # request step
        slc_data_response = self.get_all_slc_data(
            slc_id=slc_id, pageno=pageno, pagesize=pagesize
        )
        slc_response = self.get_all_slcs(
            pageno=pageno, pagesize=pagesize
        )
        # Obtaining lists
        slc_list = slc_response.data.all_slcs_list  # slc_number
        slc_data_list = slc_data_response.data.slc_data_list  # slcNo
        # Generate new list of ID to make relationship
        slc_data_id_list = [slc_data.slc_no for slc_data in slc_data_list]
        # Find, relate and instantiate SLCInfo
        slc_info_list = []
        for slc in slc_list:
            index = slc_data_id_list.index(slc.slc_number)
            slc_data = slc_data_list[index]
            slc_info = models.SLCInfo(
                **{
                    **slc.dict(by_alias=True),
                    **slc_data.dict(by_alias=True)
                }
            )
            slc_info_list.append(slc_info)
        return slc_info_list
