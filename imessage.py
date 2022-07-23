import subprocess
from typing import List


def send_imessage(reciever_contact: str, message: str):
    """
    Sends an iMessage to a contact with a specified message.
    The contact can be either a phone number or email address.
    Note: using triple quote strings will have awkward formatting when the message is sent.

    :param str reciever_contact: the contact of the person recieving the message
    :param str message: the message being sent to the reciever
    """
    res = subprocess.run(["osascript", "imessage.scpt", reciever_contact,
                         message], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        assert res.returncode != 0, res.stderr.decode('utf-8')


def send_group_imessage(reciever_contacts: List[str], message: str):
    """
    Sends a iMessage to multiple recievers with a specified message.
    The contact can be either a phone number or email address.
    Note: using triple quote strings will have awkward formatting when the message is sent.


    :param List[str] reciever_contacts: a list of contacts for the recievers of the message
    :param str message: the message being sent to the recievers
    """
    for contact in reciever_contacts:
        send_imessage(contact, message)

