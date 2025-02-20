from datetime import date
import os 
import sys

from frostclient.impl import FrostClientImpl

def main(args: list[str]):
    if "MET_CLIENT_ID" not in os.environ:
        print("Error! environment variable MET_CLIENT_ID was not set!")
        sys.exit(1)
    if len(args) != 5:
        print("Error! Wrong number of arguments provided!")
        print("Usage Hint: $ frostclient LOCATION 'temperature'|'precipitation' FROM UNTIL")
        sys.exit(1)
    location = args[1]
    elements = args[2]
    begin = date.fromisoformat(args[3])
    until = date.fromisoformat(args[4])
    client = FrostClientImpl(os.environ["MET_CLIENT_ID"])
    if elements == "temperature":
        result = client.getTemperatures(location, begin, until)
    elif elements == "precipitation":
        result = client.getPrecipitations(location, begin, until)
    else:
        print(f"Error! weather elements '{elements}' not supported!")
        sys.exit(1)
    print(f"Showing {elements} observations from {begin.isoformat()} until {until.isoformat()} at {location}")
    for obs in result:
        print(obs)


if __name__ == "__main__":
    main(sys.argv)
