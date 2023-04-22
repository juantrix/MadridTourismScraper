# MadridTurismScraper

## To run the scraper, follow these steps:

Linux(tested):

**1- Open a terminal and navigate to the root of the repository**

**2- Create a Python virtual environment**
```python3 -m venv env```

**3- Activate the virtual environment**
```source env/bin/activate```

**4- Install the dependencies**
```pip install -r requirements```

**5- Run the scraper**
```sh scraper.sh```

---

Windows(not tested):

**1- Open a terminal and navigate to the root of the repository**

**2- Create a Python virtual environment**
```python -m venv env```

**3- Activate the virtual environment**
```env/Scripts/activate```

**4- Install the dependencies**
```pip install -r requirements```

**5- Run the scraper**
```sh scraper.sh```

---
The .sh file will execute the scraper, save the data in the database (which will be generated in the corresponding directory) and immediately the tests will be executed

The database will be generated on this location ```turismomadrid/turismomadrid/db``` 


## Technologies

For this challenge, in addition to ```scrapy```, I decided to use ```sqlalchemy``` as an orm to facilitate interaction with the database. I also used ```SQLite``` to create the database locally. And finally create a sh file to run the scraper and tests correctly and make it easier to use.



## Development decisions

I started looking at the web page and doing the indicated path, at that moment I realized that I was going to need 4 tables for the 4 layers of the page. After designing how the database would be, I started to create it with SQLalchemy.

Then I started to create the scraper, I decided to use xpath to make the selections because it is what I have used the most and I know it the most. When I was in the middle of the scrpaer I thought about how to load the data into the database, two options occurred to me.
One was at the end of the whole scraper to load the data in the database, and the other was to load the data at each step. I decided to do it in each step so that if there is an error at least I collect some information before and also in case the information of the page is greater in the future, the database will be loaded procedurally and would not wait to have all the data to be loaded.

After all, once everything was working fine I decided to do tests, I chose to make a file for each table in the database and test the information inside. Then to finish, I made a .sh file to start the scrpaer and make it easier to use.
