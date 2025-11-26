# Waze Route Time Calculator - Domoticz Plugin

This Domoticz plugin calculates and displays the estimated travel time (in minutes) for the fastest route between two locations using the Waze routing service.

## Features

- Calculates travel time from a configurable "From" address to a "To" address.
- Supports configurable time windows during which the route is updated.
- Configurable refresh interval to update the travel time periodically.
- Supports multiple regions: Europe (EU), USA (US), and Israel (IL).
- Displays travel time on a custom Domoticz device.

## Configuration Parameters

| Parameter            | Description                                 | Default Value    |
|----------------------|---------------------------------------------|------------------|
| From                 | Starting location address                   | Rennes, France   |
| To                   | Destination location address                | Paris, France    |
| Time window begin    | Time of day to start updates (hh:mm)        | 06:30            |
| Time window end      | Time of day to stop updates (hh:mm)         | 20:00            |
| Refresh interval     | Update interval in seconds                  | 300 (5 minutes)  |
| Region               | Region for routing (EU, US, IL)             | Europe (EU)      |

## Installation

1. Clone this project directly in your Domoticz plugins directory (Or create directory and put the `plugin.py` file)
2. Install WazeRouteCalculator with

```
sudo pip3 install WazeRouteCalculator
```

3. Configure the plugin parameters via the Domoticz Hardware tab.

<img width="1178" height="487" alt="image" src="https://github.com/user-attachments/assets/017bf6ff-9dcf-41b6-8306-7edfd06c8c01" />

4. Restart domoticz; it creates a Domoticz custom device named "Trip" to show travel time (don't forget to allow discovering of new devices in settings).

## Usage

- The plugin uses the [WazeRouteCalculator](https://github.com/kovacsbalu/WazeRouteCalculator) module to compute the fastest route duration.
- It updates the travel time device only if the current time falls within the configured time window.
- The travel time refreshes automatically based on the refresh interval parameter.

> [!WARNING]
> **Known Issue: Accuracy with Location Names**  
> Using location names (e.g., "Paris, France") instead of precise GPS coordinates can lead to less accurate route and travel time calculations. This is because geocoding from place names to coordinates may introduce imprecision or ambiguity, which affects routing results.  
> For reliable and precise travel time estimates, users are strongly advised to use GPS coordinates (latitude, longitude) for both origin and destination whenever possible.
## Dependencies

- Requires the `WazeRouteCalculator` Python module. More details and installation instructions available [here](https://github.com/kovacsbalu/WazeRouteCalculator).
- Runs in the Domoticz Python plugin environment.

## Special Thanks

Special thanks to the author of the WazeRouteCalculator library: [kovacsbalu](https://github.com/kovacsbalu/WazeRouteCalculator) for providing the essential API integration and routing calculations.

## License

MIT License

