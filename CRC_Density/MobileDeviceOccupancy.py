import math
import random
import string
class Occupant:
    # Our Representation of a simulated person

    def __init__(self, ida=0, onSite=False, hasMD=False, detected=False):
        self.id = ida
        # Identifies if the occupant has a BT device
        self.hasMD = hasMD
        # boolean onSite refers to whether or not the occupant is in the building being observed#
        self.onSite = onSite
        # boolean that shows whether or not the occupant was located#
        self.detected = detected
        self.counter = 0
        # Number of Hours occupant spends detected before leaving the building
        self.transitionRatio = 1
        self.DeviceID = "None"

    def __str__(self):
        return str(self.id)

    def __format__(self, format_spec):
        return str(self.id)

    def __eq__(self, other):
        if self.id == other.id:
            return True
        else:
            return False

    # assign the occupants mobile device a unique id
    def assigndevice(self, string):
        if self.hasMD:
            self.DeviceID = string
        else:
            print("no mobile device on this occupant")

    # Counter value keeps track of how long occupants are supposed to stay in buildings for after they are found
    def lowercounter(self):
        if self.counter != 0:
             self.counter = self.counter-1
        else:
            print("Error: counter is already 0")

    def give_counter(self):
        self.counter = self.transitionRatio

    # Occupant enters the simulated building and is detected if they have a
    # BT devices they are given the transition ratio regardless of detection
    def enterbuilding(self):
        if self.hasMD:
            self.detected = True
            self.onSite = True
        else:
            self.detected = False
            self.onSite = True
        self.give_counter()

    # Simulates 1 hour time interval (This number could be changed and isn't attached to anything physically),
    # removes occupant if they are past the transition ratio, otherwise it lowers the counter
    def simulateinterval(self):
        # leave the building
        self.lowercounter()
        if self.counter <= 0:
            self.onSite = False
            self.detected = False

    # removes the occupant from the site and sets counter to 0
    def reset_occupant(self):
        # leave the building
        self.onSite = False
        self.detected = False
        # reset counter
        self.counter = 0


# generates a 4 letter string may or may not be unique because it is poorly written
def generateUniqueID():
    uniqueID = ''

    for x in range(4):
        uniqueID = uniqueID + random.choice(string.ascii_uppercase)
    return uniqueID


# generate our occupants given a population and, bt_ratio
def create_occupants(population, bt_ratio):
    list_of_occupants = []
    # 1 based indexing im sorry, i'm leaving 0 open for errors
    id_counter = 1
    # might want to make this something other than an integer
    device_counter = 1
    # TODO: LOW POPULATION or LOW BT RATIO CASE +1 might not work
    total_number_devices = (bt_ratio*population//1)+1
    for person in range(population):
        if device_counter < total_number_devices:
            place_holder_occupant = Occupant(id_counter, False, True, False)
            # give the occupant a mobile device
            place_holder_occupant.assigndevice(generateUniqueID())
            device_counter = device_counter + 1

        else:
            # do not give the occupant a mobile device
            place_holder_occupant = Occupant(id_counter)
        id_counter = id_counter+1
        list_of_occupants.append(place_holder_occupant)

    return list_of_occupants


# METHODOLOGIES
# takes a weeks worth of occupants with mobile devices and runs a CRC analysis yielding an occupancy profile in the
# form of a list
def CRC(week, occupancy_profile, population):
    marked = []
    print(marked)

    day_counter = 0
    hour_counter = 0
    mc = [0]*24
    m = [0]*24
    c = [0]*24
    r = [0]*24
    n = [0]*24
    c_list = [0]*24
    # first day generate a list of marked occupants for each hour summing up over the days
    for day in range(5):
        if day!= 0:
            print("DAY: ", day)
        # not sure if should get rid r = [0] * 24
        for hour in range(24):
            if day == 0:
                hour_list = []
                for occupant in week[day][hour]:
                   hour_list.append(occupant)
                marked.append(hour_list)
            else:
                # generate c values
                # UNCOMMENT TO PRINT TESTS
                c_list[hour] = week[day][hour]
                # print("HOUR:",hour)
                # print("MARKED")
                # print_occupants(marked[hour])
                # print("CURRENT")
                # print_occupants(c[hour])
                # print("")
                # generate r values
                c[hour] = len(c_list[hour])
                for occupant in c_list[hour]:
                    if occupant in marked[hour]:
                        r[hour] = r[hour] + 1
                # marking all found occupants
                for occupant in week[day][hour]:
                    if occupant not in marked[hour]:
                        marked[hour].append(occupant)

            m[hour] = len(marked[hour])
            #summing over multiple days
            mc[hour] = mc[hour] + (m[hour] * c[hour])
    for hour in range(24):
        if(r[hour] == 0):
            n[hour] = 0
        else:
            n[hour] = mc[hour]/(r[hour])//1
    print(n)







# actual_occupants is how many occupants should be in the building
# run a simulation on a given list of occupants and returns the number
# Args:
# list_found_occupants - list that holds on occupants detected in the building
# list_unfound_occupants - list that holds all occupants not detected on site
# list_of_ids - holds the ids of all found occupants
# list_of_occupants - a list of the total occupants in a building
# templist - list for switching the found occupants // probably doesn't need to be done this way



def run_simulation(list_of_occupants, occupancy_profile):
    day1 = []
    day2 = []
    day3 = []
    day4 = []
    day5 = []
    week = [day1, day2, day3, day4, day5]


    # iterate for 5 days a week and for every one hour interval in that day
    for day in range(5):
        # reset all occupants data
        list_found_occupants = []
        list_unfound_occupants = []
        random.shuffle(list_of_occupants)
        for occupant in list_of_occupants:
            occupant.reset_occupant()

        for hour in range(24):
            # check how many occupants should be in the building at the time interval
            actual_occupants = occupancy_profile[hour]*len(list_of_occupants)//1
            # check how many occupants are currently in the building
            list_of_ids = []
            for occupant in list_found_occupants:
                list_of_ids.append(occupant.id)

            for occupant in list_of_occupants:
                # make sure occupant is not already in the list
                if occupant.onSite and occupant.id not in list_of_ids:
                    list_found_occupants.append(occupant)
                else:
                    list_unfound_occupants.append(occupant)
            # if the current number occupants is less than the occupancy profile add occupants
            # until occupancy profile is reached
            while len(list_found_occupants) < actual_occupants:
                list_unfound_occupants[0].enterbuilding()
                list_found_occupants.append(list_unfound_occupants[0])
                list_unfound_occupants = list_unfound_occupants[1:]
            # CRC analysis goes here or Max devices
            # DISPLAYS THE HOUR print("CRC Calculated for Hour:", hour + 1)
            # print_occupants_detailed(list_found_occupants)
            # if a mobile device was detected append it to the proper time slot
            crc_list = []
            for occupant in list_found_occupants:
                if occupant.hasMD:
                    crc_list.append(occupant)
            week[day].append(crc_list)

        # update for the stayed occupants for next iteration
            templist = []

            for occupant in list_found_occupants:
                # lower the counter for each occupant in the list
                occupant.simulateinterval()
                # add them to the correct list
                if occupant.onSite:
                    templist.append(occupant)
                else:
                    list_unfound_occupants.append(occupant)
            list_found_occupants = templist
    CRC(week, occupancy_profile, len(list_of_occupants))

# PRINT FUNCTIONS
# prints a list of occupants and there device id
def print_occupants(list_of_occupants):
    for occupant in list_of_occupants:
        print("Occupant {} has Device {}".format(occupant,occupant.DeviceID))


# prints a list of occupants and there device id
def print_occupants_detailed(list_of_occupants):
    for occupant in list_of_occupants:
        print("Occupant {} has Device {} Counter is {}".format(occupant,occupant.DeviceID,str(occupant.counter)))


def print_2d_occupant_matrix(week):
    day_counter = 0
    for day in week:
        day_counter += 1
        hour_counter = 0
        print("Day", day_counter)
        for hour in day:
            hour_counter += 1
            print("Hour", hour_counter)
            for occupant in hour:
                print("Occupant {} has Device {}".format(occupant, occupant.DeviceID))


def main():
    # Array of Populations To Be Tested
    PopulationList = [500,1000,1500,2000]
    ratioList = [.05, .1, .3, .5, .6, .7, .8, .9]

    test_populationList = [100]
    test_ratioList = [.4]
    occupancy_profile = [.01, .01, .01, .01, .01, .01, .1, .2, .7, .7, .7, .7,
                         .5, .7, .7, .7, .7, .3, .1, .1, .1, .1, .01, .05]
    list_of_occupants = []

    # perform all CRC operations for every population and ratio given
    for population in test_populationList:
        for ratio in test_ratioList:
            list_of_occupants = create_occupants(population, ratio)

            random.shuffle(list_of_occupants)
            # set a random number of occupants to found depending on the occupancy profile and time
            list_of_occupants = run_simulation(list_of_occupants, occupancy_profile)

main()

