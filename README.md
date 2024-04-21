![logo](icon.png)

## Budget Hero is a finance-tracking website
We built budget hero to gamify the experience of saving money. In this project, you'll defeat bad credit, overcome gambling addiction, and play the stock market safe—literally. Your character, Mr. Coin, will fight against these forces on your behalf.

## How it works
Budget Hero has its own backend, which calls the `nessieisreal` CapitalOne API and allows you to track your finances. Whenever you add a positive transaction, whether that be a check, money transfer, or sale, Mr. Coin will attack the enemies on your behalf. On the other hand, if you lose money, due to debt, purchases, or any other reason, Mr. Coin will lose his health. Try to defeat the largest number of enemies before losing all of your HP! 

## Developers:

* [cwdalziel](https://github.com/cwdalziel) - Frontend / React App
* [nkasica](https://github.com/nkasica) - Backend / Artwork
* [yuwex](https://github.com/yuwex) - Backend / Database

## Running the Project

### Frontend

This projet's frontend was created with [Create React App](https://github.com/facebook/create-react-app). 
After installing `npm` on your device, use the following command to build this project.

### `npm run build`

Then, start this project with the following command.

### `npm start`

### Backend

This project's backend was created with [FastAPI](https://fastapi.tiangolo.com/).
To set up the backend, follow these steps:

1) Create a virtual environment for python with `python3.10 -m venv .venv`
2) Switch to that environment with `source .venv/bin/activate`
3) Install required dependencies with `pip install -r backend/requirements.txt`

To run the backend, do the following:

1) Ensure you are using the virtual environment. If not, repeat step 2.
2) Run `python backend/main.py`