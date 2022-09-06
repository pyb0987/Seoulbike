<template>
  <div class="col-md-10 mx-auto">
    <div ref="scroll"></div>
    <card class="p-4">
    <div class="typography-line">
    <h1>
        따릉이 분석 - 머신러닝
    </h1>
    <hr>
    </div>
    <div class="typography-line pt-5">
    <p>머신러닝 모델을 만드는 것은 여러 측면에서 고역이었는데, 여러가지 시도하고 만들다보니 나중에 알게된 모델의 제약이라던가, 이용가능한 데이터의 한계, 모델의 한계 내지는 속도의 제약 같은
      여러가지 문제를 마주했다.
      필자가 겪었던 문제를 하나하나 시간 순으로 나열하는 것은 그다지 재밌지도 않고, 지루할 것이므로 이미 다 겪은 상황에서 정리를 해보도록 하겠다.<br/><br/>

      겪었던 가장 큰 문제점은 모델의 인풋과 아웃풋을 결정하는데 큰 어려움을 가졌다는 것이다. 독립변수들의 정규화를 어떻게 하느냐에 따라 모델의 예측력은 약간의 차이를 보였고,
      또 어떤 독립변수를 실제로 골라 모델에 넣을 것인가가 매우 중요했다. 아웃풋(y) 또한 여러 선택지가 있었는데, 예측하려고 하는 것은 임의의 대여소의 자전거 잔여대수이므로
      그것을 시간당 유입량을 예측함으로써 도출할 수도 있었지만, 더 환원하여 시간당 대여대수, 반납대수를 예측하는 선택을 할 수 있었다.<br/><br/>

      두가지 선택지 모두 놓지 않고 시도해보았으나, 유입량으로 예측하는 편의 오차가 더 낮았다.
      그러나 어느쪽을 선택하든지, 분포가 0에 치우치는 경향이 있었고, 특히나 시간당 유입량의 경우에는 과반수의 데이터가 0이었다. 그러나 큰 수치로 튀는 이상치들이 확실히
      존재했고 이를 정규화하기 위해 cbrt변환을 시도했다. 대여대수와 반납대수를 예측할 때에는 log1p변환을 시도했다.<br/><br/>

      그 이유는 그렇게 할 때 정규성 검사를 통과하며, y가 정규성을 만족할 때 머신러닝의 퍼포먼스가 좋음이 알려져있었기 때문이다. 하지만 그러한 변환은 fitting을 수행할 시에
      오차 계산을 제대로 할 수 없게 한다. 때문에 TransformedTargetRegressor를 이용해 fitting을 해보기도 했다. scoring으로 널리 알려진 것은 rmsle, rmse, mae 등이었지만,
      대여소 1개소의 자전거의 대수를 예측하는 서비스의 특성상 mae를 scoring function으로 채택했다.
      그러나 결국 왜곡된 y값은 제대로 된 값을 내놓는 데 오히려 악영향을
      미쳤고, 결과적으로는 모델이 0에서 약하게 진동하는 값만을 내놓도록 하는 문제점을 보였다.<br/><br/>


    </p>
    </div>
    <div class="d-flex justify-content-center">

      <object data="http://localhost:8000/static/figures/pred_cbrt_comparison.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
    </div>

    <div class="typography-line pt-5">
    <p>필자를 절망하게 한 것은 저러한 결과만을 내놓는 모델의 오차가 다른 모델의 오차보다 더 뛰어난 경향을 보였다는 것이다.
      하지만 저러한 모델로는 서비스를 할 수 없을 것이다. 결국 cbrt 또는 log와 같은 변환을 수행하지 않고 모델을 만들었다.
      그것을 결정하는데는 오랜 시간이 걸렸고, 그 때까지는 여러가지 방법론을 시도할 때마다 스케일링을 한 경우의 결과까지 확인해야 했다.<br/><br/>

      인풋으로 무엇을 넣을지 결정하는 과정에서 데이콘에서 따릉이를 이용한 분석을 수행한 한 분의 도움을 받아 새로운 feature를 생성할 아이디어를 갖게 되었다.
      그 아이디어라는 것이 매우 주효했는데, 이전까지는 갈피를 잘 잡고 있지 못하다가 feature를 생성한다는 것에 대해 눈을 뜨자
      여러가지 새로운 시도를 할 수 있게 되었기 때문이다. 또 일전의 '지그재그'에 일직선으로 대처하던 모델보다 낮은 오차를 가지게 되었다.<br/><br/>
      그 분은 체감온도라는 feature를 만드셨지만, 필자는 그것 이외에도 약 20여가지의 feature들을 만든 후, 후진제거법으로 최종적으로는
      6개의 feature들이 최종모델에 포함되었다.(코드의 '일출시간'과 '일몰시간'은 기상청에서 확인한 서울의 일몰, 일출시간을 근거로 만든 dictionary이다.)

    </p>
    </div>
    <send-code number="1">

&nbsp; &nbsp; &nbsp; &nbsp; data['불쾌지수'] = (1.8*data['기온'] - 0.558*(1-data['습도(%)']/100)+(1.8*data['기온']-26)+32)<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['경과도'] = np.sqrt(1+data['경과일'])<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['2020년'] = (data['년']==2020).astype(int)<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['광도'] = ((data['시'] - data['월'].replace(일출시간)&gt;-1) &amp; (data['월'].replace(일몰시간) - data['시'] &gt;0.5)).astype(int) + ((data['시'] - data['월'].replace(일출시간)&gt;0) &amp; (data['월'].replace(일몰시간) - data['시'] &gt;0)).astype(int)-0.03*data['전운량(10분위)']<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['출근'] = ((data['시'].isin([7,8,9])).astype(int) + (data['시'].isin([8])).astype(int)*2)*(1-data['휴일'])<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['퇴근'] = ((data['시'].isin([17,18,19])).astype(int) + (data['시'].isin([18])).astype(int)*2)*(1-data['휴일'])<br>
    </send-code>
    <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/acf_pacf.png" class='frame' style="background-color: #fff;"/>
    </div>
    <div class="typography-line pt-5">
    <p>정말 컸던 다른 문제는, 구상하고자 하는 서비스가 실제로 어느 환경에서 작동하는지 잘 고려하지 않았기 때문에 생긴 문제였다. <br/><br/>
    예를 들면 머신러닝 예측이 잘 진행되지 않아 시계열로 분석을 시도했는데, 시계열분석의 특성상 내가 예측하고자 하는 것이 대여대수라면 대여대수의 window가 제공되어야 한다.
    모델을 개발하는 환경에선 데이터가 이미 다 주어진 터라 대여대수의 window를 마련하는 것 따위는 문제가 되지 않겠지만, 실제로 서비스한다면 실시간으로 1시간 단위로 받아올 수 있는 정보는 
    서울시에서 제공하는 api였고, 거기서는 대여소의 자전거수 변화만 감지할 수 있었다. 그것은 유입량만을 계산할 수 있는 지표였고, 때문에 대여대수와 반납대수에서 매우 높은 계절성을 보여
    잘 해결될 것 같았던 시계열 분석은 무위로 돌아가게 되었다. 유입량을 이용한 시계열 분석은 트렌드와 계절성을 분리한 후에는 kpss 검정에서 정상성을 만족했지만, white noise의 특성을 보여
    window의 수를 몇으로 늘리던 이미 있는 모델보다 낮은 오차를 가지는 모델을 만드는데 실패했다.<br/><br/>
    또 딥러닝도 시도했다. LSTM모델은 시계열 자료를 훈련할 때 좋다고 알려져있었기 때문에, LSTM모델을 사용했으며 구현은 torch로, 여러가지 hyper parameter들을 바꿔가며 시도해 보았다.
    활성화 함수로는 ReLu, Optimizer는 ADAM, batch size는 2**10, learning_rate는 0.001, hidden_layer는 70일 때 최적이었고 또 어느정도는 더 좋은 예측을 내놓기는 했다.
    그러나 그 차이가 그렇게 크지 않았으며 colab에서 훈련에 필요한 데이터를 불러오는데 시간이 한참 들고 또 걸핏하면 꺼졌는데, 나중에는 이미 많이 이용했다며 gpu를 이용할 권한이 후순위로 밀려나
    2600개 모델을 훈련시킬 시간이 충분치 않아 다른 방법을 찾는 수밖에 없었다.<br/><br/>
    이런 문제들이 다 그렇듯이
      진작에 고려했다면 먼 길을 돌아가지 않아도 됐을 것이다. 지금 돌아보면, 좋은 모델을 찾기 위한 열정은 가득했지만 실제로 구동할 서비스의 한계점을 파악하는데 미진했다. 아마 다음 프로젝트를 진행하게 된다면, 이러한 삽질은 피할 수 있을 것이라고 생각한다.<br/><br/>
      
      </p>
    </div>
    <send-code number="2">
def MakeModels(samples, target):<br>
&nbsp; &nbsp; omittedset = []<br>
&nbsp; &nbsp; totalDataset = []<br>
&nbsp; &nbsp; N = len(samples)<br>
&nbsp; &nbsp; for number in samples:<br>
&nbsp; &nbsp; &nbsp; &nbsp; data = pd.concat([대여반납_2019[대여반납_2019['대여소']==number], 대여반납_2020[대여반납_2020['대여소']==number],<br>
&nbsp; &nbsp; &nbsp; &nbsp; 대여반납_2021[대여반납_2021['대여소']==number], 대여반납_2022[대여반납_2022['대여소']==number]], ignore_index=True, axis=0)<br>
&nbsp; &nbsp; &nbsp; &nbsp; open_day = pd.to_datetime(share_spot.loc[share_spot['대여소번호']==number, '대여소신설일']).iloc[0]<br>
&nbsp; &nbsp; &nbsp; &nbsp; weather['일시'] = pd.to_datetime(weather['일시'])<br>
&nbsp; &nbsp; &nbsp; &nbsp; since_day = (weather['일시']-open_day).dt.days<br>
&nbsp; &nbsp; &nbsp; &nbsp; since_day.name = '경과일'<br>
&nbsp; &nbsp; &nbsp; &nbsp; weather_since = pd.concat([weather ,since_day], axis=1)<br>
&nbsp; &nbsp; &nbsp; &nbsp; data = pd.merge(left=data, right=weather_since.loc[weather_since['경과일']&gt;=0], how='right', left_on = ['년','월','일','시'], right_on=['년','월','일','시'])<br>
&nbsp; &nbsp; &nbsp; &nbsp; data.drop(['일시','대여소','일','휴일_x'], axis=1, inplace=True)<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['대여횟수'] = data['대여횟수'].fillna(0)<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['반납횟수'] = data['반납횟수'].fillna(0)<br>
&nbsp; &nbsp; &nbsp; &nbsp; data.columns = ['시', '대여횟수', '반납횟수', '년', '월', '기온', '강수량(mm)', '풍속(m/s)',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;'습도(%)', '전운량(10분위)', '안개', '비 또는 눈', '연무', '휴일', '경과일']<br>
&nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['불쾌지수'] = (1.8*data['기온'] - 0.558*(1-data['습도(%)']/100)+(1.8*data['기온']-26)+32)<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['경과도'] = np.sqrt(1+data['경과일'])<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['2020년'] = (data['년']==2020).astype(int)<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['광도'] = ((data['시'] - data['월'].replace(일출시간)&gt;-1) &amp; (data['월'].replace(일몰시간) - data['시'] &gt;0.5)).astype(int) + ((data['시'] - data['월'].replace(일출시간)&gt;0) &amp; (data['월'].replace(일몰시간) - data['시'] &gt;0)).astype(int)-0.03*data['전운량(10분위)']<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['출근'] = ((data['시'].isin([7,8,9])).astype(int) + (data['시'].isin([8])).astype(int)*2)*(1-data['휴일'])<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['퇴근'] = ((data['시'].isin([17,18,19])).astype(int) + (data['시'].isin([18])).astype(int)*2)*(1-data['휴일'])<br>
&nbsp; &nbsp; &nbsp; &nbsp; data = data.drop([ '년', '경과일','연무','풍속(m/s)', '전운량(10분위)', '습도(%)','안개'], axis=1)<br>
<br>
&nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp; &nbsp; &nbsp; &nbsp; data['유출량'] = data['대여횟수']-data['반납횟수']<br>
<br>
&nbsp; &nbsp; &nbsp; &nbsp; window_Xs = data.loc[:,['유출량']]<br>
&nbsp; &nbsp; &nbsp; &nbsp; wait_X = data.drop(['유출량'], axis=1)<br>
&nbsp; &nbsp; &nbsp; &nbsp; return_col = [*wait_X.columns]<br>
&nbsp; &nbsp; &nbsp; &nbsp; <br>
&nbsp; &nbsp; &nbsp; &nbsp; window = 169+48<br>
&nbsp; &nbsp; &nbsp; &nbsp; window_X = window_Xs.loc[:,'유출량']<br>
&nbsp; &nbsp; &nbsp; &nbsp; wait_X = pd.concat([wait_X, pd.concat([window_X.shift(i) for i in range(window) if i%24&lt;=1 and i &gt;48], axis=1)], axis=1)<br>
&nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp; &nbsp; &nbsp; &nbsp; for i in range(window):<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if(i%24&lt;=1 and i &gt;48):<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; colname = '유출량'+'('+str(-i)+')'<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; return_col.append(colname)<br>
&nbsp; &nbsp; &nbsp; &nbsp; wait_X.columns = return_col<br>
&nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp; &nbsp; &nbsp; &nbsp; dataset = wait_X.iloc[window-1:]<br>
&nbsp; &nbsp; &nbsp; &nbsp; ohe_cal = []<br>
&nbsp; &nbsp; &nbsp; &nbsp; for cal in ['년', '월','시','요일']:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if cal in dataset.columns:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; ohe_cal.append(cal)<br>
&nbsp; &nbsp; &nbsp; &nbsp; dataset = pd.get_dummies(dataset, columns=ohe_cal)<br>
&nbsp; &nbsp; &nbsp; &nbsp; len_in_year = len(dataset)/24/365<br>
&nbsp; &nbsp; &nbsp; &nbsp; if len_in_year &gt; 1.95:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; test_len = 24*6*30<br>
&nbsp; &nbsp; &nbsp; &nbsp; elif len_in_year &gt; 1.6:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; test_len = 24*4*30<br>
&nbsp; &nbsp; &nbsp; &nbsp; else:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; test_len = int(len(dataset)*0.2)<br>
&nbsp; &nbsp; &nbsp; &nbsp; train_len = len(dataset)-test_len<br>
&nbsp; &nbsp; &nbsp; &nbsp; print('훈련데이터 : ', train_len, '검정데이터 : ', test_len)<br>
&nbsp; &nbsp; &nbsp; &nbsp;<br>
<br>
&nbsp; &nbsp; &nbsp; &nbsp; if(len_in_year&lt;1):<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; omittedset.append(number)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; continue<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp; &nbsp; &nbsp; &nbsp; mms = MinMaxScaler()<br>
&nbsp; &nbsp; &nbsp; &nbsp; X_train = dataset.drop(['대여횟수','반납횟수'],axis=1)<br>
&nbsp; &nbsp; &nbsp; &nbsp; y_train = dataset.loc[:,['대여횟수','반납횟수']]<br>
&nbsp; &nbsp; &nbsp; &nbsp; X_train = pd.DataFrame(mms.fit_transform(X_train)) &nbsp;#정규화<br>
&nbsp; &nbsp; &nbsp; &nbsp; y_train = y_train.loc[:,target]<br>
&nbsp; &nbsp; &nbsp; &nbsp; joblib.dump(mms, 'E:/seoulbike/scalers/seoulbike_mms_'+str(number)+'.pkl')<br>
&nbsp; &nbsp; &nbsp; &nbsp; totalDataset.append({"X_train" : X_train, 'y_train' : y_train, "number" : number})<br>
&nbsp; &nbsp; &nbsp; &nbsp; print(number, '번 데이터셋 준비')<br>
&nbsp; &nbsp; &nbsp; &nbsp;<br>
<br>
&nbsp; &nbsp; model = ZeroInflatedRegressor(<br>
&nbsp; &nbsp; classifier=LGBMClassifier(num_leaves=300, n_estimators=300, min_samples_leaf=15, max_depth=3, learning_rate=0.1) ,<br>
&nbsp; &nbsp; regressor=LGBMRegressor(max_depth=5, num_leaves=200, n_estimators=200, learning_rate=0.03<br>
&nbsp; &nbsp; ) &nbsp; <br>
&nbsp; &nbsp; )<br>
<br>
&nbsp; &nbsp; i = 0<br>
&nbsp; &nbsp; if target == '대여횟수':<br>
&nbsp; &nbsp; &nbsp; &nbsp; targetname = '대여'<br>
&nbsp; &nbsp; if target == '반납횟수':<br>
&nbsp; &nbsp; &nbsp; &nbsp; targetname = '반납'<br>
&nbsp; &nbsp; for dataset in totalDataset:<br>
&nbsp; &nbsp; &nbsp; &nbsp; i += 1<br>
&nbsp; &nbsp; &nbsp; &nbsp; print(i,"/",N,'번째 데이터 셋')<br>
&nbsp; &nbsp; &nbsp; &nbsp; model.fit(dataset['X_train'], dataset['y_train'])<br>
&nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp; &nbsp; &nbsp; &nbsp; joblib.dump(model, 'E:/seoulbike/models/seoulbike_'+str(dataset['number'])+'_'+targetname+'.pkl')<br>
<br>
&nbsp; &nbsp; return omittedset<br>
<br>
    </send-code>
    <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/1_yOB-iIj9INHDoNIIBFpYVA.png" class='frame' style="background-color: #fff;"/>
    </div>
 <div class="typography-line pt-5">
    <p>결과적으로 채택한 모델은 Zero Inflated Regressor였다. 위의 사진과 같이, ZIR는 분류기로 먼저 확실하게 0으로 결과가 나올 것 같은 경우를 걸러 낸 후,
      화귀를 한다. 그러므로 앞에서 언급했던 '0'이 많은 문제들을 어느정도 해결해 준다. 분류기를 선정할 때에는 0을 전부 걸러낼 수 있을거라 생각하지 않았기 때문에,
      확실한 0들을 찾기 위해 Accuracy를 scoring function으로 삼았다. <br><br>
      여러 분류기와 회귀기를 각각 비교하여 고른 결과 우연히 LGBMClassifier와 LGBMRegressor가 선정되었다. 1만개 이상의 데이터가 있을 경우를 상정한
      모델이므로 데이터의 수가 24*365(1년)보다 적은 경우에는 모델을 생성하지 않았다. 그 경우에는 웹페이지에서 '데이터의 부족으로 인해 예측을 제공하지 않는다'는
      알림을 볼 수 있을 것이다.
    
    </p>
    </div>
        <div class="d-flex justify-content-center">
      <object data="http://localhost:8000/static/figures/sample2_borrow_mae.html"
  width="700"
  height="400"
  type="text/html">
  </object>
      <object data="http://localhost:8000/static/figures/sample2_7window_borrow_zir_mae.html"
  width="700"
  height="400"
  type="text/html">
  </object>
    </div>
 <div class="typography-line pt-5">
    <p>
      최종 채택한 모델에서 사용한 feature는 다음과 같다. 월과 시는 원핫인코딩을 했다. 또 유출량 window를 사용해
      대여횟수와 반납횟수를 예측하는데, window가 있는 편이 더 좋은 예측을 보여주는 것을 확인했다. '유출량(-49)'는 49시간 이전의 유출량을 의미한다.
      1시간 전, 24시간 전이 아니라 49시간 전의 유출량부터 사용한 이유는 서비스에서 제공하고자 하는 예측이 향후 48시간 동안이고, 48시간 후의 예측에서 1시간 전의
      window를 사용한다면 지금 가지고 있지 않은, 47시간 이후의 정보를 사용해야 하는 꼴이 되므로 다음과 같이 216시간 전부터 49시간 전까지 1주일간의 window를 사용했다.<br/><br/>

      '기온', '강수량(mm)', '비 또는 눈', '휴일', '불쾌지수', '경과도', '2020년', '광도', '출근',
       '퇴근', '유출량(-49)', '유출량(-72)', '유출량(-73)', '유출량(-96)', '유출량(-97)',
       '유출량(-120)', '유출량(-121)', '유출량(-144)', '유출량(-145)', '유출량(-168)',
       '유출량(-169)', '유출량(-192)', '유출량(-193)', '유출량(-216)', '월', '시'<br/><br/>

      결과적으로 hyper parameter를 이미 조율한 이전의 모델보다 거의 20% 더 좋은 예측을 보여주었다. 보팅과 블렌딩의 방법을 시도해 보았으나, 큰 차이는 없는 것으로 드러나
      최종 모델로 선정하지 않았다.<br/><br/>
    
    
    </p>
    </div>
    <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/backend-logic.png" class='frame' style="background-color: #fff;"/>
    </div>
<div class="typography-line pt-5">
    <p>
      최종모델로 각 대여소마다 데이터를 훈련한 후, 스케일러와 같이 pkl로 저장해 두었다. 백엔드 로직에서는 사용자가 예측 결과를 요청할 때마다
      다음과 같은 프로세스가 실행된다. 매 시간 최초 cronjob을 실행하고 범용dataframe을 만드는 부분에서 약 1초정도 소요되지만, 그 이후로는 
      0.3초 이내로 임의의 대여소의 예측결과를 제공해준다. 만약 이미 예측된적 있는 대여소라면 저장해둔 결과를 전달해주므로 속도가 훨씬 더 빠르다.<br/><br/>
    
    
    </p>
    </div>

    </card>

    <component v-for="item in components" :is="item.component" :key="item.id"></component>

    <div ref="endofcontent" class="text-center">
      <p  v-if="!loading">
        이 컨텐츠의 마지막 페이지입니다.
      </p>
      <div class="ms-auto">
        <Spinner :loading="loading"></Spinner>
      </div>
    </div>
  </div>
</template>

<script>
import BaseButton from '../components/BaseButton.vue';
import Spinner from '../components/Spinner.vue';
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue';

export default {
  components: {
    BaseButton,
    Spinner,
    sendCode,
    receiveCode
},
  data (){
    return {
      tab : 1,
      topicData: [],
      components: [],
      loading : true,
    }
  },
  mounted() {
    this.$refs.scroll.scrollIntoView();
    const endofcontent = this.$refs.endofcontent;
    let self = this
    const io = new IntersectionObserver(function(entries, observer){
        if(entries[0].isIntersecting){
          let promise = () => import(`src/components/Analysis/dynamic/MachineLearning/${self.paddedTab}`)
      promise().then((res)=>{
          setTimeout(()=>{
            const component_id = `dynamic-component-${self.paddedTab}`  
          self.components.push({
            component : res.default,
            id: component_id     
          });
          self.tab += 1
            }, 500)
        }).catch((err)=>{ 
          observer.unobserve(entries[0].target)
          self.loading = false
      })
        }
      }, {
      root: null,
      rootMargin: '100px',
      threshold: 0.1
      })
      io.observe(endofcontent);
      },
  computed : {
    paddedTab : function(){
      return ('00' + this.tab).slice(-3)
      }
  },
  method : {
  }


}

</script>

<style>
.frame{
  border: 5px solid rgb(190, 190, 190);
  padding: 0px;
}

p{
  line-height: 33px;
}
</style>