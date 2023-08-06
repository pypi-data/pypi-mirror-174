from ast import arg
from gc import get_stats
import inspect
import io
import json
import marshal
import math
from multiprocessing.sharedctypes import Value
import types
from unittest.mock import Mock
import requests
import pandas as pd
import pprint
import pickle
from copy import deepcopy

from default_metrics import metrics as d_metrics
def add_doc(m) :
    m['description'] = m['metric_function'].__doc__ 
    return m
d_metrics = [add_doc(m) for m in d_metrics]

from codecarbon import OfflineEmissionsTracker

from sklearn.metrics import roc_auc_score, r2_score, accuracy_score, f1_score, balanced_accuracy_score, matthews_corrcoef

from aiirw import AI_IRW
import copy



import numpy as np
from sklearn.metrics import roc_auc_score, r2_score, accuracy_score, f1_score, balanced_accuracy_score, matthews_corrcoef
import math
import pickle
import io
import time


MAX_MB_UPLOAD = 1

def check_and_transform(Y):
    if isinstance(Y, np.ndarray):
        pass
    elif isinstance(Y, pd.DataFrame):
        Y = Y.to_numpy()[:,0]
    elif isinstance(Y, list):
        Y = np.asarray(Y)
    return Y

def compute_aiirw_depth(x_train, y_train, x_test, y_test):
    """Compute the aiirw depths of data points in x_test based on how they are far away from the
    in distribution constituted of x_train and x_test."""
    
    y_train = check_and_transform(y_train)
    y_test = check_and_transform(y_test)
    #print(np.concatenate([y_train,y_test]))
    unique_classes = set(np.concatenate([y_train,y_test]))
    scores_aiirw = []
    depth = [0]*len(y_test)
    x_test_depth = copy.deepcopy(x_test)
    for lab in unique_classes:
    
        indices_test = np.where(y_test == lab)[0]
        indices_train = np.where(y_train == lab)[0]

        x_train_lab = x_train.iloc[indices_train]
        x_test_lab = x_test.iloc[indices_test]
        #print(np.concatenate([x_train_lab, x_test_lab]))
        score_aiirw = AI_IRW(np.concatenate([x_train_lab, x_test_lab]))
        score_aiirw_test = score_aiirw[len(x_train_lab):]
        
        index_test  = x_test_depth.index[indices_test] 
        x_test_depth.loc[index_test, 'depth'] = score_aiirw_test

    return x_test_depth["depth"]

def get_rank(depth):
    """Compute the rank of each sample in x_test based on how far they are in the distribution. Smaller rank means
    closer to the center of the distribution"""
    return len(depth) - np.argsort(np.argsort(depth))


def compute_acc_vs_depth(depth_ranks, y_pred, y_test):
    """
    Function that compute the robustness curve every 1% of depth.
    
    Back computation.
    
    depth_ranks: array of int, for each test input, the rank for the depth (high depth means in-distribution).
    y_pred: array, the predictions of the model.
    y_test: array, the ground truth
    
    Outputs: prop, acc
    
    prop: list of the proportions (in pourcentage), 
          of size 100 if len(depth_ranks)>=100, otherwise of size len(y_test)
    acc: list of the accuracies corresponding to the prop list
    """
    
    # order y_pred and y_test according to the depth
    depth_ranks_ = np.array(depth_ranks) - 1
    y_pred_ = y_pred[depth_ranks_]
    y_test_ = y_test[depth_ranks_]
    
    s = 0  # the cumulated number of good predictions

    acc = []
    if len(depth_ranks) >= 100:
        prop = np.arange(100) + 1
        n = int((1/100)*len(depth_ranks)) # the amount of samples in 1%
        for i in range(len(depth_ranks)):
            s += int(y_pred_[i] == y_test_[i])
            if (i+1) % n == 0:
                acc.append(s / (i+1))
            if i == len(depth_ranks) - 1:
                if len(acc) == 99:
                    acc.append(s / (i+1))
    else:
        prop = []
        for i in range(len(depth_ranks)):
            s += int(y_pred_[i] == y_test_[i])
            acc.append(s / (i+1))
            prop.append(round((i+1)*100/len(depth_ranks),1))
    prop_and_acc = [[float(p),float(a)] for p,a in zip(prop,acc)]
    return prop_and_acc

        
class MockModel():
    p = 0.5

    def predict(self,df) :
        return [self.p]*len(df)



def compute_rescaled_scores(dict_score_models, h_is_b):
    """
    Compute rescaled scores from raw scores.
    
    Back computation: Use it each time a model or a metric is pushed.
    
    dict_score_models: dict of the form
    dict_score_models_test = {
        'model_1': 0.,
        'model_2': 10.,
        'model_3': 100.,
        'model_4': 50.
    }
    
    h_is_b: Boolean associated to the metric ("higher is better")
    
    Output: dict of the form
    {
    'model_1': 0.2, 
    'model_2': 0.1, 
    'model_3': 1., 
    'model_4': 0.5
    }
    """
    
    scores = np.array(list(dict_score_models.values()))
    min_, max_ = min(scores), max(scores)

    output = {}
    if len(dict_score_models) >= 3:
        if min_ != max_:
            output = {model: (score - min_) / (max_ - min_) for model, score in dict_score_models.items()}
            if h_is_b is False:
                output = {model: 1 - score for model, score in output.items()} 
            output = {model: 0.5 + (score-0.5)/(0.5/0.3) for model, score in output.items()}
        else:
            output = {model: 0.6 for model in output.keys()}
    else:
        output = {model: None for model in output.keys()} 
    return output

    

class Project():
    def __init__(self, session, pk, project_name :str, project_type, x_train, y_train, x_test, y_test, models=[],metrics=[],depth_metrics=[],scores=[],reports=[]) -> None:
        if project_type.lower() not in ['reg', 'classif']:
            raise ValueError("project_type should be 'reg' or 'classif', {} is not a valid project type.".format(project_type)) 
        
        self.project_type = project_type.lower()
        self.pk = pk
        self.project_name = project_name
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self._models = models
        self._model_objects = None
        self._metrics = metrics
        self._depth_metrics = depth_metrics
        self._metrics_objects = None
        self._scores = scores
        self.reports = reports
        self.session = session


    def list_models(self):
        md = deepcopy(self._models)
        print([mod.pop("model_file", None).pop("y_pred") for mod in md])

    def get_model(self, id) :
            #print(id)
            try :
                m=  [mod for mod in self._models if mod['model_name'] == id ][0]
            except :
                raise NameError("No model with the name {name_or_id}. List models with the Project.list_models() method.")
            try :
                r = requests.get(m['model_file'])
                b= io.BytesIO()
                b.write(r.content)
                b.seek(0)
                return pickle.load(b)
            except :
                raise Exception("Error while loading the model")

    def push_model(self, model_name, model, threshold=None):
        """
        Push a ML Model to althiqa's platform. 

        The model should be an object with a predict() method if it is a regression project.
        The model should be an object with a predict_proba() model if it is a classification project, 
        and a threshold between 0 and 1 should be given as argument. 
        """
        if self.project_type == 'reg' : 
            predict  = getattr(model, "predict", None)
            if not callable(predict):
                raise Exception(f'{model} does not have a predict method')
            y_pred = pd.DataFrame(model.predict(self.y_test))
            scores = {}
            depth_scores = []
            for metric in self._metrics :
                score = self.compute_metric(metric, model, threshold)
                if score is not None: 
                    scores[metric['metric_name']] = score
        
            for metric in self._depth_metrics :
                depth_scores.append({'depth_metric_name' : metric['depth_metric_name'] , 'score' : self.compute_depth_metric(metric, model, threshold) })
        
        if self.project_type == 'classif' : 
            if threshold is None or float(threshold)<0 or float(threshold)>1 : raise ValueError("This is a classification project, please enter a threshold value between 0 and 1.")
            predict  = getattr(model, "predict_proba", None)
            if not callable(predict):
                raise Exception(f'{model} does not have a predict_proba method')
            y_pred = pd.DataFrame(model.predict_proba(self.x_test))
            y_pred = (y_pred>float(threshold)).iloc[:, 1].astype(int)
            scores = {}
            for metric in self._metrics :
                score = self.compute_metric(metric, model, threshold)
                if score is not None: 
                    scores[metric['metric_name']] = score
            depth_scores = []
            #(self._depth_metrics)
            for metric in self._depth_metrics :
                depth_scores.append({'depth_metric_name' : metric['depth_metric_name'] , 'score' : self.compute_depth_metric(metric, model, threshold) })
        

        headers = {}
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer {token}".format(token  = self.session.token)
        buffer_y_pred = io.BytesIO()
        y_pred.to_pickle(buffer_y_pred)
        buffer_y_pred.seek(0)

        buffer_model = io.BytesIO()
        pickle.dump(model, buffer_model)
        buffer_model.seek(0)
        
        data = {'project_id' : self.pk, 'model_name' : model_name, 'scores': json.dumps(scores), 'threshold' : threshold, 'depth_scores' : json.dumps(depth_scores)}
        files = { 'y_pred_file' : ('_'.join([self.session.username, self.project_name, 'y_pred']),buffer_y_pred), 'model_file' : ('_'.join([self.session.username, self.project_name, model_name]),buffer_model)}
        r = requests.put(self.session.url + '/create_model/' , headers = headers , data = data, files=files)
        if r.status_code != 200 : 
            raise Exception('Request Error  '  + r.text)
        self._models.append(r.json())
        print('Model has been pushed to althiqa\'s platform with the following metric scores :')
        pprint.pprint(scores)


    def compute_metric(self, metric, model,threshold=None):
        
        if type(metric['metric_function']) == str :
            try :
                r = requests.get(metric['metric_function'])
                b= io.BytesIO()
                b.write(r.content)
                b.seek(0)
                m1 = marshal.load(b)
                m = types.FunctionType(m1, globals(), "metric")
            except :
                print(metric)
                raise Exception("Error while loading the metric")
        else : m = metric['metric_function']


        predict  = getattr(model, "predict", None)
        def predict_proba(y):
                return 
        if self.project_type == "classif":
            def predict(y):
                return (pd.DataFrame(model.predict_proba(y))>float(threshold)).iloc[:, 1].astype(int)
            def predict_proba(y):
                return model.predict_proba(y)

        arg_dict = {'model' : model, 'y_pred' : pd.DataFrame(predict(self.x_test)).iloc[:,0].to_numpy(), 'probs' :predict_proba(self.x_test), 'threshold': threshold, 'x_train' : self.x_train, 'y_train' : self.y_train.iloc[:,0].to_numpy(), 'x_test' : self.x_test, 'y_test': self.y_test.iloc[:,0].to_numpy(), 'protected_attribute' : metric.get('protected_attribute',None)}
        f_params = list(inspect.signature(m).parameters.keys())
        d2 = { k:v for k,v in arg_dict.items() if k in f_params }

        if 'protected_attribute' in d2.keys() and d2['protected_attribute'] is None :
            #print("{mn} metric needs a valid protected attribute argument. Metric not computed.".format(mn = metric['metric_name']))
            return None
        
        try :
            score = m(**d2)
        except Exception as e: 
            raise e
        return {'score' : round(float(score),2)}

    def compute_depth_metric(self, metric, model, threshold = None):
        
        predict  = getattr(model, "predict", None)
        if not callable(predict):
            def predict(y):
                return (pd.DataFrame(model.predict_proba(y))>float(threshold)).iloc[:, 1].astype(int)
        y_pred =  pd.DataFrame(predict(self.x_test)).iloc[:,0].to_numpy()
        rank = metric['ranks']
        scores = compute_acc_vs_depth(rank, y_pred, self.y_test.iloc[:,0].to_numpy() )
        return scores

        
    def create_metric(self, metric_name: str, metric_function , protected_attribute = None, description = None, h_is_b = False, v= 1 ):
        # check metric can be applied to y_pred
        try :
            model = MockModel()
            arg_dict = {'model' : model, 'y_pred' : pd.DataFrame(model.predict(self.x_test)).iloc[:,0].to_numpy(), 'x_train' : self.x_train, 'y_train' : self.y_train, 'x_test' : self.x_test, 'y_test': self.y_test, 'protected_attribute' : protected_attribute}
            f_params = list(inspect.signature(metric_function).parameters.keys())
            d2 = { k:v for k,v in arg_dict.items() if k in f_params }
            score = float(metric_function(**d2))
            if not (type(score) == float ) or (type(score) == int ) :
                raise ValueError()
        except Exception as e :
            pass 
            
        metric = {'metric_name' : metric_name, 'metric_type' : self.project_type, 'metric_function' : metric_function, 'description' : description ,'h_is_b' : h_is_b, 'protected_attribute' : protected_attribute}
        scores = {}
        for model in self._models : 
            m = self.get_model(model['model_name'])
            score = self.compute_metric(metric, m, model['threshold'])
            if score is not None : 
                scores[model['model_name']] =  score
        metric['scores'] = scores
        
        headers = {}
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer {token}".format(token  = self.session.token)
        metric_function_file = io.BytesIO()
        marshal.dump(metric['metric_function'].__code__, metric_function_file)
        metric_function_file.seek(0)
        
        data = {'project_id' : self.pk, 'metric_name' : metric['metric_name'], 'metric_type' : metric['metric_type'],
         'description' :  metric['description'] , 'h_is_b' :  metric['h_is_b'], 'scores': json.dumps(scores)}
        files = { 'metric_file' : ('_'.join([self.session.username, self.project_name, metric_name]),metric_function_file)}
        r = requests.put(self.session.url + '/create_metric/' , headers = headers , data = data, files=files)
        if r.status_code != 200 : 
            raise Exception('Request Error  '  + r.text)
        self._metrics.append(metric)
        if v : 
            print('Metric has been pushed to the Althiqa platform with the following metric scores :')
            pprint.pprint(scores)

    def create_depth_metric(self, depth_metric_name: str, depth_metric_function , description = None):
        # check metric can be applied to y_pred
        try :
            model = MockModel()
            arg_dict = {'model' : model, 'y_pred' : model.predict(self.y_test), 'x_train' : self.x_train, 'y_train' : self.y_train, 'x_test' : self.x_test, 'y_test': self.y_test, 'protected_attribute' : protected_attribute}
            f_params = list(inspect.signature(depth_metric_function).parameters.keys())
            d2 = { k:v for k,v in arg_dict.items() if k in f_params }
            score = list(depth_metric_function(**d2))
            rank = get_rank(score)
            if not (type(score) == float ) or (type(score) == int ) :
                raise ValueError()
        except Exception as e : 
            raise e 
            
        depth_metric = {'depth_metric_name' : depth_metric_name,  'depth_metric_function' :depth_metric_function, 'description' : description, 'rank': rank }
        scores = {}
        for model in self._models :
         
            m = self.get_model(model['model_name'])
            score = self.compute_depth_metric(depth_metric, m, model['threshold'])
            scores[model['model_name']] =  score

        depth_metric['scores'] = scores
        
        headers = {}
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer {token}".format(token  = self.session.token)
        metric_function_file = io.BytesIO()
        pickle.dump(depth_metric['metric_function'], metric_function_file)
        metric_function_file = io.BytesIO().seek(0)
        
        data = {'project_id' : self.pk, 'depth_metric_name' : depth_metric['depth_metric_name'],
         'description' :  depth_metric['description'] , 'rank' : depth_metric['rank'], 'scores': json.dumps(scores)}
        files = { 'depth_metric_file' : ('_'.join([self.session.username, self.project_name, depth_metric_name]),metric_function_file)}
        r = requests.put(self.session.url + '/create_depth_metric/' , headers = headers , data = data, files=files)
        if r.status_code != 200 : 
            raise Exception('Request Error  '  + r.text)
        print('Depth metric has been pushed to althiqa\'s platform with the following metric scores :')
        pprint.pprint(scores)

    







class Session():
    def __init__(self, username, password, url ='http://api.althiqa.io') -> None:
        self.url = url
        self.username = username
        self.password = password
        try :
            r = requests.post(self.url + '/api/token/', data = {'username' : self.username , 'password' : self.password} )
            if r.status_code != 200 :
                raise Exception('Request failed, is your url correct ?')
            res = r.json()
            if 'access' in res.keys() :
                print('Login succesful, token obtained')
                self.token = res['access']
            else : 
                raise Exception("Login unsuccessful : "  +  r.text)
        except Exception as e :
            raise Exception("Can't authenticate to 'url' with this username and password")

    def list_projects(self):
        headers = {}
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer {token}".format(token  = self.token)
        r = requests.get(self.url + '/list_projects/', headers = headers)
        if r.status_code != 200 : 
            raise Exception('Bad request : '  + r.text)
        pprint.pprint(r.json())
    
            
    
    def create_project(self, project_name :str, x_train, y_train, x_test, y_test, project_type = 'reg') :
        # check project_type in 'classif' or 'reg'
        if project_type not in ['reg', 'classif'] : 
            raise Exception("Argument project_type must be 'reg' (default) or 'classif'")
        # check datas can be converted to dataframe
        try : 
            x_train = pd.DataFrame(x_train)
            y_train = pd.DataFrame(y_train)
            x_test = pd.DataFrame(x_test)
            y_test = pd.DataFrame(y_test)
        except :
            raise Exception("Passed datas must be convertible to DataFrame")
        headers = {}
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer {token}".format(token  = self.token)
        data = {'project_name' :project_name ,'project_type' : project_type.capitalize()}
        buffer_x_train = io.BytesIO()
        buffer_y_train = io.BytesIO()
        buffer_x_test = io.BytesIO()
        buffer_y_test = io.BytesIO()

        x_train.to_pickle(buffer_x_train)
        y_train.to_pickle(buffer_y_train)
        x_test.to_pickle(buffer_x_test)
        y_test.to_pickle(buffer_y_test)

        buffer_x_train.seek(0)
        buffer_x_train.name = 'x_train.pckl'
        buffer_y_train.seek(0)
        buffer_x_test.seek(0)
        buffer_y_test.seek(0)
        
        files = { 'x_train_file' : ('_'.join([self.username, project_name, 'x_train']),buffer_x_train), 'y_train_file' : ('_'.join([self.username, project_name, 'y_train']),buffer_y_train),
                'x_test_file': ('_'.join([self.username, project_name, 'x_test']),buffer_x_test), 'y_test_file' : ('_'.join([self.username, project_name, 'y_test']),buffer_y_test)}
        
        for key, value in files.items()  :
            nmb = round(value[1].getbuffer().nbytes / (1024*1024),2)
            if nmb > MAX_MB_UPLOAD : 
                raise Exception(f"File {key} is too large ({nmb}MB). Please use objects smaller than {MAX_MB_UPLOAD}MB.".format(key=key, nmb=nmb ))
        
        default_depth_rank = []
        if project_type=='classif':
            default_depth_rank = get_rank(compute_aiirw_depth(x_train, y_train, x_test, y_test) )       
        data = {'project_name' : project_name, 'project_type' : project_type, 'y_len' : len(y_test), 'default_depth_rank' : json.dumps(default_depth_rank.tolist())}
        
        r = requests.put(self.url + '/create_project/' , headers = headers , data = data, files=files)
        if r.status_code != 200 : 
            raise Exception('Request Error  '  + r.text)
        res = r.json()
        pk = res['pk']
        #print('Project pk:' + str(pk))
        #print(res)
        p = Project(self, pk, project_name, project_type, x_train, y_train, x_test, y_test, metrics = [], depth_metrics = res['depth_metrics'])
        for m in d_metrics :
            if m['metric_type'] == p.project_type : p.create_metric(metric_name = m['metric_name'], metric_function= m['metric_function'] , protected_attribute = m.get('protected_attribute',None), description = m['description'], h_is_b= m['h_is_b'], v=0)
        return p

    def get_project(self, name : str) :
        headers = {}
        headers["Accept"] = "application/json"
        headers["Authorization"] = "Bearer {token}".format(token  = self.token)
        params = {'name' : name}
        r = requests.get(self.url + '/get_project' , headers = headers , params = params)
        res = r.json()
        x_train = self.get_s3_file(res['x_train'])
        y_train = self.get_s3_file(res['y_train']) # Faire comme cela ??
        x_test = self.get_s3_file(res['x_test'])
        y_test = self.get_s3_file(res['y_test'])
        pk = res['pk']
        print(res['project_type'])
        return Project(self, pk, res['project_name'], res['project_type'], x_train, y_train, x_test, y_test, models = res['models'] , metrics= res['metrics'] , depth_metrics=res['depth_metrics'] , scores = res['scores'], reports= res['reports'])

    def get_s3_file(self, url):
        # A Tester / Debugger
        print(url)
        r = requests.get(url) # Coder l'API en faisant attention à vérifier que le fichier appartient bien au user.
        buff = r.content
        print(type(buff))
        b= io.BytesIO()
        b.write(r.content)
        b.seek(0)
        df_obj = pickle.load(b)
        return df_obj
