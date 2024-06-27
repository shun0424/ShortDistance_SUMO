import traci
import sumolib

# Start the SUMO simulation
sumoBinary = sumolib.checkBinary('sumo-gui')  # Use 'sumo' if you don't need the GUI
traci.start([sumoBinary, "-c", "./osm.sumocfg"])

# Define the incident parameters
incident_time = 500  # Time step when the incident occurs
incident_duration = 9000  # Duration of the incident
incident_edge = '977465924#1'  # Edge where the incident occurs
incident_lane = 0  # Lane where the incident occurs

def reroute_vehicles():
    # Get the list of all vehicles in the simulation
    vehicle_ids = traci.vehicle.getIDList()
    for vehicle_id in vehicle_ids:
        try:
            # Find an alternative route for the vehicle
            v_route = traci.vehicle.getRoute(vehicle_id)
            print(vehicle_id)
            print("Before Re_route : " + str(v_route))
            traci.vehicle.rerouteTraveltime(vehicle_id)
            v_route = traci.vehicle.getRoute(vehicle_id)
            print("After Re_route : " + str(v_route))
            print("------------------------------------------------------------------")
        except traci.TraCIException:
            # Handle any exceptions (e.g., if the vehicle can't be rerouted)
            pass

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    current_time = traci.simulation.getTime()

    # Introduce the incident
    if current_time == incident_time:
        traci.edge.setDisallowed(incident_edge, ["passenger"])
        # Reroute vehicles immediately after the incident
        reroute_vehicles()

    # Clear the incident after the duration
    if current_time == incident_time + incident_duration:
        traci.edge.setAllowed(incident_edge , ["passenger"])
        # Optionally, reroute vehicles again to normalize traffic
        reroute_vehicles()

traci.close()
