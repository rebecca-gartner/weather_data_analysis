# import relevant modules
import json
import requests
import logging
from requests.structures import CaseInsensitiveDict
import adal


class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def read_single_line(filename):
    with open(filename, "r") as file:
        lines = file.readlines()
        return lines[0][:-1] if lines[0][-1] == "\n" else lines[0]


TENANT_ID = read_single_line(".TENANT_ID")
CLIENT = read_single_line(".CLIENT")
KEY = read_single_line(".KEY")


authority_url = "https://login.microsoftonline.com/" + TENANT_ID
context = adal.AuthenticationContext(authority_url)
token = context.acquire_token_with_client_credentials(
    resource="1484212f-edce-452a-aae9-46141bae91af", client_id=CLIENT, client_secret=KEY
)


bearer = token["accessToken"]

logger = logging.getLogger(__name__)


class Train_Delay_Extraction:
    """sends  POST requests to RNV API for information on train delays at a particular train station
      and returns JSON

    -------------
    Parameter:
    - hafasID: hafasID of the train station
    - startTime: start time of the journey, format "YYYY-MM-DDTHH:MM:SSZ"
    - first_n: number of journeys that should be extracted. int

    """

    def __init__(
        self,
        hafasID: int,
        startTime: str,
        first_n: int,
    ) -> None:
        self.hafasID = hafasID
        self.startTime = startTime
        self.first_n = first_n

    def get_departure_times(self) -> json:

        query = (
            """query {"""
            + f"""station(id:\"{self.hafasID}\")"""
            + """ {
            hafasID
            longName
            journeys(startTime:"""
            + f""" \"{self.startTime}\" first: {self.first_n})"""
            + """ {
                    totalCount
                    elements {
                            ... on Journey {
                                
                                line {
                                    id
                                    }
                                stops {
                                    plannedDeparture {
                                        isoString
                                        }
                                        realtimeDeparture {
                                            isoString
                                            }
                                        }
                }
            }
        } 
        }
        }

        """
        )

        r = requests.post(
            "https://graphql-sandbox-dds.rnv-online.de",
            json={"query": query},
            auth=BearerAuth(bearer),
        )
        return r.json()
