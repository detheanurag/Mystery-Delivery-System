import json
import math


def load_data():
    """Load delivery data from the JSON file."""
    with open("data.json", "r") as file:
        return json.load(file)


def calculate_distance(point1, point2):
    #Calculate Euclidean distance between two points.
    x1, y1 = point1
    x2, y2 = point2

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_nearest_agent(agents, warehouse):
    """Find the agent closest to the warehouse.

    `agents` is a list of dicts like {"id": ..., "location": [x, y]}.
    """
    nearest_agent = None
    shortest_distance = float("inf")

    for agent in agents:
        agent_id = agent["id"]
        agent_location = agent["location"]

        distance = calculate_distance(
            agent_location,
            warehouse
        )

        if distance < shortest_distance:
            shortest_distance = distance
            nearest_agent = agent_id

    return nearest_agent, shortest_distance


def create_report(data):
    """Create a delivery report for all agents."""
    # warehouses is a list of {"id": ..., "location": [x, y]} dicts,
    # so build a lookup by id for O(1) access below.
    warehouses = {
        warehouse["id"]: warehouse["location"]
        for warehouse in data["warehouses"]
    }
    agents = data["agents"]
    packages = data["packages"]

    report = {}

    for agent in agents:
        agent_id = agent["id"]
        report[agent_id] = {
            "packages_delivered": 0,
            "total_distance": 0
        }

    for package in packages:
        warehouse = warehouses[package["warehouse_id"]]
        destination = package["destination"]

        nearest_agent, agent_to_warehouse = find_nearest_agent(
            agents,
            warehouse
        )

        warehouse_to_destination = calculate_distance(
            warehouse,
            destination
        )

        total_distance = (
            agent_to_warehouse + warehouse_to_destination
        )

        report[nearest_agent]["packages_delivered"] += 1
        report[nearest_agent]["total_distance"] += total_distance

    return report


def calculate_efficiency(report):
    #Calculate average delivery distance for each agent.
    for agent_id in report:
        packages_delivered = report[agent_id]["packages_delivered"]
        total_distance = report[agent_id]["total_distance"]

        if packages_delivered > 0:
            efficiency = total_distance / packages_delivered
        else:
            efficiency = 0

        report[agent_id]["total_distance"] = round(
            total_distance,
            2
        )

        report[agent_id]["efficiency"] = round(
            efficiency,
            2
        )

    return report


def find_best_agent(report):
    #Find the agent with the lowest average distance
    return min(
        report,
        key=lambda agent_id: report[agent_id]["efficiency"]
    )


def save_report(report):
    #Save the delivery report to a JSON file
    with open("report.json", "w") as file:
        json.dump(report, file, indent=4)


def display_report(report):
    #Display the delivery report
    print("Delivery Report")
    print("----------------")

    for agent_id, details in report.items():
        print(agent_id, ":", details)


def main():
    #Run the delivery system
    data = load_data()

    report = create_report(data)

    report = calculate_efficiency(report)

    best_agent = find_best_agent(report)

    save_report(report)

    display_report(report)

    print("\nBest agent:", best_agent)
    print("Report saved to report.json")


if __name__ == "__main__":
    main()