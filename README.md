# SE4AS_EcoTrafficFlowManager
## Introduction
The developed autonomous system represents a solution for traffic light management aimed at minimizing traffic congestion, optimizing fuel consumption and reducing environmental pollution.

Utilizing machine learning techniques, the system employs real-time data analysis and image recognition to detect vehicles within the scenario. This approach is designed to enhance the efficiency of traffic flow, thereby reducing wait times and alleviating queues. The system relies on cameras strategically positioned at each intersection, capturing images that are subsequently used to assess the volume of vehicles present.

In addition to vehicle detection, the system incorporates a responsive feature to address the presence of people waiting at a traffic signal. If someone has activated the corresponding button, the system takes this into consideration, adjusting its operation accordingly. This approach not only optimizes vehicular movement but also prioritizes the safety and convenience of pedestrians at crosswalks.
## Architecture Diagram
![image](https://github.com/RobyBobby24/SE4AS_EcoTrafficFlowManager/assets/64257821/6f468639-1e97-40b8-aece-886d567caf45)

Sequence Diagram 1: Traffic Light Subsystem
 ![image](https://github.com/RobyBobby24/SE4AS_EcoTrafficFlowManager/assets/64257821/29e7e024-1a4e-4295-90e9-35a1df39a1ab)

Sequence Diagram 2: Traffic Switcher Subsystem
![image](https://github.com/RobyBobby24/SE4AS_EcoTrafficFlowManager/assets/64257821/24ab118e-59c8-4fd7-b331-ce877dc03b0e)
![image](https://github.com/RobyBobby24/SE4AS_EcoTrafficFlowManager/assets/64257821/bd269ae9-1b7e-4349-aff3-8657b849c5b2)


<b>The full documentation can be found in "SE4AS Project.pdf"</b>
## Instructions to use the system.
1.	git clone https://github.com/RobyBobby24/SE4AS_EcoTrafficFlowManager.git
2.	In the cmd of the directory run: docker compose build.
3.	In the cmd of the directory run: docker compose up.
4.	To access InlfuxDB (admin:adminadmin).
5.	To access Grafana (admin:admin).
6.	To close, in the cmd of the directory run: docker compose down
