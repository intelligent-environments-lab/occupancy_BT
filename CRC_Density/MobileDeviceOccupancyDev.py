import math
import random
import string

# notes
# OCCUPANCY AS a scale of population e.g. 80% occupants stay an hour
# Duration may be the problem.  have to check all individual for population
# Transition Ratio - Consider a range of values.  Is a function of time. [2-9pm Prime time 2]
# Refer to academic calendar
# People without BT Devices are not staying, no ratio value
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
        self.transitionRatio = 0
        self.DeviceID = "None"
        self.firstHour = False

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
        elif self.counter < 0:
            print("Error: counter is already 0")

    def give_counter(self):
        self.counter = 2

    # Occupant enters the simulated building and is detected if they have a
    # BT devices they are given the transition ratio regardless of detection
    def enterbuilding(self):
        if self.hasMD:
            self.detected = True
            self.onSite = True
        else:
            self.detected = False
            self.onSite = True
        if self.firstHour:
            self.firstHour = False
            self.counter = 0
        else:
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


# generates a 10 letter string may or may not be unique because it is poorly written and may result in duplicates
def generateUniqueID():
    uniqueID = ''
    for x in range(10):
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
    mc = [0]*25
    m = [0]*25
    c = [0]*25
    r = [0]*25
    n = [0]*25
    c_list = [0]*25
    tempMark_list = [0]*25
    captured_list = [0]*25
    recaptured_list = [0]*25

    # first day generate a list of marked occupants for each hour summing up over the days
    for day in range(5):
        if day != 0:
            print("DAY: ", day)
        # not sure if should get rid r = [0] * 24
        # next perform a daily sample
        for hour in range(25):

            if day == 0:
                hour_list = []
                for occupant in week[day][hour]:
                   hour_list.append(occupant)
                # don't know if marked serves a purpose
                marked.append(hour_list)
                tempMark_list[hour] = week[day][hour]
                captured_list[hour] = week[day][hour]
                recaptured_list[hour] = []

            else:
                '''
                # WE ARE HERE IS THE DEBUGING
                # generate c values
                # UNCOMMENT TO PRINT TESTS
                #c_list[hour] = week[day][hour]

                # print("HOUR:",hour)
                # print("MARKED")
                # print_occupants(marked[hour])
                # print("CURRENT")
                # print_occupants(c[hour])
                # print("")
                # generate r values
                #c[hour] = len(c_list[hour])
                #for occupant in c_list[hour]:
                #    if occupant in marked[hour]:
                #        r[hour] = r[hour] + 1
                # marking all found occupants
                #for occupant in week[day][hour]:
                #    if occupant not in marked[hour]:
                #        marked[hour].append(occupant)
                '''
                # list all captures for this iteration
                captured_list[hour] = week[day][hour]
                # find number of recaptures

                # count all recaptures
                for occ in week[day][hour]:
                    if occ in tempMark_list[hour]:
                        recaptured_list[hour].append(occ)
                # mark all non marked occupants
                m[hour] = len(tempMark_list[hour])
                c[hour] = len(captured_list[hour])
                mc[hour] += m[hour]*c[hour]
                r[hour] += len(recaptured_list[hour])
                for occ in week[day][hour]:
                    if occ not in tempMark_list[hour]:
                        tempMark_list[hour].append(occ)
                if hour == 0:
                    print("TEMP LIST HOUR 0")
                    for ele in tempMark_list[hour]:
                        print(ele.id)


            # summing over multiple days

    if debug:
        print("LIST Values")
        print_seperator()
        print("DAY: " + str(day))
        for ele in range(25):
            if(ele == 0):
                print("HOUR " + str(ele))
                print(len(tempMark_list[ele]))
                print(len(captured_list[ele]))
                print(len(recaptured_list[ele]))

    '''for hour in range(25):
        if r[hour] == 0:
            n[hour] = 0
        else:
            n[hour] = mc[hour]/(r[hour]) // 1
            '''
    # convert to lengths sum up over days

    for hour in range(25):
        try:
            n[hour] = mc[hour]/(r[hour]) / 1
        except ZeroDivisionError as error:
            n[hour] = 0
    #  print our n values
    for hour in range(1,25):
        n[hour] = n[hour]/n[0]
    if debug:
        print("MC Array:")
        print(mc)
        print("R Array:")
        print(r)
    print(n)






# actual_occupants is how many occupants should be in the building
# run a simulation on a given list of occupants and returns the number
# Args:
# list_found_occupants - list that holds on occupants detected in the building
# list_unfound_occupants - list that holds all occupants not detected on site
# list_of_ids - holds the ids of all found occupants
# list_of_occupants - a list of the total occupants in a building
# templist - list for switching the found occupants // probably doesn't need to be done this way



def run_simulation(list_of_occupants, occupancy_profile,debug):
    day1 = []
    day2 = []
    day3 = []
    day4 = []
    day5 = []
    week = [day1, day2, day3, day4, day5]

    # iterate for 5 days a week and for every one hour interval in that day
    # print full list of sampled occupants for all days
    if debug:
        print()
        print()
        print("Occupant Breakdown")
        print_seperator()
    for day in range(5):
        # reset all occupants data
        hourlyList = []
        list_found_occupants = []
        list_unfound_occupants = []
        random.shuffle(list_of_occupants)
        for occupant in list_of_occupants:
            occupant.reset_occupant()
        sampled_list = []
        sampled_list = sample_day(.5, list_of_occupants)
        if debug:
            print()
            print_seperator()
            print()
            print("Day " + str(day))
            print("All Occupants on Day: " +str(day))
            print_occupants(sampled_list)
        for hour in range(25):
            # check how many occupants should be in the building at the time interval
            if hour == 0:
                actual_occupants = len(sampled_list)
            else:
                actual_occupants = occupancy_profile[hour]*len(sampled_list)//1
            # check how many occupants are currently in the building
            list_of_ids = []
            for occupant in list_found_occupants:
                list_of_ids.append(occupant.id)

            for occupant in sampled_list:
                # make sure occupant is not already in the list
                if occupant.onSite and occupant.id not in list_of_ids:
                    list_found_occupants.append(occupant)
                else:
                    list_unfound_occupants.append(occupant)
            # if the current number occupants is less than the occupancy profile add occupants
            # until occupancy profile is reached
            while len(list_found_occupants) < actual_occupants:
                if hour == 0:
            # Discount the first hour as it is for summing of the day
                    list_unfound_occupants[0].hourFirst = True
                list_unfound_occupants[0].enterbuilding()
                list_found_occupants.append(list_unfound_occupants[0])
                list_unfound_occupants = list_unfound_occupants[1:]
            # CRC analysis goes here or Max devices
            # DISPLAYS THE HOUR print("CRC Calculated for Hour:", hour + 1)
            # print_occupants_detailed(list_found_occupants)
            # if a mobile device was detected append it to the proper time slot
            if debug:
                hourlyList.append(list_found_occupants)
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
        # print Hourly Breakdown
        if debug:
            print()
            for x in range(25):
                if(x == 0 or x == 1 or x == 2):
                    print()
                    print("Hour " + str(x))
                    print_occupants(hourlyList[x])
                    print("WEEK")
                    print_occupants(week[day][x])
                    print
    CRC(week, occupancy_profile, len(sampled_list))
    return


def sample_day(sample_ratio, occupant_list):
    counter = 0
    num_day_sample = len(occupant_list)*sample_ratio - 1
    out_list = []
    while counter <= num_day_sample:
        temp_occ = random.choice(occupant_list)
        if temp_occ not in out_list:
            out_list.append(temp_occ)
            counter += 1
    return out_list


# PRINT FUNCTIONS
# prints a list of occupants and there device id
def print_occupants(list_of_occupants):
    for occupant in list_of_occupants:
        print("Occupant {} has Device {}".format(occupant, occupant.DeviceID))


# prints a list of occupants and there device id
def print_occupants_detailed(list_of_occupants):
    for occupant in list_of_occupants:
        print("Occupant {} has Device {} Counter is {}".format(occupant, occupant.DeviceID, str(occupant.counter)))


# prints seperator
def print_seperator():
    print("-----------------------------------------------------------------------------------------------------------")


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


# runs program step by step with print functions
def debug():
    # Array of Populations To Be Tested

    test_populationList = [10]
    test_ratioList = [.7]
    occupancy_profile = [.5, .01, .01, .01, .01, .01, .01, .1, .2, .7, .7, .7, .7,
                         .5, .7, .7, .7, .7, .3, .1, .1, .1, .1, .01, .05]

    list_of_occupants = []

    # perform all CRC operations for every population and ratio given
    for population in test_populationList:
        for ratio in test_ratioList:
            # create_occupants works
            list_of_occupants = create_occupants(population, ratio)
            random.shuffle(list_of_occupants)
            # set a random number of occupants to found depending on the occupancy profile and time
            # test if the right population and BT Ratio are being printed out
            print("OCCUPANT TEST")
            print_seperator()
            print_occupants(list_of_occupants)
            list_of_occupants = run_simulation(list_of_occupants, occupancy_profile,True)


def main():
    # Array of Populations To Be Tested
    PopulationList = [500, 1000, 1500, 2000]
    ratioList = [.05, .1, .3, .5, .6, .7, .8, .9]

    test_populationList = [1000]
    test_ratioList = [.7]
    occupancy_profile = [.5, .01, .01, .01, .01, .01, .01, .1, .2, .7, .7, .7, .7,
                         .5, .7, .7, .7, .7, .3, .1, .1, .1, .1, .01, .05]

    list_of_occupants = []

    # perform all CRC operations for every population and ratio given
    for population in test_populationList:
        for ratio in test_ratioList:
            # create_occupants works
            list_of_occupants = create_occupants(population, ratio)
            random.shuffle(list_of_occupants)
            # set a random number of occupants to found depending on the occupancy profile and time
            list_of_occupants = run_simulation(list_of_occupants, occupancy_profile,False)

debug()



