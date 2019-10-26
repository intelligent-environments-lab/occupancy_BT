import csv

class mobileDevice:
    def __init__(self, time_array=None, location_array=None, id=None):
        self.time_array = time_array
        # Identifies if the occupant has a BT device
        self.location_array = location_array
        self.id = id
        self.hour = 0
        self.year = 0
        self.month = 0
        self.day = 0


    def __str__(self):
        return str(self.id)

    def __format__(self, format_spec):
        return str(self.id)

    def __eq__(self, other):
        if self.id == other.id:
            return True
        else:
            return False



    def addEntry(self,timeEntry,LocationEntry):
        if self.time_array:
            self.time_array.append(timeEntry)
            self.location_array.append(LocationEntry)
        else:
            self.time_array = []
            self.time_array.append(timeEntry)
            self.location_array = []
            self.location_array.append(LocationEntry)

csvMatrix = []
with open('testcsv.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    dates = []
    list_of_ids = []
    for row in csv_reader:
        csvMatrix.append(row)
        hashed_id = row[3]
        list_of_ids.append(hashed_id)
    list_of_MD = []
    for ele in list_of_ids:
        temp = mobileDevice(None,None,ele)
        list_of_MD.append(temp)


# read through and attach all instances the device is seen
for device in list_of_MD:
    for row in csvMatrix:
        if device.id == row[3]:
            device.addEntry(row[0],row[1])
print(list_of_MD[1].time_array)

