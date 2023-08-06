import requests
import json
import time
import subprocess as sub
import platform as plat


"""
Very bad WX alert scanner system thing.
Scans a state every 30 seconds for weather alerts.
"""


def clear(shell=True):
    if plat.system().lower() == "windows":
        sub.call("cls", shell=shell)
    else:
        sub.call("clear", shell=shell)


class Scan:
    def __init__(self, state):
        self.state = state

        self.main()

    def main(self):
        clear()

        url = "https://api.weather.gov/alerts/active"

        q = {"area": self.state}

        resp = requests.get(url, params=q)
        d = resp.content
        data = json.loads(d)

        title = data["title"]
        print(title)

        try:
            if not data["features"][0]["id"]:
                pass
        except IndexError:
            print("\nNo watches, warning, or advisories")
        finally:

            for each in data["features"]:
                id_url = each["id"]

                id_resp = requests.get(id_url)
                id_d = id_resp.content
                id_data = json.loads(id_d)

                VTEC = "VTEC was not giving by the API"

                try:
                    event = id_data["properties"]["event"]
                    area = id_data["properties"]["areaDesc"]
                    ends = id_data["properties"]["ends"]
                    status = id_data["properties"]["status"]
                    response = id_data["properties"]["response"]
                    headline = id_data["properties"]["headline"]
                    urgency = id_data["properties"]["urgency"]
                    severity = id_data["properties"]["severity"]
                    description = id_data["properties"]["description"]
                    instruction = id_data["properties"]["instruction"]
                    sender = id_data["properties"]["sender"]
                    senderName = id_data["properties"]["senderName"]
                    messageType = id_data["properties"]["messageType"]
                    WMOidentifier = id_data["properties"]["parameters"]["WMOidentifier"]
                    VTEC = id_data["properties"]["parameters"]["VTEC"]

                except KeyError:
                    pass

                if VTEC[0] != "V":
                    VTEC = VTEC[0]

                if instruction is None:
                    instruction = "Instruction was not giving by the API"

                body = f"""
{VTEC}

{WMOidentifier[0]}
Status............: {status}
Message Type......: {messageType}
Response..........: {response}
Urgency...........: {urgency}
Severity..........: {severity}
Ends..............: {ends}
Affected Area(s)..: {area}

  
{headline} ({sender})

{description}

{instruction}

-------------------------------------------"""

                with open("last.log", "r") as f:
                    if f.read() == body:
                        continue

                print(f"{id_url}/n{body}")

                with open("last.log", "w") as f:
                    f.write(body)
                    f.close()


def start(refresh: bool = True,
          refresh_time: int = 30,
          refresh_count: int = 5,
          state: str = None):
    """
    Start the scan.
    refresh         :   bool, tells the class if it should
                        redo the scan

    refresh_time    :   int, tells the class how many seconds
                        it should wait before refreshing
                        (only works if refresh is True)

    refresh_count   :   int, tells the class how many times to
                        refresh. Set to 0 if you want infinite
                        (only works if refresh is True)

    state           :   str, tells the class what state to scan
                        for (1), initials only, IL, OR, FL, and
                        so on
    """

    state = state.upper()

    if refresh is True:
        if refresh_count != 0:
            for i in range(refresh_count):
                Scan(state)
                print(f"Updating in {refresh_time} second(s)...")
                time.sleep(refresh_time)

                with open("last.log", "w") as f:
                    f.write("")
                    f.close()
        else:
            while True:
                Scan(state)
                print(f"Updating in {refresh_time} second(s)...")
                time.sleep(refresh_time)

                with open("last.log", "w") as f:
                    f.write("")
                    f.close()
    else:
        Scan(state)

        with open("last.log", "w") as f:
            f.write("")
            f.close()
