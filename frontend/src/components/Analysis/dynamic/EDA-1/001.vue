<template>
   <card class="pt-4">
        <div class="typography-line">
        <p>코드는 다음과 같이 표기한다. 분석하는 동안 import했던 모듈의 총 집합이다.</p>
        </div>
        <send-code number="1">
                    import numpy as np<br/>
import pandas as pd <br/>
import os<br/>
import json<br/>
import time<br/>
import hashlib<br/>
from os import listdir<br/>
from os.path import isfile, join<br/>
from copy import deepcopy<br/>
<br/>
import datatable as dt<br/>
import dask.dataframe as dd<br/>
import datetime<br/>
<br/>
import folium<br/>
import dash_bio<br/>
from plotly.subplots import make_subplots<br/>
import plotly.graph_objects as go<br/>
import plotly.express as px<br/>
import plotly.offline as pyo<br/>
from folium.plugins import HeatMap<br/>
import matplotlib.pyplot as plt<br/>
import seaborn as sns<br/>
from IPython.display import Image<br/>
from matplotlib import font_manager<br/>
<br/>
import scipy.stats as stats<br/>
from scipy.signal import periodogram<br/>
<br/>
from matplotlib import rcParams<br/>
<br/>
import statsmodels.api as sm<br/>
from statsmodels.formula.api import ols<br/>
from statsmodels.stats.outliers_influence import OLSInfluence<br/>
from statsmodels.tsa.stattools import kpss<br/>
from statsmodels.tsa.deterministic import CalendarFourier, DeterministicProcess<br/>
<br/>
from sklearn.neighbors import KNeighborsClassifier<br/>
from sklearn.preprocessing import MinMaxScaler, power_transform, StandardScaler<br/>
from sklearn.metrics import mean_squared_error, mean_absolute_error, make_scorer, accuracy_score, log_loss<br/>
from sklearn.model_selection import train_test_split , TimeSeriesSplit, GridSearchCV, ParameterGrid<br/>
from sklearn.linear_model import LinearRegression , Ridge , Lasso, ElasticNet, LassoLars, SGDRegressor, Perceptron, LogisticRegression<br/>
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor,AdaBoostRegressor, RandomForestClassifier, GradientBoostingClassifier, ExtraTreesClassifier, VotingClassifier<br/>
from sklego.meta import ZeroInflatedRegressor<br/>
<br/>
from xgboost import XGBRegressor, XGBClassifier<br/>
from lightgbm import LGBMRegressor, LGBMClassifier<br/>
<br/>
import multiprocessing<br/>
import gplearn as gpl<br/>
from gplearn.genetic import SymbolicRegressor <br/>
from sklearn.neural_network import MLPRegressor, MLPClassifier<br/>
from sklearn.cross_decomposition import PLSRegression<br/>
from sklearn.compose import TransformedTargetRegressor<br/>
import torch<br/>
import torch.nn as nn<br/>
from torch.autograd import Variable<br/>
import torch.optim as optim<br/>
import torch.nn.functional as F<br/>
from torch.utils.data import TensorDataset, DataLoader, Dataset<br/>
import argparse<br/>
import keras<br/>
import tensorflow as tf<br/>
from keras import optimizers<br/>
from keras.models import Sequential<br/>
from keras.layers import Dense, LSTM, TimeDistributed, RepeatVector<br/>
<br/>
from functools import partial<br/>
<br/>
import os<br/>
import dataframe_image as dfi<br/>
        </send-code>
        <div class="typography-line">
        <p>다음은 코드의 입력과 출력이다. 입력은 왠만하면 숨겨놓도록 하겠다.</p>
        </div>
        <send-code number="2">
            data_dir = 'E:/seoulbike/data/'<br/>
                share_spot = pd.read_csv(data_dir + '대여소\대여소정보.csv', engine='python',encoding='CP949', index_col=0)<br/>
                share_spot.info()<br/>
        </send-code>
        <receiveCode>           
            Int64Index: 2653 entries, 102 to 5855<br/>
            Data columns (total 9 columns):<br/>
            #   Column     Non-Null Count  Dtype  <br/>
            ---  ------     --------------  -----  <br/>
            0   보관소(대여소)명  2653 non-null   object <br/>
            1   자치구        2653 non-null   object <br/>
            2   상세주소       2653 non-null   object <br/>
            3   위도         2653 non-null   float64<br/>
            4   경도         2653 non-null   float64<br/>
            5   설치시기       2652 non-null   object <br/>
            6   LCD        1290 non-null   float64<br/>
            7   QR         1355 non-null   float64<br/>
            8   운영방식       2629 non-null   object <br/>
            dtypes: float64(4), object(5)<br/>
            memory usage: 207.3+ KB<br/>
        </receiveCode>


   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue'

export default {
    name : 'dynamic-001',
  components: {
    sendCode,
    receiveCode
  },
  data() {
    return {

    };
  }
};
</script>