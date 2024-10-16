# Control Solar Power with Tuya API + SolaxCloud API

## Objective
The goal of this project is to automate the management of power sources between solar energy and the grid, based on the capacity of a battery system, charged from the solar panels.
Unfortunately, SolaxCloud hasn't functionality to create the algorithm, so I used Tuya API to turn on the smart socket (in fact relay) connected to the grid.

## The algorithm:
1. Get real-time data about battery capacity from the SolaxCloud API
2. If battery capacity below 15% => Turn on the Smart Life smart socket (relay) with Tuya API, which turns on the power supply from the grid
3. If not => the grid power remains off, ensuring optimal usage of solar energy

```
Alternatively, you can use Tuya API for a completely different purposes.
In this project, I'm using the basic Smart Home Basic Service to control the specified device.
In the files you can see how to send GET and POST requests with Tuya API and use this for your projects.
```

## Prerequisites
1. Created Account in SolaxCloud
2. Obtained token ID from the https://global.solaxcloud.com -> Service -> API
3. Obtained registration number of the inverter from the https://global.solaxcloud.com -> Device -> Inverter -> Registration No. column
4. Created Account in Tuya Developer Platform https://platform.tuya.com/
5. Created Cloud Smart Home project and imported devices from the Smart Life Account
6. Obtained Client ID and Client Secret from the section Authorization in the project
7. Replaced the corresponding values of the variables in files "get_token.py", "refresh_token.py" and "script.py" with values from paragraphs 2,3,6

## Before compiling the script.py, you must first compile get_token.py to get a token for the Tuya API.
After automation, file get_token.py will not be needed, because the token will be refreshed with refresh_token.py every 2 hours
So I didn't include code here to avoid doubling the number of requests each time. (Request to control device + unnecessary Request to get token)
If you forget to update the token within 2 hours, you need to get a new one using get_token.py

## Summary
This solution leads to maximizing the use of solar power while ensuring seamless energy supply when the battery is discharged, providing an efficient and automated approach to hybrid power management
