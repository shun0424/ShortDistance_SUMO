import traci
import sumolib

# Start the SUMO simulation
sumoBinary = sumolib.checkBinary('sumo-gui')  # Use 'sumo' if you don't need the GUI
traci.start([sumoBinary, "-c", "./osm.sumocfg"])

# Define the incident parameters
incident_time = 500  # Time step when the incident occurs
incident_duration = 9000  # Duration of the incident
incident_edges = ['977465924#1', '977465924#4', '465069434#1', '465069439#2', '1101850024', '978085966#9']  # Edges where the incidents occur
incident_lane = 0  # Lane where the incidents occur

def reroute_vehicles():
    # Get the list of all vehicles in the simulation
    vehicle_ids = traci.vehicle.getIDList()
    for vehicle_id in vehicle_ids:
        try:
            # Find an alternative route for the vehicle
            traci.vehicle.rerouteTraveltime(vehicle_id)
        except traci.TraCIException:
            # Handle any exceptions (e.g., if the vehicle can't be rerouted)
            pass

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    current_time = traci.simulation.getTime()

    # Introduce the incidents
    if current_time == incident_time:
        for edge in incident_edges:
            traci.edge.setDisallowed(edge, ["passenger"])
        # Reroute vehicles immediately after the incident
        reroute_vehicles()

    # Clear the incidents after the duration
    if current_time == incident_time + incident_duration:
        for edge in incident_edges:
            traci.edge.setAllowed(edge, ["passenger"])
        # Optionally, reroute vehicles again to normalize traffic
        reroute_vehicles()

traci.close()