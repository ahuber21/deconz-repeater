import json
import logging
import requests
import time

logging.basicConfig(level=logging.INFO)

KEY = "2907919579"
BASE_URL = f"http://192.168.0.214:8081/api/{KEY}/lights"

# which light should be repeated on change?
TARGET = "Kaffeebar"
ATTRIB = "name"  # e.g. manufacturername, name, etags, etc.

# the value to be repeated
VALUE = 0

def main():
    while True:
        try:
            refresh()
        except Exception as e:
            logging.error("Caught %s - please debug", str(e))
            time.sleep(5)
        time.sleep(0.5)

def refresh():
    r = requests.get(BASE_URL)
    if r.status_code != 200:
        logging.error("Failed to GET current light status")
        return

    # convert status to object by parsing the json
    data = json.loads(r.text)

    # find the object for which the script is configured
    try:
        my_id, my_obj = [(_id, obj) for _id, obj in data.items() if obj[ATTRIB] == TARGET][0]
    except:
        logging.error("Failed to find object with %s = %s", ATTRIB, TARGET)
        return

    # nothing to do if the state is off
    if not my_obj["state"]["on"]:
        return

    # repeat if the value has changed
    current_bri = my_obj["state"]["bri"]
    global VALUE
    if current_bri == VALUE:
        logging.debug("current_bri unchanged at %d", current_bri)
        return

    # make the request to set the brightness again
    url = f"{BASE_URL}/{my_id}/state"
    r = requests.put(url, json={"on": True, "bri": current_bri})

    if r.status_code != 200:
        logging.error("Failed to PUT current light status")
        r.raise_for_status()
        return
    logging.info("Updated bri to %d", current_bri)
    VALUE = current_bri


if __name__ == "__main__":
    main()
