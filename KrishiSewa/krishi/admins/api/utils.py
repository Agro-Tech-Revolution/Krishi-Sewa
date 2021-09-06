from api.serializers import *
from api.models import *
from admins.api.serializers import *

def get_ticket_data(request, tickets):
    ticket_data = TicketSerializer(tickets, many=True).data
    for ticket in ticket_data:
        ticket_to = User.objects.get(id=ticket["ticket_to"])
        ticket_to_data = UserSerializer(ticket_to).data 
        profile_for_ticket_to = Profile.objects.get(user=ticket["ticket_to"])
        profile_data_for_ticket_to = UpdateProfileSerializer(profile_for_ticket_to).data 

        ticket_to_data["profile"] = profile_data_for_ticket_to
        ticket["ticket_to"] = ticket_to_data

        ticket_response = TicketResponse.objects.filter(ticket=ticket["id"])
        ticket_response_data = get_ticket_response_data(request, ticket_response)
        for tick_resp in ticket_response_data:
            remove_key = tick_resp.pop("ticket", None)
        ticket["ticket_responses"] = ticket_response_data
    return ticket_data


def get_ticket_response_data(request, ticket_response):
    ticket_response_data = TicketResponseSerializer(ticket_response, many=True).data
    for tick_resp in ticket_response_data:
        ticket = Ticket.objects.get(id=tick_resp["ticket"])
        ticket_data = TicketSerializer(ticket).data 

        ticket_to = User.objects.get(id=ticket_data["ticket_to"])
        ticket_to_data = UserSerializer(ticket_to).data 
        profile_for_ticket_to = Profile.objects.get(user=ticket_data["ticket_to"])
        profile_data_for_ticket_to = UpdateProfileSerializer(profile_for_ticket_to).data 

        ticket_to_data["profile"] = profile_data_for_ticket_to
        ticket_data["ticket_to"] = ticket_to_data
        tick_resp["ticket"] = ticket_data

        response_by = User.objects.get(id=tick_resp["response_by"])
        response_by_data = UserSerializer(response_by).data

        profile_for_response_by = Profile.objects.get(user=tick_resp["response_by"])
        profile_data_for_response_by = UpdateProfileSerializer(profile_for_response_by).data
        response_by_data["profile"] = profile_data_for_response_by
        tick_resp["response_by"] = response_by_data
    return ticket_response_data