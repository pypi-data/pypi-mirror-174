import os

from fpodms import Client


def test_client_init():
    fpodms = Client(
        email_address=os.getenv("EMAIL_ADDRESS"), password=os.getenv("PASSWORD")
    )
    assert isinstance(fpodms, Client)

    return fpodms


fpodms = test_client_init()
