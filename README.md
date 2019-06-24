# robo-advisor

# 1. Use your text editor or the command-line to create a new file called "requirements.txt", and then place the following contents inside:

requests
python-dotenv


# 2. Create and activate a new Anaconda virtual environment:

conda create -n stocks-env python=3.7 # (first time only)
conda activate stocks-env

# 3. From within the virtual environment, install the required packages specified in the "requirements.txt" file you created:

pip install -r requirements.txt
pip install pytest # (only if you'll be writing tests)

# 4. Make sure the .env file is updated with your 

ALPHAVANTAGE_API_KEY 
# 5. Which can be found here: https://www.alphavantage.co/documentation/

# 6. From within the virtual environment, demonstrate your ability to run the 
Python script from the command-line:

python robo_advisor.py

