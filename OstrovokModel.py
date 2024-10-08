import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


class OstrovokModel:
    """
    A model for predicting hotel room attributes based on rate names.

    This class loads training data from a CSV file, processes it using TF-IDF vectorization,
    and trains or loads multiple neural network models to predict various room attributes.

    Parameters:
    -----------
    pred_type : int, optional (default=1)
        Determines the number of room attributes to predict:
        0 - Predicts 3 main parameters: bedding, capacity, view
        1 - Predicts 7 parameters: class, quality, bathroom, bedding, capacity, club, view
        2 - Predicts 10 parameters: class, quality, bathroom, bedding, capacity, club, bedrooms, balcony, view, floor

    need_create : int, optional (default=0)
        Determines whether to train new models or load existing ones:
        1 - Train new neural network models
        0 - Load pre-trained models from files

    Input Data:
    predict(X): 
        X - list of strings representing rate names
    Output Data:
        Dict of predicted parameters for each rate name in X
        
        Output Format:
            list of dict = {
                rate_name: input rate name,
                class: predicted class,
                quality: predicted quality,
                bathroom: predicted bathroom,
                bedding: predicted bedding,
                capacity: predicted capacity,
                club: predicted club,
                bedrooms: predicted bedrooms,
                balcony: predicted balcony,
                view: predicted view,
                floor: predicted floor
            }
    """
    
    def __init__(self, pred_type=0, need_create=1):

        self.train_data = pd.read_csv('opt/temp/rates_train.csv', encoding='latin-1')
        self.train_data.fillna('undefined', inplace=True)
        self.vectorizer = TfidfVectorizer(max_features=16384)
        self.vectorizer.fit_transform(self.train_data['rate_name'].values)
        self.models = dict()
        
        self.col_names = (
            ['bedding', 'capacity', 'view'] if pred_type == 0
            else ['class', 'quality', 'bathroom', 'bedding', 'capacity', 'club', 'balcony', 'view'] if pred_type == 1
            else ['class', 'quality', 'bathroom', 'bedding', 'capacity', 'club', 'bedrooms', 'balcony', 'view', 'floor']
        )

        for col_name in self.col_names:
            self.models[col_name] = (self.model_create(col_name) if need_create else self.model_load(col_name))


    def model_fit(self, model, X, y):
        model.fit(X, y)
        return model

    def model_create(self, col_name):
        X_train_vectorized = self.vectorizer.fit_transform(self.train_data['rate_name'].values)

        # Our model is here. Since this is a trade secret, we cannot disclose it.
        return None

        with open(f'opt/temp/models/model_{col_name}.pkl', 'wb') as f:
            pickle.dump(model, f)

        return model

    def model_load(self, col_name):
        with open(f'opt/temp/models/model_{col_name}.pkl', 'rb') as f:
            return pickle.load(f)


    def predict(self, X):
        ans = [
            {
                'rate_name': rate_name
            }
            for rate_name in X
        ]
        for col_name in self.col_names:
            new_room_names_vectorized = self.vectorizer.transform(X)
            predictions = self.models[col_name].predict(new_room_names_vectorized)
            for i in range(len(predictions)):
                ans[i][col_name] = str(predictions[i])

        return ans