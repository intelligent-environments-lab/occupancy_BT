# Occupcny detection by Bluetooth device tracking

This repository is for the Bluetooth based occupancy detection system using Raspberry Pi.

The repository is structed as follows:
- `Individual_Presence`: The l2ping command is used. The system sends packets to pre-defined occupant devices. If a positive return signal is received, then it is considered as occupied, otherwise unoccupied.
- `Crowd_Density`: The lescan command is used. Every one minute, Raspberry Pi logs the number of advertising Bluetooth devices with hashed MAC addresses.

<!---
## `Individual Presence` folder
This folder contains blabla: `temporal` or blabla and `meta` or the data is collected from.

## `Crowd Density` folder
%blablabla `blablabla` - blablabla (or **blablabla**) as blabla
-->

## Publications
- [J.Y. Park, T. Dougherty, and Z. Nagy, ”A Bluetooth based occupancy detection for buildings”, 2018 Building Performance Analysis Conference and SimBuild, Chicago IL, September, 2018](https://www.researchgate.net/publication/326718201_A_Bluetooth_based_occupancy_detection_for_buildings)
- [Z. Nagy, J.R. Vazquez-Canteli, and J.Y. Park, ”Using Bluetooth Based Occupancy Estimation for HVAC Set-back to Reduce Energy Consumption in Buildings ”, 2018 ASHRAE Annual Conference, Houston TX, June, 2018](https://www.researchgate.net/publication/326723732_Using_Bluetooth_Based_Occupancy_Estimation_for_HVAC_Set-back_to_Reduce_Energy_Consumption_in_Buildings)

