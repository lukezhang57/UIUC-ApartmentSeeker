<!-- ABOUT THE PROJECT -->
# ApartmentSeeker
## About The Project

<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com) -->

Almost every college student has to look for apartments at some point in their four years. There are so many factors when it comes to picking apartments (like how far you want to be from your classes, how clean you want your apartment, how much rent you are willing to spend, etc.), and not all of those factors are fully considered. 

ApartmentSeeker is a social networking platform where thousands of students can come together to rate apartments near them and find subleases. ApartmentSeeker helps put all the apartment information people want in one place, adds additional considerations along with the most common ones, and allows users to share opinions on these various apartments.



### Built With

#### Front End

* [React.js](https://reactjs.org/)
* [Chakra UI](https://chakra-ui.com/)
* [Leaflet](https://leafletjs.com/)


#### Back End
* [Django](https://www.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [MongoDB](https://www.mongodb.com/)
* [Geopy](https://geopy.readthedocs.io/en/stable/)



<!-- GETTING STARTED -->
## Getting Started
After cloning the repo with
```
git clone https://github.com/lukezhang57/UIUC-ApartmentSeeker
```
change directory to the folder with
```
cd UIUC-ApartmentSeeker
```


The backend code is in the `backend` folder of the repo, so to go to the backend code, change directory to the backend folder
```
cd backend
```
For the backend code to run, first the prerequisite libraries have to be installed. There is a file requirements.txt with the libraries needed to run the backend

* python
  ```sh
  pip install -r requirements.txt
  ```


1. If you made any changes on the models.py, first, make the migrations of the Django models by running
   
   ```
   python manage.py makemigrations
   ```
   
2. Migrate the changes made

   ```
   python manage.py migrate
   ```
   
3. Run the server

   ```
   python manage.py runserver
   ```

From there, you will be able to access the backend server and request data from it via HTTP requests. The http urls are either `http://localhost:8000/api/` or `http://127.0.0.1:8000/api/`. The urls are provided in `\backend\urls.py` from the backend folder. 

Open another terminal, go to your repository folder
```
cd <path-to-repo>/course-project-tqk-b
```

To run the react app, cd into the frontend folder first
```
cd frontend
```
Then, npm install
```
npm install
```
Finally, run 
```
npm start
```
Visit `localhost:3000` to view the application
   

<!-- TECHNICAL ARCHITECTURE -->
On the frontend, the project uses React.js. With reusable components for the star ratign system, apartment cards, and university cards,
we were able to expedite our development process. There is a folder called "components" which houses the components. Then, there is a folder called "pages" which houses the pages that use the compoments. We used react-router-dom to allow navigation between pages. For gettign data from and sending data to the backend, we used the axios library. For the map, leaflet.js was used to guide the user in picking important buildings. We added pins on the map corresponding to the locations of the important buildings. 

On the backend, the project uses Django and its REST framework along with the MongoDB database to store the apartment data as well as the apartment reviews, apartment subleases, and the important buildings. The backend communicates with the frontend via HTTP requests, and when the frontend sends an HTTP request to the backend, depending on the request, the backend does specific tasks, like posting review data to the database, posting sublease data to the database, returning nearest apartments to a list of important buildings by calculating disance between the apartments and the important buildings via Geopy and Haversine. 


<!-- USAGE EXAMPLES -->
## Usage

* [Presentation link here](https://docs.google.com/presentation/d/1Zhr8qFA--O80eYQpkk2Fhpn2VT1A9H9hk1qBDjLDzeg/edit?usp=sharing)


## Testing
To run the formal unit tests locally on the backend, we first must go to the backend code. The backend code is in the `backend` folder of the repo, so to go to the backend code, change directory to the backend folder
```
cd backend
```
For the backend code to run, first the prerequisite libraries have to be installed. There is a file requirements.txt with the libraries needed to run the backend

* python
  ```sh
  pip install -r requirements.txt
  ```


1. If you made any changes on the models.py, first, make the migrations of the Django models by running
   
   ```
   python manage.py makemigrations
   ```
   
2. Migrate the changes made

   ```
   python manage.py migrate
   ```

3. Run the unit tests with
   ```
   python manage.py test
   ```

## Creators
* **Yug Mittal** -- Worked on backend code
* **Luke Zhang** -- Worked on backend code
* **Jinhyuk Kim** -- Worked on frontend code
* **James Huang** -- Worked on frontend code
