import random
import copy


class Agent:

    def __init__(self, name, value, neighbor_agent_list, priority, domain_list):
        self.name=name
        self.value = value
        self.priority = priority
        self.neighbor_list = []
        self.consistent = True
        self.domains = copy.deepcopy(domain_list)
        self.constraints = []
        self.no_good_list = []
        for neighbor in neighbor_agent_list:
            self.neighbor_list.append({'name':neighbor.name})

    def handle_ok(self, neighbor, value):
        for item in self.neighbor_list:
            if item['name'] == neighbor:
                item.update({'value': value})
        self.check_local_view()

    def check_consistency(self):
        if any(neighbor['value'] == self.value for neighbor in self.neighbor_list):
            self.consistent = False
        else:
            self.consistent = True


    def check_local_view(self):
        self.check_consistency()
        if not self.consistent:
            for domain in self.domains:
                old_value = copy.deepcopy(self.value)
                self.domains.remove(self.value)
                self.value = self.domains[0]
                self.domains.append(old_value)
                self.check_consistency()
                if self.check_consistency():
                    pass
                else:
                    for neighbor in self.neighbor_list:
                        if neighbor['priority']==self.priority-1:
                            #send backtrack to higher priority agent

    def handle_no_good(self, neighbor, no_good):
        self.constraints.append(no_good)
        for no_good_neighbor in no_good:
            if not any(no_good_neighbor[0] != neighbor['name'] for neighbor in self.neighbor_list):
                self.neighbor_list.append({'name': no_good_neighbor[0], 'value': no_good_neighbor[1], 'priority':no_good_neighbor[2]})
        old_value = copy.deepcopy(self.value)
        self.check_local_view()
        if old_value != self.value:
         # send handle ok?

    def backtrack(self):
        for domain in self.domains:
            old_value = copy.deepcopy(self.value)
            self.domains.remove(self.value)
            self.value = self.domains[0]
            self.domains.append(old_value)
            #check conssistency with higher priority sgentd



def send_handle_ok(neighbor_agent,update_agent):


def abt(agent_list):
    for agent in agent_list:
        agent.check_consistency()
        if agent.consistent:
            for neighbor in agent.neighbor_list:
                send_handle_ok(neighbor,agent)
        else:
            agent.backtrack()




agent1,agent2,agent3=Agent()
agent2=Agent('red', [agent1], 2, ['red','blue','green'])
agent3=Agent('red', [agent1], 3, ['red','blue','green'])
agent1=Agent('red', [agent2,agent3], 1, ['red','blue','green'])
agent_list= [agent1, agent2, agent3]
abt(agent_list)