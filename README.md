# biston
Calliope-class sentiment parser with built-in usefulness metrics

## components
The following files are available for use. Those marked with an asterisk(*) afterward are not yet completed.

### JSONLoader
Loads a JSON file into memory. Operates under the lazy-loading paradigm (meaning it won't guarantee having processed the data until it's asked for). 

### DataProcessor
Pulls in reviews from JSONLoader, processes the data to match what the Learners will need

### SentimentLearner*
Trains on a set of texts to create a Bayesian Naïve model for individual word sentiment scores. Predicts review sentiment by averaging individual word scores. 

### UsefulnessLearner*
Runs an MLP model for predicting the usefulness of a given review. Pre-processes input to extract relevant features.
