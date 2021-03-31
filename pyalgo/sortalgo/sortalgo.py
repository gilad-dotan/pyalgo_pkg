import random
import copy
from pyalgo import basic_modules
from pyalgo.basic_modules import sortalgo_default_values


def in_order(List, order='SmallToBig'):
    """
    this function takes a list and check if all the elements are in order
    the default is from the smallest to the biggest
    """

    # // check if the input is valid \\
    if order not in basic_modules.sortalgo_default_values.in_order_default_values:
        raise ValueError(
            f"'order' needs to be from the list of options: {sortalgo_default_values.in_order_default_values}")
        #raise ValueError("'order' needs to be from the list of possibilities:",
        #                 basic_modules.default_functions.print_list_arguments(sortalgo_default_values.in_order_default_values, print_the_msg=True, return_msg=True))

    ListType = basic_modules.default_values.ListType

    if not isinstance(List, ListType):
        raise TypeError("'List' needs to be a list type")



    length = len(List)  # get the length of the list (the number of check that we need to do)

    if order == 'SmallToBig':
        for i in range(length - 1):
            if (List[i + 1] < List[i]):
                return False
    elif order == 'BigToSmall':
        for i in range(length - 1):
            if (List[i + 1] > List[i]):
                return False

    return True





def quick_sort(List):   # // needs to be optimized \\
                        # // may  use a regeession \\

    def split_to_subsets(List, ConstNumber, move_same_value_to='down'):

        # // check that the input is valid \\

        if not move_same_value_to in basic_modules.sortalgo_default_values.\
                quick_sort_default_values.move_same_value_to_default_values:
            raise ValueError("'move_same_value_to' needs to 'up' or 'down'")


        List = copy.deepcopy(List)                 # make a deep-copy to not change the parameters outside the function
        ConstNumber = copy.deepcopy(ConstNumber)   # make a deep-copy to not change the parameters outside the function



        transferList = [[], [ConstNumber], []]

        # // Spliting between the 3 subsets \\
        # // subset 1: the numbers that are smaller than the choosen number \\
        # // subset 2: the choosen number itself \\
        # // subset 3: the numbers that are bigger than the choosen number \\
        for i in range(len(List)):
            if List[i] > ConstNumber:
                transferList[2].append(List[i])
            elif List[i] < ConstNumber:
                transferList[0].append(List[i])
            elif List[i] == ConstNumber:
                if move_same_value_to == 'down':
                    transferList[0].append(List[i])
                elif move_same_value_to == 'up':
                    transferList[2].append(List[i])

        # // Clearing the empty sublists \\
        for i in range(3):
            try:
                if transferList[i] == []:
                    del transferList[i]
            except: pass

        return transferList

    # // preparing list \\
    List = basic_modules.default_functions.to_single_list(List)

    Random_Choosen_Number = random.randint(0, len(List) - 1)
    Random_Choosen_Number = List[Random_Choosen_Number]

    List.remove(Random_Choosen_Number)

    List = split_to_subsets(List, Random_Choosen_Number)

    while not in_order(basic_modules.default_functions.to_single_list(List)):
        for i in range(len(List)):
            if not in_order(basic_modules.default_functions.to_single_list(List[i])):
                pass
                Random_Choosen_Number = random.randint(0, len(List[i])-1)
                Random_Choosen_Number = List[i][Random_Choosen_Number]

                List[i].remove(Random_Choosen_Number)

                TransferList = split_to_subsets(List[i], Random_Choosen_Number)

                del List[i]
                for j in range(len(TransferList)):
                    List.insert(i, TransferList[-1-j])

    return basic_modules.default_functions.to_single_list(List)