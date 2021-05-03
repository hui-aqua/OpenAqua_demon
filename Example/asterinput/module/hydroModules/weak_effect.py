"""
-------------------------------------------\n
-         University of Stavanger          \n
-         Hui Cheng (PhD student)          \n
-          Lin Li (Medveileder)            \n
-      Prof. Muk Chen Ong (Supervisor)     \n
-------------------------------------------\n
Any questions about this code,
please email: hui.cheng@uis.no \n

"""
import numpy as np
from numpy import pi

class net2netWeak:
    """
    #TODO to be modified later
    A module that can be use to deal with net to net wake effect.\n
    .. note: Can only apply to a single fish cage.
    """
    def __init__(self, model_index, initial_node_position,hydro_element, direction, net_solidity):
        """
        :param model_index: [string] Unit: [-]. To indicate the model function, e.g.: 'factor-0.9', 'loland-0.5', 'hui-1'.
        :param initial_node_position: [np.array].shape=(N,3) Unit: [m]. The initial coordinates of N nodes in cartesian coordinate system.
        :param hydro_element: [list] Unit: [-]. A python list to indicate how the lines are connected.
        :param current_velocity: [np.array].shape=(1,3) or a [list] of three values Unit: [m/s]. The current velocity [ux,uy,uz] in cartesian coordinate system.
        :param origin: [np.array].shape=(1,3) or a [list] of three values Unit: [m]. The origin [x,y,z] for detecting the elements in the wake region. For a fish cage, the origin is usually sit in the floating collar.
        :param dw0: [float] Unit: [m]. The diameter of the physical net twines.
        :param net_solidity: [float] Unit: [-]. The solidity of netting.
        """
        self.positions = np.array(initial_node_position)
        self.flow_direction=direction/np.linalg.norm(direction)
        self.elements=hydro_element
        self.origin = np.mean(initial_node_position,axis=0)
        self.sn = net_solidity
        self.wake_type = str(model_index).split("-")[0]
        self.wake_value = str(model_index).split("-")[1]
        self.get_element_in_wake()
        self.reduction_factors=np.ones((len(hydro_element),1))
        # print("\n net2net weak effect is initialized.\n")
        # print(self.flow_direction)
        # print(self.wake_type)
        # print(self.elements)
        # print(self.origin)
        
        # print(self.wake_element_indexes)

    def __str__(self):
        s0 = "The selected wake model is " + str(self.wake_type) + "\n"
        s1 = "The index of the nodes in the wake region is " + str(self.wake_element_indexes) + "\n"
        S = s0 + s1
        return S

    def is_element_in_wake(self, one_element):
        """
        A private function to tell if an element is in wake region or not.\n
        :param one_element: [List] of three values Unit [-]. A list to contain the index of nodes in one element. The list should contain at least two values.
        :return: True if the element in the wave region.
        """
        element_center = np.array([0.0, 0.0, 0.0])  # must be a float
        for node in one_element:
            element_center += np.array(self.positions[int(node)] / len(one_element))
        vector_point_to_origin = np.array(element_center - self.origin)
        if np.dot(vector_point_to_origin, self.flow_direction) < 0:
            return True
        else:
            return False

    def get_element_in_wake(self):
        """
        A private function to go go through all the elements and find the elements in the wake region.\n
        :return: [List] Unit [-]. A list of "indexes of the elements" in the wake region.
        """
        elements_in_wake = []
        for index,element in enumerate(self.elements):
            if self.is_element_in_wake(element):
                elements_in_wake.append(index)
        self.wake_element_indexes=elements_in_wake

    def reduction_factor(self, element_index, alpha=0):
        """
        A public function to return the flow reduction factor according to the index of element (and inflow angle).\n
        :param element_index: [integer] Unit [-]. A index of element
        :param alpha: [float] Unit [rad]. *Default value=0*; The inflow angle of the net panel.
        :return: [float] Unit [-]. *Range [0,1]* Flow reduction factor. If value=1, the flow is no change. If value is 0, the flow is reduced to zero.
        """     
        if self.wake_type in ['factor']:
            factor = min(1.0, float(self.wake_value))
        elif self.wake_type in ['loland']:
            factor = float(self.cal_factor1())
        elif self.wake_type in ['hui']:
            factor = float(self.cal_factor2(position))
        else:
            print("the selected wake type " + str(self.wake_type) + " is not supported.")
            print()
        return factor

    def cal_factor1(self):
        """
        A private function calculate the flow reduction factor according to Loland (1991). r=1-0.14*CD (CD is the input value in the ```wakeModel```) \n
        :return: Flow reduction factor: [float] Unit [-].
        """
        cd_0=self.sn-1.24*pow(self.sn,2)+13.7*pow(self.sn,3)
        return (1 - 0.46 * cd_0)

    def cal_factor2(self, alf):
        """
        A private function calculate the flow reduction factor according to Hui et al., (2020).\n
        :param alf: [float] Unit [rad]. Definition: the angle between normal vector of a net panel and the flow direction.
        :return: Flow reduction factor: [float] Unit [-].
        """
        alf = np.abs(alf)
        reduction_factor = (np.cos(alf) + 0.05 - 0.38 * self.sn) / (np.cos(alf) + 0.05)
        return max(0, reduction_factor)
    
    def update_reduction(self,position):
        for i in self.wake_element_indexes:
            self.reduction_factors[i]=self.reduction_factor(position)
        