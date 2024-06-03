import pytest
from abc import ABC

class MyError(Exception):
    def __str__(self) -> str:
        return "you cannot have more than 2 instances"


#class BaseInstanceCounter(ABC):


class InstanceCounter:
    static_var = 0
     
    def __init__(self) -> None:
        if InstanceCounter.static_var > 2:
            raise MyError()
        InstanceCounter.static_var += 1
        self.instance_var = InstanceCounter.static_var 

    @staticmethod
    def get_nb_live_instances():
        return InstanceCounter.static_var

    def __del__(self):
        print("deleting")
        
    def __enter__(self):
        pass
    
    def __exit__(self, *args):
        InstanceCounter.static_var -= 1

def test_should_return_one_if_we_have_one_live_instane():
    with InstanceCounter() as counter:
        assert(InstanceCounter.get_nb_live_instances() == 1)

def test_should_not_accept_three_instances():
    with pytest.raises(MyError) as e_info:
        counter1 = InstanceCounter()
        counter2 = InstanceCounter()
        counter3 = InstanceCounter()

def test_should_return_two_if_we_have_two_live_instane():
    counter1 = InstanceCounter()
    counter2 = InstanceCounter()
    assert(InstanceCounter.get_nb_live_instances() == 2)



    [i for i in range(5)]

from collections import Counter
def has_doublon(l):
    #d = Counter(l)
    d = {}
    for i in l:
        d[i] += 1
        if d[i] == 2:
            return True

    
