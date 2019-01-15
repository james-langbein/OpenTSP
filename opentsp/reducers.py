from opentsp import helpers


def diamond_prune(instance):

    # def list_prune(ls):
    #     var = True  # may not be needed
    #     while var is True:  # may not be needed
    #         bad_count = 0  # may not be needed
    #         semi_pruned_ls = [i for i in ls if i.fitness == 'good']  # may not be needed
    #         last_good_index = 0
    #         for index, edge in enumerate(semi_pruned_ls):
    #             if index == 0 or index == len(semi_pruned_ls) - 1:
    #                 pass
    #             elif edge.length_ > semi_pruned_ls[last_good_index].length_ \
    #                     or edge.length_ > semi_pruned_ls[index + 1].length_:
    #                 edge.fitness = 'bad'
    #                 # for i in instance.edges.values():
    #                 #     if i == edge:
    #                 #         i.fitness = 'bad'
    #                 bad_count += 1  # may not be needed
    #             else:
    #                 last_good_index = index
    #         if bad_count == 0:  # may not be needed
    #             var = False  # may not be needed
    #     pruned_ls = semi_pruned_ls  # may not be needed
    #     return pruned_ls
    #
    # def list_prune_v2(ls, n):  # changed 'bad' count check to a while loop less than three check, added another test
    #     loop = 1  # may not be needed
    #     while loop < n + 1:  # may not be needed
    #         semi_pruned_ls = [i for i in ls if i.fitness == 'good']  # may not be needed
    #         if len(semi_pruned_ls) <= 2:
    #             break
    #         last_good_index = 0
    #         for index, edge in enumerate(semi_pruned_ls):
    #             if index == 0 or index == len(semi_pruned_ls) - 1:
    #                 pass
    #             elif edge.length_ > semi_pruned_ls[last_good_index].length_ or \
    #                     edge.length_ > semi_pruned_ls[index + 1].length_:
    #                 edge.fitness = 'bad'
    #             else:
    #                 last_good_index = index
    #         loop += 1
    #     if len(semi_pruned_ls) == 3:
    #         if semi_pruned_ls[1].length_ < semi_pruned_ls[0].length_ and \
    #                 semi_pruned_ls[1].length_ < semi_pruned_ls[2].length_:
    #             if abs(helpers.angle(semi_pruned_ls[1].node_one, semi_pruned_ls[1].node_two,
    #                          semi_pruned_ls[0].node_two)) < \
    #                     abs(helpers.angle(semi_pruned_ls[1].node_one, semi_pruned_ls[1].node_two,
    #                               semi_pruned_ls[2].node_two)):
    #                 del semi_pruned_ls[0]
    #             else:
    #                 del semi_pruned_ls[2]
    #         # add an else here in version 3 for when the middle edge is the middle length
    #     pruned_ls = semi_pruned_ls  # may not be needed
    #     return pruned_ls
    #
    # def list_prune_v3(ls):
    #     loop = 1
    #     while loop < 3:
    #         # sp_ls stands for semi-pruned-ls
    #         sp_ls = [i for i in ls if i.fitness == 'good']
    #         if len(sp_ls) <= 3:
    #             break
    #         last_good_index = 0
    #         for index, edge in enumerate(sp_ls):
    #             if index == 0 or index == len(sp_ls) - 1:
    #                 pass
    #             elif edge.length_ > sp_ls[last_good_index].length_ or edge.length_ > sp_ls[index + 1].length_:
    #                 edge.fitness = 'bad'
    #                 # for e in inst.edges.values():
    #                 #     if e == edge:
    #                 #         e.fitness = 'bad'
    #             else:
    #                 last_good_index = index
    #         loop += 1
    #     if len(sp_ls) == 3:
    #         ang_to_0 = helpers.angle(sp_ls[1].node_one, sp_ls[1].node_two, sp_ls[0].node_two)
    #         ang_to_2 = helpers.angle(sp_ls[1].node_one, sp_ls[1].node_two, sp_ls[2].node_two)
    #         # if middle edge of remaining 3 is the shortest:
    #         if sp_ls[1].length_ < sp_ls[0].length_ and sp_ls[1].length_ < sp_ls[2].length_:
    #             # if angle to edge_0 in sp_ls is less then angle to edge_2 in sp_ls:
    #             if abs(ang_to_0) < abs(ang_to_2):
    #                 del sp_ls[0]
    #             else:
    #                 del sp_ls[2]
    #         elif sp_ls[1].length_ > sp_ls[0].length_ or sp_ls[1].length_ > sp_ls[2].length_:
    #             if abs(ang_to_0) < abs(ang_to_2) and sp_ls[0].length_ < sp_ls[2].length_:
    #                 del sp_ls[1]
    #             elif abs(ang_to_0) < abs(ang_to_2) and sp_ls[0].length_ > sp_ls[2].length_:
    #                 del sp_ls[0]
    #             elif abs(ang_to_0) > abs(ang_to_2) and sp_ls[0].length_ > sp_ls[2].length_:
    #                 del sp_ls[1]
    #             elif abs(ang_to_0) > abs(ang_to_2) and sp_ls[0].length_ < sp_ls[2].length_:
    #                 del sp_ls[2]
    #             else:
    #                 print('The middle was the shortest but no edge was removed.')
    #     if len(sp_ls) > 3:
    #         print(f'The semi-pruned list had more three edges remaining on this iteration.')
    #     pruned_ls = sp_ls  # may not be needed
    #     return pruned_ls
    #
    # def list_prune_v4(ls):
    #     while True:
    #         # sp_ls stands for semi-pruned-ls
    #         sp_ls = [i for i in ls if i.fitness == 'good']
    #         if len(sp_ls) <= 3:
    #             break
    #         last_good_index = 0
    #         for index, edge in enumerate(sp_ls):
    #             if index == 0 or index == len(sp_ls) - 1:
    #                 pass
    #             elif edge.length_ > sp_ls[last_good_index].length_ or edge.length_ > sp_ls[index + 1].length_:
    #                 edge.fitness = 'bad'
    #                 # for e in inst.edges.values():
    #                 #     if e == edge:
    #                 #         e.fitness = 'bad'
    #             else:
    #                 last_good_index = index
    #     if len(sp_ls) == 3:
    #         ang_to_0 = helpers.angle(sp_ls[1].node_one, sp_ls[1].node_two, sp_ls[0].node_two)
    #         ang_to_2 = helpers.angle(sp_ls[1].node_one, sp_ls[1].node_two, sp_ls[2].node_two)
    #         # if middle edge is the shortest:
    #         if sp_ls[1].length_ < sp_ls[0].length_ and sp_ls[1].length_ < sp_ls[2].length_:
    #             # if angle to edge_0 in sp_ls is less then angle to edge_2 in sp_ls:
    #             if abs(ang_to_0) < abs(ang_to_2):
    #                 del sp_ls[0]
    #             else:
    #                 del sp_ls[2]
    #         # else if middle edge is the middle length:
    #         elif sp_ls[1].length_ > sp_ls[0].length_ or sp_ls[1].length_ > sp_ls[2].length_:
    #             # comment what these ifs represent
    #             if abs(ang_to_0) < abs(ang_to_2) and sp_ls[0].length_ < sp_ls[2].length_:
    #                 del sp_ls[1]
    #             elif abs(ang_to_0) < abs(ang_to_2) and sp_ls[0].length_ > sp_ls[2].length_:
    #                 del sp_ls[0]
    #             elif abs(ang_to_0) > abs(ang_to_2) and sp_ls[0].length_ > sp_ls[2].length_:
    #                 del sp_ls[1]
    #             elif abs(ang_to_0) > abs(ang_to_2) and sp_ls[0].length_ < sp_ls[2].length_:
    #                 del sp_ls[2]
    #             else:
    #                 print('The middle was the shortest but no edge was removed.')
    #     if len(sp_ls) > 3:
    #         print('The semi-pruned list had more three edges remaining on this iteration.')
    #     elif len(sp_ls) == 2:
    #         print('The semi-pruned list had two edges remaining on this iteration.')
    #     pruned_ls = sp_ls  # may not be needed
    #     return pruned_ls

    def list_prune_v5(ls):
        while True:
            # sp_ls stands for semi-pruned-ls
            sp_ls = [i for i in ls if i.fitness == 'good']
            if len(sp_ls) <= 4:
                break
            last_good_index = 0
            for index, edge in enumerate(sp_ls):
                if index == 0 or index == len(sp_ls) - 1:
                    pass
                # if the edge is the middle in length:
                elif edge.length_ > sp_ls[last_good_index].length_ or edge.length_ > sp_ls[index + 1].length_:
                    # print('Calculating angles.')
                    # if max(abs(sp_ls[last_good_index].angle), abs(sp_ls[index + 1].length)) - \
                    #         min(abs(sp_ls[last_good_index].angle), abs(sp_ls[index + 1].length)) > 120:
                    edge.fitness = 'bad'
                else:
                    last_good_index = index
        if len(sp_ls) == 3:
            ang_to_0 = helpers.angle(sp_ls[1].node_one, sp_ls[1].node_two, sp_ls[0].node_two)
            ang_to_2 = helpers.angle(sp_ls[1].node_one, sp_ls[1].node_two, sp_ls[2].node_two)
            # if middle edge is the shortest:
            if sp_ls[1].length_ < sp_ls[0].length_ and sp_ls[1].length_ < sp_ls[2].length_:
                # if angle to edge_0 in sp_ls is less then angle to edge_2 in sp_ls:
                if abs(ang_to_0) < abs(ang_to_2):
                    del sp_ls[0]
                else:
                    del sp_ls[2]
            # else if middle edge is the middle length:
            elif sp_ls[1].length_ > sp_ls[0].length_ or sp_ls[1].length_ > sp_ls[2].length_:
                # comment what these ifs represent
                if abs(ang_to_0) < abs(ang_to_2) and sp_ls[0].length_ < sp_ls[2].length_:
                    del sp_ls[1]
                elif abs(ang_to_0) < abs(ang_to_2) and sp_ls[0].length_ > sp_ls[2].length_:
                    del sp_ls[0]
                elif abs(ang_to_0) > abs(ang_to_2) and sp_ls[0].length_ > sp_ls[2].length_:
                    del sp_ls[1]
                elif abs(ang_to_0) > abs(ang_to_2) and sp_ls[0].length_ < sp_ls[2].length_:
                    del sp_ls[2]
                else:
                    print('The middle was the shortest but no edge was removed.')
        if len(sp_ls) > 3:
            print('The semi-pruned list had more three edges remaining on this iteration.')
        elif len(sp_ls) == 2:
            print('The semi-pruned list had two edges remaining on this iteration.')
        pruned_ls = sp_ls  # may not be needed
        return pruned_ls

    # populate edge angles
    # eap_start = time.time()
    # edg_count = 0
    for edge in instance.edges.values():
        # edg_count += 1
        # print(f'Populating edge angle: {edg_count}')
        edge.angle = helpers.angle(edge.node_one, instance.average_node, edge.node_two)
    # eap_end = time.time()

    # for each node, list the edges for which it is the origin, and which have good fitness
    good_edges = []
    # node_count = 0
    # pn_start = time.time()
    for node in instance.nodes.values():
        # node_count += 1
        # print(node_count)
        ls = [i for i in instance.edges.values() if i.node_one == node]
        ls.sort(key=lambda x: x.angle)
        # n_start = time.time()
        good = list_prune_v5(ls)  # prune the list of edges
        # n_end = time.time()
        # print(f'Time taken for this node: {n_end - n_start}')
        # print(instance.edges)
        good_edges.extend(good)  # this may not be needed...
    # pn_end = time.time()
    # print(f'Populating edge angles took: {eap_end - eap_start}')
    # print(f'Processing the nodes took: {pn_end - pn_start}')
