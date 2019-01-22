import random
import copy


class Agent:
    def __init__(self, name, value, priority, neighbor_list, domain):
        self.name = name
        self.value = value
        self.priority = priority
        self.neighbors_list = copy.deepcopy(neighbor_list)
        self.agent_domain = domain
        self.consistent = True
        self.constraints = []
        # if self.neighbors_list:
        #     for neighbor_agent in neighbor_list:
        #         self.neighbors_list.append(
        #             {'name': neighbor_agent.name, 'value': neighbor_agent.value, 'priority': neighbor_agent.priority})

    def check_consistency(self):
        self.consistent = True
        for neighbor in self.neighbors_list:
            if neighbor.value == self.value:
                self.consistent = False

    def change_value(self):
        self.value = random.choice(self.agent_domain)

    def check_local_view(self):
        print("check_local_view for {0}".format(self.name))
        self.check_consistency()
        if not self.consistent:
            print("agent {0} value is not consistent with neighbor(s)".format(self.name))
            old_value = self.value
            for domain in self.agent_domain:
                self.value = domain
                self.check_consistency()
                if self.consistent:
                    break
            if not self.consistent:
                for agents in self.neighbors_list:
                    if agents.priority == self.priority - 1:
                        master_agent = agents
                print("backtracking for agent {0}".format(self.name))
                backtrack(master_agent)
            else:
                for agents in self.neighbors_list:
                    send_handle_ok(self)

    def handle_ok(self, agent):
        for neighbor in self.neighbors_list:
            print("handle_ok? for agent {0}".format(agent.name))
            if neighbor.name == agent.name:
                neighbor.value = agent.value
                neighbor.priority = agent.priority
                self.check_local_view()

    # def handle_nogood(self, agent, nogood_list):
    #     self.constraints.append(nogood_list)
    #     for agent_in_nogood in nogood_list:
    #         if any(neighbor_agent['name'] == agent_in_nogood[0] for neighbor_agent in self.neighbors_list):
    #             pass
    #         else:
    #             self.neighbors_list.append(
    #                 {'name': agent_in_nogood[0], 'value': agent_in_nogood[1], 'priority': agent_in_nogood[2]})
    #     old_value = self.value
    #     self.check_local_view()
    #     if old_value != self.value:
    #         for agents in self.neighbors_list:
    #             send_handle_ok(self)


def backtrack(master_agent):
    higher_priority_agents = []
    higher_domains = []
    for neighbor in master_agent.neighbors_list:
        if neighbor.priority < master_agent.priority:
            higher_priority_agents.append(neighbor)
    for agent in higher_priority_agents:
        higher_domains.append(agent.value)
    if master_agent.agent_domain == higher_domains:
        print("no_solution")
    else:
        if not (master_agent.value in higher_domains):
            print("no_solution")
            return 0
        while master_agent.value in higher_domains:
            master_agent.value = random.choice(master_agent.agent_domain)
        for agents in master_agent.neighbors_list:
            if agents.priority > master_agent.priority:
                send_handle_ok(master_agent)


def send_handle_ok(agent):
    for agents in agent.neighbors_list:
        if agents:
            if agents.priority > agent.priority:
                agents.handle_ok(agent)


def abt(agent_list):
    for agent in agent_list:
        agent.check_consistency()
        send_handle_ok(agent)


# agent1 = Agent
# agent2 = Agent
# agent3 = Agent

agent1 = Agent('agent1', 'red', 1, [], ['red', 'blue', 'yellow'])
agent2 = Agent('agent2', 'red', 2, [], ['red', 'blue', 'yellow'])
agent3 = Agent('agent3', 'red', 3, [], ['red', 'blue', 'yellow'])
agent1.neighbors_list.append(agent2)
agent1.neighbors_list.append(agent3)
agent2.neighbors_list.append(agent1)
agent2.neighbors_list.append(agent3)
agent3.neighbors_list.append(agent1)
agent3.neighbors_list.append(agent2)
agent_list = [agent1, agent2, agent3]
abt(agent_list)
print(agent1.value)
print(agent2.value)
print(agent3.value)

