import csv

ATTRS = ["LOCATION", "W", "FINAL_MARGIN", "SHOT_NUMBER", "PERIOD", "GAME_CLOCK", "SHOT_CLOCK", "DRIBBLES", "TOUCH_TIME",
         "SHOT_DIST", "PTS_TYPE", "CLOSE_DEF_DIST", "SHOT_RESULT"]
ATTRS_WO_CLASS = 12

def load_data(filename):
    train_x = []
    train_y = []
    test_x = []
    test_y = []
    with open(filename, 'rt') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        i = 0
        for row in csvreader:
            if len(row) == ATTRS_WO_CLASS + 1:
                i += 1
                instance = [row[i] for i in range(ATTRS_WO_CLASS)]  # first ATTRS_WO_CLASS values are attributes
                label = row[ATTRS_WO_CLASS]  # (ATTRS_WO_CLASS + 1)th value is the class label
                if i % 3 == 0:  # test instance
                    test_x.append(instance)
                    test_y.append(label)
                else:  # train instance
                    train_x.append(instance)
                    train_y.append(label)
                    
    return train_x, train_y, test_x, test_y

def evaluate(predictions, true_labels):
    correct = 0
    incorrect = 0
    for i in range(len(predictions)):
        if predictions[i] == true_labels[i]:
            correct += 1
        else:
            incorrect += 1

    print("\tAccuracy:   ", correct / len(predictions))
    print("\tError rate: ", incorrect / len(predictions))

def main():
         
         
train_x, train_y, test_x, test_y = load_data("data/basketball.train.csv")

from sklearn.feature_extraction import DictVectorizer

dicts_train_x = []
for x in train_x:
    d = {}
    for i, attr in enumerate(ATTRS):
        if i < len(ATTRS) - 1: # we removed class from train_x elems
            val = x[i]
            # TODO: save as floats the values for the already-numeric attributes from dataset, keep the rest as the 
            #strings they are
            d[attr] = val
        if (i >= 2) and (i <= 11):
            val = float(x[i])#save as float
            d[attr] = val
    dicts_train_x.append(d)

vectorizer_train = DictVectorizer()
vec_train_x = vectorizer_train.fit_transform(dicts_train_x).toarray()

dicts_test_x = []

for x in test_x:
    d = {}
    for i, attr in enumerate(ATTRS):
        if i < len(ATTRS) - 1: # we removed class from train_x elems
            val = x[i]
            # TODO: save as floats the values for the already-numeric attributes from dataset, keep the rest as the 
            #strings they are
            d[attr] = val
        if (i >= 2) and (i <= 11):
            val = float(x[i])#save as float
            d[attr] = val
    dicts_test_x.append(d)
    
vectorizer_test = DictVectorizer()
vec_test_x = vectorizer_test.fit_transform(dicts_test_x).toarray()

from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier()
clf.fit(vec_train_x, train_y)
predictions = clf.predict(vec_test_x)
evaluate(predictions, test_y)


if __name__ == "__main__":
    main()
