<template>
   <card class="pt-4">
    <send-code number="29">

fig = px.density_heatmap(pd.concat([hour_2021_대여, hour_2021_반납]), x="시", y="자치구", z="유입량", facet_row="요일", histfunc="avg")<br>
fig.update_layout( &nbsp; <br>
&nbsp; &nbsp; width=900,<br>
&nbsp; &nbsp; height = 800,<br>
&nbsp; &nbsp; title='자치구별 시간별 대여소당 자전거 유입량 추이')<br>
fig.show()<br>
    </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/dist_hourly_inflow.html"
  width="925"
  height="830"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="typography-line pt-5">
    <p>
      자치구별로 유입량을 나눠서 살펴보면 큰 차이가 있는 지역들이 있었다. 예를들면 제일 노란색에 가까운 순으로 성동구, 영등포구, 
      중구 등은 사람들이 많이 도착하는 쪽이고 제일 파란색에 가까운 순으로 광진구, 서대문구, 성북구 등은 사람들이 많이 출발하는 편이었다.
      본인은 광진구에 거주중이므로, 평일 아침에 자전거를 빌리기 위해 갔을 때 자전거가 없으면 기다려도 소용이 없다는 것을 알 수 있었다. 
      그러나 다수의 자치구는 별로 유입, 유출이 보이지 않는 듯 했다.<br/><br/>

      자치구의 비교에서 무언가를 얻을 수 있을 거라는 기대는 앞으로는 하지 않는 것이 낫겠다.
자치구 내의 주거지역에서 상업지역으로 출근하는 경향이 있다고 가정하면 그러므로 아마 자치구별 히트맵에서 기대하던 결과는, 개별 대여소에 대한 비교에서 볼 수 있을 것 같다.

    </p>
    </div>

  <send-code number="30">
(time_split_2021['대여대여소번호']==time_split_2021['반납대여소번호']).value_counts()
  </send-code>
  <receive-code>
False &nbsp; &nbsp;23664913<br>
True &nbsp; &nbsp; &nbsp;2530740<br>
dtype: int64<br>
  </receive-code>
    <send-code number="31">
dist_hour_대여 = time_split_2021.copy()<br>
dist_hour_대여['대여요일'] = dist_hour_대여['대여요일'].replace({0: '평일',1: '평일',2: '평일',3: '평일',4: '평일',5: '휴일',6: '휴일' })<br>
dist_hour_대여 = dist_hour_대여.groupby(['대여요일', '대여시','대여대여소번호']).size()<br>
dist_hour_대여.name = '대여횟수'<br>
dist_hour_반납 = time_split_2021.copy()<br>
dist_hour_반납['반납요일'] = dist_hour_반납['반납요일'].replace({0: '평일',1: '평일',2: '평일',3: '평일',4: '평일',5: '휴일',6: '휴일' })<br>
dist_hour_반납 = dist_hour_반납.groupby(['반납요일', '반납시','반납대여소번호']).size()<br>
dist_hour_반납.name = '반납횟수'<br>
<br>
dist_hour_대여반납 = pd.concat([dist_hour_대여,dist_hour_반납], axis=1)<br>
del dist_hour_대여<br>
del dist_hour_반납<br>
dist_hour_대여반납['유출량'] = dist_hour_대여반납['대여횟수'] - dist_hour_대여반납['반납횟수']<br>
dist_hour_대여반납 = dist_hour_대여반납.reset_index()<br>
dist_hour_대여반납.columns = ['이용요일', '이용시', '대여소', '대여횟수', '반납횟수', '유출량']<br>
dist_hour_대여반납 = dist_hour_대여반납[dist_hour_대여반납['이용요일']=='평일'].pivot(index='대여소',columns='이용시', values='유출량').fillna(0)<br>
<br>
fig = dash_bio.Clustergram(<br>
&nbsp; &nbsp; data=np.cbrt(dist_hour_대여반납),<br>
&nbsp; &nbsp; cluster='row',<br>
&nbsp; &nbsp; column_labels=list(dist_hour_대여반납.columns.values),<br>
&nbsp; &nbsp; row_labels=list(dist_hour_대여반납.index),<br>
&nbsp; &nbsp; height=800,<br>
&nbsp; &nbsp; width=1000,<br>
&nbsp; &nbsp; &nbsp;color_map= [<br>
&nbsp; &nbsp; &nbsp; &nbsp; [0.0, "#ffffff"],<br>
&nbsp; &nbsp; &nbsp; &nbsp; [0.35, "#e5e5e5"],<br>
&nbsp; &nbsp; &nbsp; &nbsp; [0.55, "#fca311"],<br>
&nbsp; &nbsp; &nbsp; &nbsp; [0.85, "#14213d"],<br>
&nbsp; &nbsp; &nbsp; &nbsp; [1.0, "#000000"]],<br>
&nbsp; &nbsp; hidden_labels='row',<br>
<br>
)<br>
fig.update_layout( &nbsp; <br>
&nbsp; &nbsp; title='시간별 대여소별 자전거 유입량 클러스터 맵')<br>
fig.show()<br>
  </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/dist_hourly_inflow_cluster.html"
  style="background-color : #fff"
  width="1020"
  height="830"
  class="frame"
  type="text/html">
  </object>
  </div>


  <div class="typography-line pt-5">
    <p>
      유출량에 대한 클러스터맵을 작성했다. 편차가 매우 커서 나타낸 양은 유출량의 세제곱근이다.
      유의미한 클러스터가 두개 관찰되는 것을 볼 수 있다. 위쪽은 오전에 많이 유출된 후 오후
       유입되는 경향을 보이고 아래쪽은 오전에 많이 유입된 후, 오후 유출되는 경향을 보였다.
      가운데에도 클러스터가 하나 있는 것처럼 보인다. 시간대에 고르게 유출관 유입이 있는 대여소들이다. 
      그러나 차트의 클러스터 생성함수에는 감지되지 않았다.
어느 시간대에서나 빠져나가는 쪽의 대여소는 그 비율이 더 적고, 그러므로 많이 빠져나갔다. 
나타내어진 값은 세제곱근이므로 넓게 분포해있는 '5'들의 값은 125, 그리고 좁은 '-10'이하의 값들은 사실상 1000이 넘는 유출량을 의미한다.<br><br>

자치구마다의 유출량이 사실상 대여소에 주는 영향이 미미하다고 볼 수 있으므로, 또 유의미한 클러스터링이 존재하는 것으로 보이므로
 대여소 자체의 경향을 파악하는 쪽으로 가닥을 잡아야 하겠다.

    </p>
    </div>
    <send-code number="32">

weather = getAllCsvDask('날씨')<br>
for i in range(len(weather)):<br>
&nbsp; &nbsp; weather[i].columns = ['지점', '지점명', '일시', '기온', '강수량(mm)','풍속(m/s)','습도(%)', '전운량(10분위)', '현상번호']<br>
weather = pd.concat(weather)<br>
weather['현상번호'] = weather['현상번호'].fillna(0).astype(int).astype(str)<br>
weather.loc[weather['현상번호'].str.len()%2 ==1,'현상번호'] = '0'+weather[weather['현상번호'].str.len()%2 ==1]['현상번호']<br>
weatherDict = {'00' : '없음', '01':'비', '02':'비', '03':'비', '04':'비', '05':'눈', '06':'눈', '07':'비', '08':'눈',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;'09':'눈', '10':'눈', '11':'눈', '12':'비', '13':'우박', '14':'우박', '15':'우박', '16':'안개', '17':'안개',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; '18':'안개', '19':'안개', '20':'눈', '21':'눈', '22':'눈', '23':'이슬', '24':'이슬', '25':'서리', '26':'서리',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;'27':'서리', '28':'서리', '29':'서리','30':'서리', '31':'서리', '32':'서리', '33':'기타', '34':'서리',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; '35':'서리', '36' : '서리', '40':'연무', '41':'연무', '42':'연무', '43':'연무', '44':'연무', '45':'연무', '46':'연무', '47':'연무', '48':'연무',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;'50' : '기타', '51':'기타', '52' : '기타', '53':'기타', '54' : '기타', '55':'기타', '56' : '기타', '57':'기타', '58' : '기타', '59':'기타',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;'60':'기타'}<br>
weather['현상번호'] = weather['현상번호'].str.extract('([0-9]{2})([0-9]{2})?([0-9]{2})?').replace(weatherDict).apply(lambda x: ', '.join(x.dropna().values.tolist()), axis=1)<br>
weather['현상번호'] = weather['현상번호'].replace({'안개, 비, 비':'안개, 비', '안개, 안개, 비' : '안개, 비', '안개, 눈, 눈' : '안개, 눈 ', '눈, 눈, 비': '눈, 비' ,'연무, 연무, 눈': '연무, 눈'})<br>
weather['강수량(mm)'].fillna(method='bfill', limit=2, inplace=True)<br>
weather['전운량(10분위)'].fillna(method='bfill', limit=2, inplace=True)<br>
weather['강수량(mm)'].replace(0.0, 0.1, inplace=True)<br>
weather.loc[~(weather['현상번호'].str.contains('눈')) &amp; ~(weather['현상번호'].str.contains('비')),'강수량(mm)'] = 0.0<br>
#강수량 관측이 3시간마다 이루어지는 경우가 있으므로 2칸까지 채운다.<br>
#전운량 또한 같이 처리한다.<br>
#현상번호가 붙은 경우에는 0,1미만이더라도 올림하여 0,1로하고<br>
#결측값(비가 오지않은 경우)을 0.0으로 채운다.<br>
<br>
weather['안개'] = weather['현상번호'].str.contains('안개').replace({False:0, True:1})<br>
weather['비'] = weather['현상번호'].str.contains('비').replace({False:0, True:1})<br>
weather['눈'] = weather['현상번호'].str.contains('눈').replace({False:0, True:1})<br>
weather['비 또는 눈'] = 1-(1-weather['비'])*(1-weather['눈'])<br>
weather['연무'] = weather['현상번호'].str.contains('연무').replace({False:0, True:1})<br>
weather.drop(['지점', '지점명', '현상번호', '비', '눈'], axis=1, inplace=True)<br>
weather['일시'] = pd.to_datetime(weather['일시'])<br>
weather['년'] = weather['일시'].dt.year<br>
weather['월'] = weather['일시'].dt.month<br>
weather['일'] = weather['일시'].dt.day<br>
weather['시'] = weather['일시'].dt.hour<br>
weather['휴일'] = weather['일시'].dt.day_of_week.replace({0: 0,1: 0,2: 0,3: 0,4: 0,5: 1,6: 1 })<br>
weather.loc[weather['기온'].isna(), '기온'] = 34.0 &nbsp;#직접 검색해서 넣음<br>
weather.loc[weather['강수량(mm)'].isna(), '강수량(mm)'] = 0.1<br>
weather['풍속(m/s)'].fillna(0.0, inplace=True)<br>
weather.info()<br>
  </send-code>
  <receive-code>
&lt;class 'pandas.core.frame.DataFrame'&gt;<br>
Int64Index: 30648 entries, 0 to 4343<br>
Data columns (total 14 columns):<br>
&nbsp;# &nbsp; Column &nbsp; &nbsp; Non-Null Count &nbsp;Dtype &nbsp; &nbsp; &nbsp; &nbsp;<br>
--- &nbsp;------ &nbsp; &nbsp; -------------- &nbsp;----- &nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp;0 &nbsp; 일시 &nbsp; &nbsp; &nbsp; &nbsp; 30648 non-null &nbsp;datetime64[ns]<br>
&nbsp;1 &nbsp; 기온 &nbsp; &nbsp; &nbsp; &nbsp; 30648 non-null &nbsp;float64 &nbsp; &nbsp; &nbsp;<br>
&nbsp;2 &nbsp; 강수량(mm) &nbsp; &nbsp;30648 non-null &nbsp;float64 &nbsp; &nbsp; &nbsp;<br>
&nbsp;3 &nbsp; 풍속(m/s) &nbsp; &nbsp;30648 non-null &nbsp;float64 &nbsp; &nbsp; &nbsp;<br>
&nbsp;4 &nbsp; 습도(%) &nbsp; &nbsp; &nbsp;30648 non-null &nbsp;float64 &nbsp; &nbsp; &nbsp;<br>
&nbsp;5 &nbsp; 전운량(10분위) &nbsp;30648 non-null &nbsp;float64 &nbsp; &nbsp; &nbsp;<br>
&nbsp;6 &nbsp; 안개 &nbsp; &nbsp; &nbsp; &nbsp; 30648 non-null &nbsp;int64 &nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp;7 &nbsp; 비 또는 눈 &nbsp; &nbsp; 30648 non-null &nbsp;int64 &nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp;8 &nbsp; 연무 &nbsp; &nbsp; &nbsp; &nbsp; 30648 non-null &nbsp;int64 &nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp;9 &nbsp; 년 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;30648 non-null &nbsp;int64 &nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp;10 &nbsp;월 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;30648 non-null &nbsp;int64 &nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp;11 &nbsp;일 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;30648 non-null &nbsp;int64 &nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp;12 &nbsp;시 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;30648 non-null &nbsp;int64 &nbsp; &nbsp; &nbsp; &nbsp;<br>
&nbsp;13 &nbsp;휴일 &nbsp; &nbsp; &nbsp; &nbsp; 30648 non-null &nbsp;int64 &nbsp; &nbsp; &nbsp; &nbsp;<br>
dtypes: datetime64[ns](1), float64(5), int64(8)<br>
memory usage: 3.5 MB<br>
  </receive-code>

<div class="typography-line">
    <p>
      이제 실제 예측을 수행하기 위해 날씨 데이터를 추가했다. 앞에서 본 것처럼 최소한 비가 오는지의 여부는 굉장히 중요한 변수이며
      실제로 맞는 예측을 하기 위해서는 포함하지 않을 수 없다.
      서리, 황사와 같은 카테고리들을 모두 합쳐 안개 또는 연무로 통합하였으며 결측치들을 이전의 관측치를 근거로 하여 채워 넣었다.  
    </p>
    </div>



   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue';

export default {
    name : 'dynamic-008',
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