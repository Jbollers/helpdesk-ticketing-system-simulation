import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "tickets.json")

class Ticket:

    #Creates Ticket class with attributes
    def __init__(self, ticket_id, description, status = "Open", created_at=None):

        self.ticket_id = ticket_id

        self.description = description

        self.status = status

        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    #Define method to resolve ticket
    def resolve(self):

        self.status = "Resolved"

    def to_dict(self):

        return {

            "ticket_id": self.ticket_id,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at
        }
    
    def from_dict(data):

        return Ticket(data["ticket_id"], data["description"], data.get("status", "Open"), data.open("created_at"))


#Manage class with attributes
class TicketSystem:

    def __init__(self, filename=DATA_PATH):

        self.filename = filename

        self.tickets = []

        self.next_id = 1

        self.load_tickets()

    def load_tickets(self):

        if os.path.exists(self.filename):

            try:

                with open(self.filename, "r") as file:
                    
                    content = file.read().strip()

                    if content:

                        data = json.load(file)

                        self.tickets = [Ticket.from_dict(item) for item in data]

                        if self.tickets:

                            self.next_id - max(ticket.ticket_id for ticket in self.tickets) + 1

                        else:

                            self.tickets = []

            except (json.JSONDecodeError, IOError) as e:

                print(f"[Error] Could not load tickets: {e}")

                self.tickets = []

        else:
            
            os.makedirs(os.path.dirname(self.filename), exist_ok=True)
            with open(self.filename, "w") as file:

                json.dump([], file)
            
        

    def save_tickets(self):

        with open(self.filename, "w") as file:

            json.dump([ticket.to_dict() for ticket in self.tickets], file, indent=4)

    #Method for creating a ticket
    def create_ticket(self, description):

        ticket = Ticket(self.next_id, description)

        self.tickets.append(ticket)

        self.save_tickets()

        self.next_id += 1

        print(f"Ticket #{ticket.ticket_id} created at {ticket.created_at}.")

    #Method for viewing tickets
    def view_tickets(self):

        if not self.tickets:

            print("No tickets found.")


        else:

            for ticket in self.tickets:

                print(f"ID: {ticket.ticket_id}, Description: {ticket.description}, Status: {ticket.status}, Created At: {ticket.created_at}")


    #Method for marking tickets as resolved
    def resolve_ticket(self, ticket_id):

        for ticket in self.tickets:

            if ticket.ticket_id == ticket_id:

                ticket.resolve()

                self.save_tickets()

                print(f"Ticket #{ticket_id} resolved.")
                return
            
        print(f"Ticket #{ticket_id} not found.")



#Main function for user interaction
def main():

    system = TicketSystem()

    while True:

        print("\nTicket Management System")

        print("1. Create Ticket")
        print("2. View Ticket")
        print("3. Resolve Ticket")
        print("4. Exit")


        choice = input("Enter your choice: ")

        #Response to user choice
        if choice == "1":

            description = input("Enter the ticket description: ")

            system.create_ticket(description)


        elif choice == "2":

            system.view_tickets()


        elif choice == "3":

            try:

                ticket_id = int(input("Enter the ticket ID to resolve: "))

                system.resolve_ticket(ticket_id)

            except ValueError:

                print("Invalid ticket ID. Please enter a number.")


        elif choice == "4":

            system.save_tickets()
            print("Exiting the Ticket Management System.")
            break


        else:

            print("Invalid choice. Please select a valid option!")


#Code to run the script
if __name__ == "__main__":

    main()