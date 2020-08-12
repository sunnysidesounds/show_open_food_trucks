# SHOW OPEN FOOD TRUCKS
Simple command-line program that will print out a list of food trucks, given a source of food truck data from the
San Francisco government’s API.

## Setup & Install Dependencies For Program
1. Install virtualenv using `pip install virtualenv`
2. Pull down from git or unzip the show_open_food_trucks/ service source code.
3. Get to the root directory of the service `cd /path-to-project/show_open_food_trucks/`
4. Create a new virtual environment `virtualenv venv`
5. Active the new virtual environment `source venv/bin/activate`
6. Install requirements into virtual environment `venv/bin/pip install -r requirements.txt`

## Running Program
1. Run the program by `venv/bin/python show_open_food_trucks.py` or `python show_open_food_trucks.py`
- If there are more than 1 page. you will be prompted to enter a page number to view additional results

## Assumptions / Additional Details:
- Using the ***applicant*** key/value response to sort by alphabetically
- Using the ***start24*** and ***end24*** key/value response to determine if a food truck is open
- As it displays NAME and ADDRESS, I added HOURS that show what hours the food truck is open
- Using python module ***tabulate*** to format the output for the command-line


## Roadmap: (proof-of-concept to fully featured web application)
To turn this proof-of-concept command-line program to a fully featured web application

## Self-Evalution Code Review  (area's of improvment)



## Example Response from Socrata API
```
   [{
      "dayorder":"2",
      "dayofweekstr":"Tuesday",
      "starttime":"10AM",
      "endtime":"6PM",
      "permit":"19MFF-00105",
      "location":"773 MARKET ST",
      "locationdesc":"Pushcart located on Market St. 7 linear feet West of the Fire Hydrant. Must maintain 8 linear feet clearance from Street Artist Booth M22. Reference Street Artist Map #14 (http://www.sfartscommission.org/street_artists_program/maps/index.html)",
      "optionaltext":"Kettle Corn, Funnel Cakes, Lemonade, Beverages, Flan, Hot Dogs, Falafel, Hot and Cold Sandwiches, French Fries, Baklava and Pastries",
      "locationid":"1341056",
      "start24":"10:00",
      "end24":"18:00",
      "cnn":"8746103",
      "addr_date_create":"2011-11-15T13:48:04.000",
      "addr_date_modified":"2011-11-15T13:50:08.000",
      "block":"3706",
      "lot":"096",
      "coldtruck":"N",
      "applicant":"Kettle Corn Star",
      "x":"6011164.82111",
      "y":"2114324.40143",
      "latitude":"37.786160934428665",
      "longitude":"-122.40512731130576",
      "location_2":{
         "type":"Point",
         "coordinates":[
            -122.405127311306,
            37.7861609344287
         ]
      }
   }]
```



