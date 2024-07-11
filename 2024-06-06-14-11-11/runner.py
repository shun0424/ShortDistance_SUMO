import traci
import sumolib
import numpy as np
import random

# Start the SUMO simulation
sumoBinary = sumolib.checkBinary('sumo-gui')  # Use 'sumo' if you don't need the GUI
traci.start([sumoBinary, "-c", "./osm.sumocfg"])

# Define Route
start_edge = "BL_Start"  # Replace with your start edge ID
start_edge_2 = "B_Start"
stop_edge = "TR_End"    # Replace with your stop edge ID

# Define the incident parameters
incident_time = 500  # Time step when the incident occurs
incident_duration = 1000  # Duration of the incident
incident_number = 150
incident_edge_list = traci.edge.getIDList()
selected_edge_list = []
vehicle_num = 200

def reroute_vehicles():
    # Get the list of all vehicles in the simulation
    vehicle_ids = traci.vehicle.getIDList()
    for vehicle_id in vehicle_ids:
        try:
            # Find an alternative route for the vehicle
            v_route = traci.vehicle.getRoute(vehicle_id)
            print(vehicle_id +" " + str(traci.vehicle.getDeparture(vehicle_id)))
            print("Before Re_route : " + str(v_route))

            traci.vehicle.rerouteTraveltime(vehicle_id)
            
            v_route = traci.vehicle.getRoute(vehicle_id)
            print("After Re_route : " + str(v_route))
            
            print("------------------------------------   ------------------------------")
        
        except traci.TraCIException:
            # Handle any exceptions (e.g., if the vehicle can't be rerouted)
            pass

def random_incident(edge_list, edge_number):
    random_list = np.random.choice(edge_list, size=edge_number)
    # print(random_list)
    for incident_edge in random_list:
        traci.edge.setDisallowed(incident_edge, ["passenger"])
    traci.edge.setDisallowed("incident_Lane",["passenger"])
    return random_list

def clear_incident(incident_list):
    for incident_edge in incident_list:
            traci.edge.setAllowed(incident_edge , ["passenger"])
    traci.edge.setAllowed("incident_Lane",["passenger"])
    selected_edge_list = []

route_edges = traci.simulation.findRoute(start_edge, stop_edge).edges

route_edges_2 = traci.simulation.findRoute(start_edge_2, stop_edge).edges

# Add the calculated route to TraCI
traci.route.add('r_0', route_edges)
traci.route.add('r_1', route_edges_2)


for i in range(vehicle_num):
    vehicle_id = "v" + str(i)
    if i % 2 == 0 :
        traci.vehicle.add(vehicle_id, "r_0")
        traci.vehicle.setRoutingMode(vehID=vehicle_id, routingMode = 1)
    else :
        traci.vehicle.add(vehicle_id, "r_1")

while traci.simulation.getMinExpectedNumber() > 0:
    
    traci.simulationStep()
        
    current_time = traci.simulation.getTime()

    # Introduce the incident
    if current_time == incident_time:
        selected_edge_list = random_incident(incident_edge_list, incident_number)
        # Reroute vehicles immediately after the incident
        reroute_vehicles()

    # Clear the incident after the duration
    if current_time == incident_time + incident_duration:
        clear_incident(selected_edge_list)
        # Optionally, reroute vehicles again to normalize traffic
        reroute_vehicles()
        incident_time = current_time + incident_duration



traci.close()
