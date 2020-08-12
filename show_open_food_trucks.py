#!/usr/bin/env python

import requests
import datetime
import calendar
import math
import sys
from tabulate import tabulate


class FoodTruck(object):
    def __init__(self, data):
        # explicit mapping of food truck json to object
        self.dayorder = None if 'dayorder' not in data else int(data['dayorder'])
        self.dayofweekstr = None if 'dayofweekstr' not in data else data['dayofweekstr']
        self.starttime = None if 'starttime' not in data else data['starttime']
        self.endtime = None if 'endtime' not in data else data['endtime']
        self.permit = None if 'permit' not in data else data['permit']
        self.location = None if 'location' not in data else data['location']
        self.locationdesc = None if 'locationdesc' not in data else data['locationdesc']
        self.optionaltext = None if 'optionaltext' not in data else data['optionaltext']
        self.locationid = None if 'locationid' not in data else int(data['locationid'])
        start24 = '23:59' if data['start24'] == '24:00' else data['start24']  # since 24:00 is not a time, remove 1 mins
        self.start24 = None if 'start24' not in data else datetime.datetime.strptime(start24, "%H:%M")
        end24 = '23:59' if data['end24'] == '24:00' else data['end24']  # since 24:00 is not a time, remove 1 mins
        self.end24 = None if 'end24' not in data else datetime.datetime.strptime(end24, "%H:%M")
        self.cnn = None if 'cnn' not in data else int(data['cnn'])
        self.addr_date_create = None if 'addr_date_create' not in data else data['addr_date_create']
        self.addr_date_modified = None if 'addr_date_modified' not in data else data['addr_date_modified']
        self.block = None if 'block' not in data else data['block']
        self.lot = None if 'lot' not in data else data['lot']
        self.coldtruck = None if 'coldtruck' not in data else data['coldtruck']
        self.applicant = None if 'applicant' not in data else data['applicant']
        self.x = None if 'x' not in data else data['x']
        self.y = None if 'y' not in data else data['y']
        self.latitude = None if 'latitude' not in data else data['latitude']
        self.longitude = None if 'longitude' not in data else data['longitude']
        self.location_2 = None if 'location_2' not in data else data['location_2']


class FoodTruckFinder(object):

    def __init__(self, url_source):
        self.url = url_source
        self.open_food_trucks = []
        self.open_food_trucks_pagination = {}
        self.current_dayofweek = calendar.day_name[datetime.datetime.today().weekday()]
        self.current_time = datetime.datetime.today()
        self.truck_per_page = 10
        self.__build_open_food_trucks()

    def get_open_food_trucks(self, page=1):
        """
        Entry point / Main method that gets, builds and displays results
        :param page:
        :return:
        """
        self.__diplay_food_trucks_list(page)

    def get_current_dayofweek(self):
        """
        Get current string day of week (i.e Tuesday)
        :return:
        """
        return self.current_dayofweek

    def get_current_time(self):
        """
        Get current time in format HH:MM
        :return:
        """
        return self.current_time

    def get_total_open_trucks(self):
        """
        Get total number of trucks
        :return:
        """
        return len(self.open_food_trucks)

    def get_total_pages(self):
        """
        Determine the total number of pages (shift + 1 for 1 index)
        :return:
        """
        if len(self.open_food_trucks) > self.truck_per_page:
            pages = math.ceil(len(self.open_food_trucks) / self.truck_per_page) + 1
        else:
            pages = 2
        return pages

    def __build_open_food_trucks(self):
        """
        Private method: Build and paginate food truck results.
        :return:
        """
        self.__build_food_trucks_list()
        self.__paginate_food_trucks_list()

    def __paginate_food_trucks_list(self):
        """
        Private method:This create a paginated dictionary with list of list for the tabulate module formatting
        :return:
        """
        # TODO: Need to improve time complexity O(n2)
        pages = [self.open_food_trucks[x:x+self.truck_per_page] for x in range(0, len(self.open_food_trucks), self.truck_per_page)]

        for i in range(len(pages)):
            truck_list = pages[i]
            self.open_food_trucks_pagination[i + 1] = []
            for j in range(len(truck_list)):
                truck = truck_list[j]
                self.open_food_trucks_pagination[i + 1].append([truck.applicant, truck.location, "{start} - {end}".format(start=truck.starttime, end=truck.endtime)])


    def __diplay_food_trucks_list(self, page):
        """
        Private method: Using the tabulate module. This prints out a grid of alphabetically sorted food trucks based on page
        :return:
        """
        truck_list = self.open_food_trucks_pagination[page]
        print(tabulate(truck_list, headers=['NAME', 'ADDRESS', 'HOURS']))
        print("\nPage: {startPage} of {endPage} \n".format(startPage=page, endPage=self.get_total_pages()-1))

    def __insert_food_truck(self, truck):
        """
        Private method: This inserts a FoodTruck object into a list while maintaining sorted alphabetical order of list
        :param truck:
        :return:
        """
        if len(self.open_food_trucks) == 0:
            self.open_food_trucks.append(truck)
        else:
            for index, food_truck in enumerate(self.open_food_trucks):
                if food_truck.applicant > truck.applicant:
                    self.open_food_trucks.insert(index, truck)
                    break

    def __build_food_trucks_list(self):
        """
        Private method: This makes the http GET requests and builds a list of open FoodTrucks
        :return:
        """
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            if response.status_code == 200:
                for item in response.json():
                    food_truck = FoodTruck(item)
                    # check if incoming food truck day of week, matches today's day of the week
                    if food_truck.dayofweekstr == self.current_dayofweek:
                        # next check if the food truck is open by matching incoming food truck hours with current hour
                        if self.current_time.hour >= food_truck.start24.hour and self.current_time.hour <= food_truck.end24.hour:
                            self.__insert_food_truck(food_truck)

        except requests.exceptions.HTTPError as e:
            print(e.response.text)


if __name__ == '__main__':

    food_trucks = FoodTruckFinder("http://data.sfgov.org/resource/bbb8-hzi6.json")

    print("\n############## FOOD TRUCK FINDER ##############")
    print(food_trucks.get_current_time().strftime('  Open food trucks for %b %d, %Y at %H:%M'))
    print("###############################################\n")

    # By default display first page
    food_trucks.get_open_food_trucks(1)
    # If more than 1 page create a loop that prompts for each page, until you hit enter to quit
    if food_trucks.get_total_pages() - 1 > 1:
        while True:
            try:
                page_number = int(input("Enter page number?, [ENTER] to quit "))
                if not page_number or page_number < 0:
                    break
                food_trucks.get_open_food_trucks(page_number)

            except Exception as e:
                print("Exiting program")
                break
