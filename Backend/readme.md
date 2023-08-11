## the program  uses fastapi for the backend

### cd Backend/app/
### pip install -r requirements.txt
Modify the mongourl in the .env file
To load the data from the csv file to db
### python3 dataloader.py
To run the app
### uvicorn main:app --reload
