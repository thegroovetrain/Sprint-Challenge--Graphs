from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

map_graph = {}
unexplored = 1

# while there are still rooms to explore
while unexplored > 0:
    print(f'entering room {player.current_room.id}')
    # add the current room's data to the map graph
    room_id = player.current_room.id
    if room_id not in map_graph.keys():
        print('first time entering this room!')
        map_graph[room_id] = {}
    exits = player.current_room.get_exits()
    unexplored_exits = []
    for exit in exits:
        if exit not in map_graph[room_id].keys():
            map_graph[room_id][exit] = '?'
            unexplored += 1
        if map_graph[room_id][exit] == '?':
            unexplored_exits.append(exit)

    # update unexplored to be equal to the total number of '?'s on the map graph
    unexplored = 0
    for r in map_graph.keys():
        for v in map_graph[r].values():
            if v == '?':
                unexplored += 1

    print(f'there are currently {unexplored} known unexplored rooms\n')

    print(f'exits: {exits} \nunexplored exits: {unexplored_exits}')
    # if dead end (no unexplored paths in current room)
    if len(unexplored_exits) == 0:
        # break
        # walk back to nearest room with an unexplored path
        queue = []
        queue.append([room_id])
        visited = set()
        while len(queue) > 0:
            path = queue.pop(0)
            current = path[-1]
            print('path:', path, '| current:', current)
            if current not in visited:
                visited.add(current)
                if current == '?':
                    # ok we found an unexplored path so lets convert this to a list of directions
                    print('found unexplored path!')
                    for r in path[1:-1]:
                        direction = None
                        for d, v in map_graph[player.current_room.id].items():
                            if v == r:
                                direction = d
                                break
                        print(f'traveling {direction}')
                        traversal_path.append(direction)
                        player.travel(direction)
                    break
                else:
                    # get known neighbors of current room id
                    neighbors = map_graph[current].values()
                    print('neighbors:', neighbors)
                    for neighbor in neighbors:
                        new_path = [v for v in path]
                        new_path.append(neighbor)
                        queue.append(new_path)

    # otherwise
    else:
        print('There are unexplored directions in this room!')
        # choose a random unexplored direction
        direction = unexplored_exits[random.randint(0, len(unexplored_exits) - 1)]
        print(f'about to travel {direction}')
        # travel in that direction
        traversal_path.append(direction)
        player.travel(direction)
        # add this new information to the map graph
        new_room_id = player.current_room.id
        map_graph[room_id][direction] = new_room_id
        reverse_direction = 's' if direction == 'n' else 'n' if direction == 's' else 'e' if direction == 'w' else 'w'
        if new_room_id not in map_graph.keys():
            print('first time entering this room!')
            map_graph[new_room_id] = {}
        map_graph[new_room_id][reverse_direction] = room_id
    print('CURRENT MAP GRAPH:', map_graph)
    print('CURRENT TRAVERSAL PATH:', traversal_path)
    print('CURRENT ROOM:', player.current_room.id)



print('\n\nfinal path:', traversal_path)




# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
