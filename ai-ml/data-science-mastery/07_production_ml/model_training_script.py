import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

class MlModel:
    def __init__(self, model, name='Model'):
        self.model = model
        self.name = name

    def train(self, X_train, y_train):
        print ('\nTraining %s ...\n'%self.name)
        self.model.fit(X_train, y_train)
        print ('Training completed!\n')

    def predict(self, X_test):
        print ('Making predictions ...\n')
        return self.model.predict(X_test)

    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        print ('Accuracy: %.4f\n'%acc)
        print ('Confusion Matrix:\n', confusion_matrix(y_test, y_pred))
        print ('\nClassification Report:\n', classification_report(y_test, y_pred))
        return acc

    def feature_importance(self, feature_names=None):
        if hasattr(self.model, 'feature_importances_'):
            imp = self.model.feature_importances_
            if feature_names:
                for name, val in sorted(zip(feature_names, imp), key=lambda x: x[1], reverse=True):
                    print ('%s: %.4f\n'%(name, val))
            else:
                for i, val in enumerate(imp):
                    print ('Feature %d: %.4f\n'%(i, val))
            return imp
        else:
            print ('Model does not have feature_importances_ attribute\n')
            return None
