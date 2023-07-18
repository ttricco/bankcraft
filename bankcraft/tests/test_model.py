import pytest
from bankcraft.agent.general_agent import GeneralAgent
from bankcraft.model import Model



def agent():
    return GeneralAgent(Model)


def test_put_people_in_model():
