from .data_cleaner import clean_data
from .data_cleaner_sample import sample_clean_data
from .data_fetch_api import fetch_data
from .model_train import train_model
from .predict import make_prediction
from .data_exploration import explore_data

def main():
    fetch_data()
    clean_data()
    sample_clean_data()
    explore_data()
    train_model()
    make_prediction()




if __name__ == "__main__":
    main()