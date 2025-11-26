"""
<plugin key="WazeRouteTime" name="Waze Route Time Calculator" author="cth35" version="1.1.0" externallink="https://github.com/cth35/Domoticz-WazeTimeTravel-Plugin">
    <params>
        <param field="Mode1" label="From" width="200px" required="true" default="Rennes, France"/>
        <param field="Mode2" label="To" width="200px" required="true" default="Paris, France"/>
        <param field="Mode3" label="Time window begin (hh:mm)" width="100px" required="false" default="06:30"/>
        <param field="Mode4" label="Time windows end (hh:mm)" width="100px" required="false" default="20:00"/>
        <param field="Mode5" label="Refresh interval (seconds)" width="100px" required="false" default="300"/>
        <param field="Mode6" label="Region" width="150px">
            <options>
                <option label="Europe (EU)" value="EU" default="true"/>
                <option label="USA (US)" value="US"/>
                <option label="Israël (IL)" value="IL"/>
            </options>
        </param>
    </params>
    <description>
        Waze time travel plugin. Display time in minutes from one location to another.
    </description>
</plugin>
"""

import Domoticz
import datetime
import time
import WazeRouteCalculator
import logging

logging.basicConfig()
logging.getLogger("WazeRouteCalculator").setLevel(logging.DEBUG)

class BasePlugin:
    def __init__(self):
        self.from_address = ""
        self.to_address = ""
        self.region = ""
        self.last_update = 0
        self.update_interval = 300  # 5 minutes
        self.time_window_start = "06:30"
        self.time_window_end = "20:00"

    def onStart(self):
        Domoticz.Log("Plugin started")
        self.from_address = Parameters["Mode1"]
        self.to_address = Parameters["Mode2"]
    
        self.time_window_start = Parameters.get("Mode3", "06:30")
        self.time_window_end = Parameters.get("Mode4", "20:00")

        # Get update interval from parameters, fallback to default if invalid
        if "Mode5" in Parameters and Parameters["Mode5"].isdigit():
          self.update_interval = int(Parameters["Mode5"])
        else:
          self.update_interval = 300

        Domoticz.Log(f"Refresh interval : {self.update_interval} seconds - Range: {self.time_window_start} to {self.time_window_end}")

        self.region = Parameters["Mode6"]

        if len(Devices) == 0:
            Domoticz.Device(Name="Trip", Unit=1, TypeName="Custom", Used=True).Create()

        self.update_route()

    def onStop(self):
        Domoticz.Log("Plugin stopped")

    def onHeartbeat(self):
        if not self._is_in_time_window():
            Domoticz.Log("Outside time window, skipping calculation.")
            return
        current_time = time.time()
        if current_time - self.last_update > self.update_interval:
            self.update_route()
            self.last_update = current_time

    def _is_in_time_window(self):
        try:
            now = datetime.datetime.now().time()
            start = datetime.datetime.strptime(self.time_window_start, "%H:%M").time()
            end = datetime.datetime.strptime(self.time_window_end, "%H:%M").time()
            if start <= end:
                return start <= now <= end
            # Case night range (ex: 22:00 to 06:00)
            return now >= start or now <= end
        except Exception as e:
            Domoticz.Error(f"Error parsing time range : {str(e)}")
            return True

    def update_route(self):
        try:
            Domoticz.Log("Calculating fastest route...")
            route_go = WazeRouteCalculator.WazeRouteCalculator(
                self.from_address, self.to_address, self.region)
            
            routes = route_go.calc_all_routes_info()
            best_route = None
            min_time = None

            for (route_label, (duration, distance)) in routes.items():
                if (min_time is None) or (duration < min_time):
                    min_time = duration
                    best_route = (route_label, duration, distance)
                    Domoticz.Log(f"TRY route: {route_label} ({duration} min, {distance} km)")

            if best_route:
                route_label, duration, distance = best_route
                Domoticz.Log(f"Selected route: {route_label} ({duration} min, {distance} km)")
                if 1 in Devices:
                    # nValue is integer time, sValue is string time (to 2 decimals)
                    Devices[1].Update(nValue=int(duration), sValue=str(round(duration, 2)))
            else:
                Domoticz.Error("No routes found!")

        except Exception as e:
            Domoticz.Error(f"Error in Waze computation : {str(e)}")

global _plugin
_plugin = BasePlugin()

def onStart():
    _plugin.onStart()

def onStop():
    _plugin.onStop()

def onHeartbeat():
    _plugin.onHeartbeat()
