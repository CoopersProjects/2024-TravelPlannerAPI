# Cooper Scott T2A2 API Assignment 
## Travel Planner API

Link to Github: https://github.com/CoopersProjects/2024-TravelPlannerAPI
`Insomnia` or `Postman` is required to replicate the running of this application.

### R1:	Identification of the problem you are trying to solve by building this particular app.
The problem I am trying to solve by creating this application is the unorganised nature of travel. This looks like: missing events due to schedule disorganisation, or things getting lost due to all the separate documentation or bookings required. For the average person, this process is often stressful and multifaceted, and takes a lot of planning to form an efficient itinerary.

### R2:	Why is it a problem that needs solving?
People travel for many reasons (some being essential), including holidays, business/work trips, visiting family/friends or even things such as studying or work in general. Due to the multifaceted nature of travel, there are a lot of decisions as well as the associated time required to investigate, decide and then purchase. As well, due to separate documentation and bookings, things can easily get lost, which costs not only time, but can also cost money. These problems are avoidable via the implementation of my app which allows users to create "trips" and add all the important information associated with the trip such as accommodation, destination, trip dates, transportation and activities. All of this information is stored within the user's created 'trip' and is then easy to read, create and keep organised. 


### R3:	Why have you chosen this database system. What are the drawbacks compared to others?

When selecting a database to use in the creation of your application, it is important to think about the pros and cons of each one, and which one may be the best to use in your project. 

An example of a popular database is MongoDB, which is a NoSQL database type. In terms of scalability and flexibility, this type of database is better compared to that of a relational database like postgreSQL, allowing faster flow of data traffic. These databases are also paired well with JSON data types and, as previously stated, works well on the scalability side.

I have chosen to use postgreSQL in my project. PostgreSQL was selected for a few reasons, one of them being it's adherence to the ACID principles, which ensures more data integrity and reliability in my database; particularly with user access regarding personal information and trip plans. Another reason being the learning curve being more achieveable in the given time, rather than learning, for example, MongoDB. PostgreSQL provides an extensive array of data types and advanced features, including JSONB, which allows for adaptability to evolving data structures while ensuring optimal performance. 

The SQL querying features of PostgreSQL are powerful, facilitating efficient data retrieval and analysis for activities and destinations such as searching for lodging and studying user behaviour, if required. PostgreSQL's excellent backing for geospatial data, and for an example, if coupled with the PostGIS extension, enhances location-based functionalities such as proximity searches and route planning, which my application could be scaled to use. I believe due to these reasons that postgreSQL is the more suitable choice for my travel planner project.

### R4:	Identify and discuss the key functionalities and benefits of an ORM.

ORM frameworks have become indispensable in contemporary software development as they bridge the gap between object-oriented programming and relational databases. By simplifying the process of database interaction, developers can utilise their primary programming language instead of relying solely on SQL. This not only leads to more comprehensible and sustainable code but also enhances productivity by allowing developers to focus on the business logic rather than the complexities of the database.

One of the key advantages of ORMs is their ability to ensure consistent data management across different applications, thereby preserving the integrity of the data model. Additionally, they facilitate smooth transitions between various databases, which is crucial for scalability and future migrations in the creation of a web-application. Many ORMs also offer advanced features like lazy loading or many extensive library features, further improving application performance and reliability.

In conclusion, ORMs refine database operations, leading to efficient and organised code outcomes. They serve as a vital abstraction layer that simplifies interactions with databases and enhances the scalability and maintainability of applications. As a result, they have become essential tools in the field of software development.

### R5: API Endpoints
`POST "/auth/register"`

Function: Registers a user within the database.

Input: 
    - `username` string: A user's username, maximum of 50 characters. Will be unique and not-null.
    - `email` string: A user's associated email, maximum of 100 characters. Will also be unique and not-null.
    - `password` string: A user's password, maximum of 50 characters. Cannot be null.

`POST "/auth/login"`

Function: Allows a registered user to log-in and returns authentication token.

Input:
    - `email` Uses the registered email.
    - `password` Uses the registered password.

`DELETE "/trip/delete/<int:id>"`

Function: Deletes a single, specified, trip. JWT is required.

Returns: 
    - "({'message': f'Successfully deleted trip {id}'}), 200"

`PUT "/trip/update/<int:id>"`

Function: Updates an existing trip. Requires a JWT token.

Input: 
    - `user_id` User ID required.
    - `destination_id` Valid Destination ID required.
    - `start_date_str` Enter start date of trip (YYYY-MM-DD format, otherwise, error.)
    - `end_date_str` Enter end date of trip (YYYY-MM-DD format, otherwise, error.)
    - `budget` Enter budget for trip (as a float, otherwise error.)

`GET "/trip/read/<int:id>"`

Function: Retrieves existing details about a specific trip.

Response: Shows information about a specific trip. If the trip doesn't exist, return error.

`GET "/trip/read"`

Function: Retrieves exisiting details about all available trips.

Resonse: Shows information about trips.

`POST "/trip/create"`

Function: Creates a new trip. JWT required.

Input: (If not all fields filled, return error.)
    - `user_id` User ID required.
    - `destination_id` Valid Destination ID required.
    - `start_date_str` Enter start date of trip (YYYY-MM-DD format, otherwise, error.)
    - `end_date_str` Enter end date of trip (YYYY-MM-DD format, otherwise, error.)
    - `budget` Enter budget for trip (as a float, otherwise error.)


`POST "/destination/create"`

Function: Creates a new destination. JWT required.

Input: 
    - `name` String: Name of destination. Required.
    - `description` Brief description of destination. Not required.
    - `location` String: Location of said destination. Required field.
    - `climate_id` Climate type of destination (1-5 only, otherwise error. Key: 1 - Tropical, 2 - Temperate, 3 - Dry, 4 - Polar, 5 - Continental.)

`DELETE "/destination/delete/<int:id>"`

Function: Deletes an existing destination. JWT required.

Response: 
    - If valid destination, returns: "({'message': f'Successfully deleted destination with id {id}'}), 200"
    - Otherwise will return, "({'error': 'Destination not found.'}), 404"

`PUT "/destination/update/<int:id>"`

Function: Updates an existing destination. JWT required.

Input: 
    - `name` String: Name of destination.
    - `description` Brief description of destination.
    - `location` String: Location of said destination. 
    - `climate_id` Climate type of destination (1-5 only, otherwise error. Key: 1 - Tropical, 2 - Temperate, 3 - Dry, 4 - Polar, 5 - Continental.)

`GET "/destination/read"`

Function: Retrieves all exisiting destinations.

Response: Shows all current destinations.

`GET "/destination/read/<int:id>"`

Function: Retrieves a single existing location by ID.

Response: Shows existing trip with specified ID. If ID is not valid, return error.


`POST "/transport/create"`

Function: Creates a new transportation event. JWT required. 

Input: (None can be null).
    - `trip_id` Enter a valid trip_id. If not a valid id, return error.
    - `transport_type_id` Enter a valid transport_type_id. If not valid id, return error (Options include: 1 - Car, 2 - Bus, 3 - Plane, 4 - Train, 5 - Boat, 6 - Taxi, 7 - Walk, 8 - Bike.).
    - `arrival_time` Enter arrival time (YYYY-MM-DD HH:MM:SS format, otherwise error.)
    - `departure_time` Enter departure time (YYYY-MM-DD HH:MM:SS format, otherwise error)
    - `arrival_location` String: Enter arrival location
    - `departure_location` String: Enter the departure location.
    - `cost` Enter the cost of transport.

`DELETE "/transport/delete/<int:id>"`

Function: Deletes an existing transport event. JWT required. 

Response: 
    - If the transport event is valid, returns: ({'message': f'Transportation with ID {id} deleted successfully.'}).
    - If the id does not exist, returns error.

`PUT "/transport/update/<int:id>"`

Function: Updates a sepcific transport event. JWT required.

Input: (Only updates changed fields.)
    - `trip_id` Enter a valid trip_id. If not a valid id, return error.
    - `transport_type_id` Enter a valid transport_type_id. If not valid id, return error (Options include: 1 - Car, 2 - Bus, 3 - Plane, 4 - Train, 5 - Boat, 6 - Taxi,  7 - Walk, 8 - Bike.).
    - `arrival_time` Enter arrival time (YYYY-MM-DD HH:MM:SS format, otherwise error.)
    - `departure_time` Enter departure time (YYYY-MM-DD HH:MM:SS format, otherwise error)
    - `arrival_location` String: Enter arrival location
    - `departure_location` String: Enter the departure location.
    - `cost` Enter the cost of transport.

`GET "/transport/read"`

Function: Retrieves all available transport events.

Response: Shows all transport events.

`GET "/transport/read/<int:id>"`

Function: Retrieves a transport event by ID.

Response:
    - If valid ID, shows information on the specifically requested transport event.
    - If ID does not exist, returns error.

`POST "/accommodation/create"`

Function: Create a new accommodation instance for a trip. JWT required.

Input: 
    - `name` String: Name of the accommodation. (Required field).
    - `address` String: Address of the accommodation. (Required field).
    - `check_in` Check in date of accommodation (YYYY-MM-DD formatting, not a required field)
    - `check_out` Check out date of accommodation (YYYY-MM-DD formatting, not a required field)
    - `cost_per_night` Cost per night at the accommodation. (required field).
    - `trip_id` Trip ID that the accommodation is associated with. (Required field).

`PUT "/accommodation/update/<int:id>"`

Function: Update an existing accommodation instance. JWT required.

Input: 
    - `name` String: Name of the accommodation. 
    - `address` String: Address of the accommodation. 
    - `check_in` Check in date of accommodation (YYYY-MM-DD format).
    - `check_out` Check out date of accommodation (YYYY-MM-DD format).
    - `cost_per_night` Cost per night at the accommodation. 
    - `trip_id` Trip ID that the accommodation is associated with. 

`DELETE "/accommodation/delete/<int:id>"`

Function: Deletes an existing accommodation instance. JWT required. 

Response: 
    - If the accommodation instance ID is valid, returns: ({'message': f'Accommodation with ID {id} deleted successfully.'}).
    - If the id does not exist, returns error.


`GET "/accommodation/read"`

Function: Retrieves all available accommodation instances.

Response: Shows all accommodation instances.


`GET "/accommodation/read/<int:id>"`

Function: Retrieves an accommodation event by ID.

Response:
    - If valid ID, shows information on the specifically requested accommodation instance.
    - If ID does not exist, returns error.

`POST "/activity/create"`

Function: Create a new activity for a trip. JWT required.

Input: 
    - `name` String: Name of activity. (required field).
    - `description` Description of activity.
    - `cost` Cost of the specific activity. (Float value, if not, error).
    - `trip_id` Associated trip ID that the user would like to add an activity to (required field).

`DELETE "/activity/delete/<int:id>"`

Function: Deletes an existing activity. JWT required. 

Response: 
    - If the activity ID is valid, returns: ({'message': f'Activity with ID {id} deleted successfully.'}).
    - If the id does not exist, returns error.

`PUT "/activity/update/<int:id>"`

Function: Update an existing activity within a trip. JWT required.

Input: 
    - `name` String: Name of activity.
    - `description` Description of activity.
    - `cost` Cost of the specific activity. (Float input, if not, error).
    - `trip_id` Associated valid trip ID that the user would like to add an activity to.

`GET "/activity/read"`

Function: Retrieves all available activities.

Response: Shows all activities.


`GET "/activity/read/<int:id>"`

Function: Retrieves an activity by ID.

Response:
    - If valid ID, shows information on the specifically requested activity.
    - If ID does not exist, returns error.


### R6:	An ERD for your app
Here is my ERD:
![Travel Planner API ERD](/Resources/Travel%20Planner%20ERD.png)

### R7:	Detail any third party services that your app will use

#### `PostgreSQL`:
- PostgreSQL is the database I have chosen, and is the backbone of my project. PostgreSQL is a relational database type that allows data to be stored while being compatible with the Flask framework. 

#### `Flask`:
- I will be using Flask to create my web application. Flask is a Python framework that lets a developer use many libraries and extensions within the same service, allowing the creation of APIs in an efficient matter. 

#### `SQLAlchemy`:
-  SQLAlchemy is a Object Relational Mapper (ORM) that offers many services to a developer creating an application. It will allow me to interact with my PostgreSQL database while using python and flask, and will be used to create and design models in my application.

#### `Flask-JWT-Extended`:
- Flask JWT extended is a Flask extension that allows an extra layer of security. My project will use JWT tokens to grant access to authorisation features such as logging in, and making changes to existing data. It also allows my application to verify tokens, adding security. 

#### `Psycopg2`:
- Psycopg2 is a service that connects PostgreSQL to my python application. It allows me to interact with the database and provides a Python DB-API 2.0-compliant interface for developers.

#### `Bcrypt`:
- Bcrypt is a service that works in conjunction with Flask, allowing me to add security into my project by hashing passwords without storing the password itself within the database. 

#### `Marshmallow`:
- Marshmallow is a service that allows me to work with schemas to validate input data, and serialises/deserialises data when needed and works closely with SQLAlchemy, allowing developers to create APIs. 

### R8:	Describe your projects models in terms of the relationships they have with each other

Each model within the `models` folder represents a table within my relational database. Here are the relationships: 

1. `Users`:
- This model represents each user. It has a One-Many relationship with the trips model, in which trips references users as a foreign key. Meaning one user can have many trips.
```
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
```

2. `Trips`:
- This model represents each trip. Trip has a one-to-one relationship with destinations, in which case trip references destinations as a foreign key. Meaning a trip can have one destination.
```
class Trip(db.Model):
    __tablename__ = "trips"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.id'), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    budget = db.Column(db.Float, nullable=True)  
```

3. `TransportType`:
This model represents a transport type/mode. This has a one-to-one relationship with transportation. Meaning a transportation event can have one transport type.
```
class TransportType(db.Model):
    __tablename__ = "transport_types"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
```

4. `Transportation`:
- This model represents each transportation event. As stated, a transportation event references the trip model with trip_id, as well as transportType. Meaning a transportation event can have one transport type, and it can also have one trip.
```
class Transportation(db.Model):
    __tablename__ = "transportations"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    transport_type_id = db.Column(db.Integer, db.ForeignKey('transport_types.id'), nullable=False)
    arrival_time = db.Column(db.DateTime, nullable=False)
    departure_time = db.Column(db.DateTime, nullable=False)
    arrival_location = db.Column(db.String(100), nullable=False)
    departure_location = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
```

5. `Destination`:
- This model respresents each individual destination. The trips model references climate ID as a foreign key, and is referenced by the trips model as a foreign key. Meaning a trip can have one destination and a destination can have many trips, as well as a destination can have 1 climate.
```
class Destination(db.Model):
    __tablename__ = "destinations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(100), nullable=False)
    climate_id = db.Column(db.Integer, db.ForeignKey('climates.id'), nullable=False)
```

6. `Climate`:
- This model represents each climate for a destination. Climate is referenced by the destination model as a foreign key, as a destination can have one climate.
```
class Climate(db.Model):
    __tablename__ = "climates"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False, unique=True)

```

7. `Activities`:
- This model represents activities within a trip. An activity references the trips model, as a foreign key. A trip can have many activities in this case. 
```
class Activity(db.Model):
    __tablename__ = "activities"

    id = db.Column(db.Integer, primary_key=True)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cost = db.Column(db.Float, nullable=True)
```

8. `Accommodation`:
- This model represents accommodation instances within a trip. An accommodation instance references the trips model as a foreign key, and a trip can have many accommodations. 
```
class Accommodation(db.Model):
    __tablename__ = "accommodations"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    check_in = db.Column(db.DateTime, nullable=True)
    check_out = db.Column(db.DateTime, nullable=True)
    cost_per_night = db.Column(db.Float, nullable=False)
    trip_id = db.Column(db.Integer, db.ForeignKey('trips.id'), nullable=False)
```

In summary, a user can make many trips. A trip can have one destination (which may have one climate.), many accommodation instances, many transportation events (which may have one transport type) and many activities.


### R9:	Discuss the database relations to be implemented in your application

In my flask application, there is a postgreSQL relational database, which uses SQLAlchemy to operate. The database can be accessed via psycopg2 which connects postgreSQL to python. Data is then encrypted, serialised and deserialised using Bcrypt and Marshmallow, respectively. In terms of models, my database has 8 tables, 6 of which have controllers, and 2 have preset options (`climate` and `transportType`). My `users` table is conntected to my `trips` model, which only references `users` and `destination` as a foreign key. The `accommodation`, `activities` and `transportation` tables are all connected to the `trips` model, as they reference it has a foreign key. The `destination` model references the `climates` model as a foreign key. The `transportation` model references `transportTypes` as a foreign key as well. 

`Users` - Allows a user to be registered and authenticated.
`Trips` - Allows a user to create a trip.
`Destination` - Allows a destination to be created and assigned to a trip.
`Climates` - Allows a destination to choose a climate.
`Activities` - Allows an activity to be assigned to a trip.
`Accommodation` - Allows an instance of accommodation to be assigned to a trip.
`Transportation` - Allows a transportation event to be assigned to a trip.
`TransportType` - Allows a transport type, or mode, to be assigned to a transportation event.


### R10: Describe the way tasks are allocated and tracked in your project

Throughout the construction of my web-application, I will, and have been using `monday.com` and `GitHub` to track and manage my project. I have been using monday.com as my project management service, assigning different tasks to "Haven't started", "Started", "Almost Finished" and "Complete". As I have moved through different stages and finishing different models pages, controller pages or questions, I have used this app as a sort of "to-do list" as well as to visually keep track of what must be complete, keeping me on task and motivating me to continue and work on different aspects. I also think it was good to look back on to know how much I have completed so there's a sense of "I am getting somewhere". 

As well as monday.com, I have also been using Github every time I have done work on a feature. Github is so useful for storing a backup, having access to changes over time as well as just knowing what I am up to. Throughout the creation of my project I would work on a feature on my to-do list and then after I have done substantial work on it, I would commit changes to the branch on github. There were times when looking back at a previous version was very valuable to make sure I didn't commit a change that should not have been done. 

By using both of these services, I found it very easy to organise what I had to do and slowly plan and deliver on features that I wanted to implement into my project. They both proved to be very important in the design and carrying-out of writing the code process and kept me on track to submit this project. 