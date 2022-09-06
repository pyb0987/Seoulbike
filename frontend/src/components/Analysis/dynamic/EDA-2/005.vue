<template>
   <card class="pt-4">
    <send-code number="18">

spot_date.loc[spot_date['대여일자']&lt;'2018-07-05', '대여일자'] = '2018-01-01'<br>
spot_date.columns = ['번호', '대여소신설일']<br>
share_spot = pd.merge(left=share_spot, right=spot_date, how='left', left_on = '대여소번호', right_on = '번호').drop(['index','번호','연','월','일'], axis=1)<br>
<br>
daily_use = pd.merge(left=daily_use, right=spot_date, left_on = '번호', right_on='번호')<br>
daily_use['대여일자'] = pd.to_datetime(daily_use['대여일자'])<br>
daily_use['대여소신설일'] = pd.to_datetime(daily_use['대여소신설일'])<br>
daily_use['경과일'] = (daily_use['대여일자'] - daily_use['대여소신설일'])<br>
<br>
day_spot_df = daily_use.groupby(['대여일자','번호']).sum().reset_index().loc[:,['대여일자', '번호', '이용건수']]<br>
day_spot_df = pd.merge(left=day_spot_df, right=spot_date, left_on = '번호', right_on='번호')<br>
day_spot_df['대여소신설일'] = pd.to_datetime(day_spot_df['대여소신설일'])<br>
day_spot_df['경과일'] = (day_spot_df['대여일자'] - day_spot_df['대여소신설일'])<br>
day_spot_df['경과일'] = day_spot_df['경과일'].dt.days<br>
<br>
stats.spearmanr(day_spot_df['이용건수'],day_spot_df['경과일'])<br>
<br>
<br>

    </send-code>
  <recieve-code>
    SpearmanrResult(correlation=0.14838047761597012, pvalue=0.0)
  </recieve-code>
      <div class="typography-line">
        
    <p>
      <strong>
        귀무가설 : 이용건수와 경과일의 상관계수는 0이다. <br>
      대립가설 : 이용건수와 경과일은 상관계수는 0이 아니다.<br><br>
      </strong>
pvaule는 0.0으로 상관관계가 있다는 것이 드러났다. 다만 0.15의 상관계수는 매우 작은데, 단조성만 유지하면 되므로 정규화가 쉽다는 점을 고려하여 우선은 모델을 만들때 포함시키도록 하자
우선은 이정도로 하고 본격적인 로그데이터 분석에 들어가도록 하자.

    </p>
    </div>
    <div class="typography-line">
      <hr>
    <h3>로그 데이터 톺아보기</h3>
    </div>
  <send-code number="19">
log_data2019 = getAllCsvDask('로그/2019년',dtype={'대여거치대': 'object',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'반납대여소번호': 'object',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'이용거리': 'float64', '이용시간': 'float64'}<br>
)<br>
log_data2020 = getAllCsvDask('로그/2020년',dtype={'대여거치대': 'object',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'반납대여소번호': 'object',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'이용거리': 'float64', '이용시간': 'float64'}<br>
)<br>
log_data2021 = getAllCsvDask('로그/2021년',dtype={'대여거치대': 'object',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'반납대여소번호': 'object',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'이용거리': 'float64', '이용시간': 'float64'}<br>
)<br>
log_data2022 = getAllCsvDask('로그/2022년',dtype={'대여거치대': 'object',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'반납대여소번호': 'object',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'이용거리': 'float64', '이용시간': 'float64'}<br>
)<br>
<br>
for i in range(len(log_data2019)):<br>
&nbsp; &nbsp; log_data2019[i].columns = ['자전거번호', '대여일시', '대여대여소번호', '대여대여소명', '대여거치대','반납일시','반납대여소번호', '반납대여소명', '반납거치대','이용시간', '이용거리']<br>
log_data2019 = pd.concat(log_data2019)<br>
for i in range(len(log_data2020)):<br>
&nbsp; &nbsp; log_data2020[i].columns = ['자전거번호', '대여일시', '대여대여소번호', '대여대여소명', '대여거치대','반납일시','반납대여소번호', '반납대여소명', '반납거치대','이용시간', '이용거리']<br>
log_data2020 = pd.concat(log_data2020)<br>
for i in range(len(log_data2021)):<br>
&nbsp; &nbsp; log_data2021[i].columns = ['자전거번호', '대여일시', '대여대여소번호', '대여대여소명', '대여거치대','반납일시','반납대여소번호', '반납대여소명', '반납거치대','이용시간', '이용거리']<br>
log_data2021 = pd.concat(log_data2021)<br>
for i in range(len(log_data2022)):<br>
&nbsp; &nbsp; log_data2022[i].columns = ['자전거번호', '대여일시', '대여대여소번호', '대여대여소명', '대여거치대','반납일시','반납대여소번호', '반납대여소명', '반납거치대','이용시간', '이용거리']<br>
log_data2022 = pd.concat(log_data2022)<br>
<br>
log_data2019 = log_data2019.reset_index().drop('index', axis=1)<br>
log_data2020 = log_data2020.reset_index().drop('index', axis=1)<br>
log_data2021 = log_data2021.reset_index().drop('index', axis=1)<br>
log_data2022 = log_data2022.reset_index().drop('index', axis=1)<br>
<br>
#망가진 컬럼 복구<br>
broken_index = log_data2019[log_data2019['대여거치대'].astype(str).str.len() &gt;4].index<br>
log_data2019.loc[broken_index, '이용거리'] = log_data2019.loc[broken_index, '이용시간']<br>
log_data2019.loc[broken_index, '이용시간'] = log_data2019.loc[broken_index, '반납거치대']<br>
log_data2019.loc[broken_index, '반납거치대'] = log_data2019.loc[broken_index, '반납대여소명']<br>
log_data2019.loc[broken_index, '반납대여소명'] = log_data2019.loc[broken_index, '반납대여소번호']<br>
log_data2019.loc[broken_index, '반납대여소번호'] = log_data2019.loc[broken_index, '반납일시']<br>
log_data2019.loc[broken_index, '반납일시'] = log_data2019.loc[broken_index, '대여거치대']<br>
broken_index = log_data2020[log_data2020['대여거치대'].astype(str).str.len() &gt;4].index<br>
log_data2020.loc[broken_index, '이용거리'] = log_data2020.loc[broken_index, '이용시간']<br>
log_data2020.loc[broken_index, '이용시간'] = log_data2020.loc[broken_index, '반납거치대']<br>
log_data2020.loc[broken_index, '반납거치대'] = log_data2020.loc[broken_index, '반납대여소명']<br>
log_data2020.loc[broken_index, '반납대여소명'] = log_data2020.loc[broken_index, '반납대여소번호']<br>
log_data2020.loc[broken_index, '반납대여소번호'] = log_data2020.loc[broken_index, '반납일시']<br>
log_data2020.loc[broken_index, '반납일시'] = log_data2020.loc[broken_index, '대여거치대']<br>
broken_index = log_data2021[log_data2021['대여거치대'].astype(str).str.len() &gt;4].index<br>
log_data2021.loc[broken_index, '이용거리'] = log_data2021.loc[broken_index, '이용시간']<br>
log_data2021.loc[broken_index, '이용시간'] = log_data2021.loc[broken_index, '반납거치대']<br>
log_data2021.loc[broken_index, '반납거치대'] = log_data2021.loc[broken_index, '반납대여소명']<br>
log_data2021.loc[broken_index, '반납대여소명'] = log_data2021.loc[broken_index, '반납대여소번호']<br>
log_data2021.loc[broken_index, '반납대여소번호'] = log_data2021.loc[broken_index, '반납일시']<br>
log_data2021.loc[broken_index, '반납일시'] = log_data2021.loc[broken_index, '대여거치대']<br>
broken_index = log_data2022[log_data2021['대여거치대'].astype(str).str.len() &gt;4].index<br>
<br>
log_data2019.drop(['대여대여소명','반납대여소명','대여거치대','반납거치대'], axis=1, inplace=True)<br>
log_data2020.drop(['대여대여소명','반납대여소명','대여거치대','반납거치대'], axis=1, inplace=True)<br>
log_data2021.drop(['대여대여소명','반납대여소명','대여거치대','반납거치대'], axis=1, inplace=True)<br>
log_data2022.drop(['대여대여소명','반납대여소명','대여거치대','반납거치대'], axis=1, inplace=True)<br>
<br>
#행의 타입을 지정<br>
log_data2019['반납대여소번호'] = log_data2019['반납대여소번호'].astype(int)<br>
log_data2022['반납대여소번호'] = log_data2022['반납대여소번호'].astype(int)<br>
log_data2020['반납대여소번호'] = log_data2020['반납대여소번호'].astype(int)<br>
log_data2021['반납대여소번호'] = log_data2021['반납대여소번호'].astype(int)<br>
<br>
log_data2022['대여일시'] = pd.to_datetime(log_data2022['대여일시'], format='%Y-%m-%d %H:%M')<br>
log_data2022['반납일시'] = pd.to_datetime(log_data2022['반납일시'], format='%Y-%m-%d %H:%M')<br>
log_data2021['대여일시'] = pd.to_datetime(log_data2021['대여일시'], format='%Y-%m-%d %H:%M')<br>
log_data2021['반납일시'] = pd.to_datetime(log_data2021['반납일시'], format='%Y-%m-%d %H:%M')<br>
log_data2020['대여일시'] = pd.to_datetime(log_data2020['대여일시'], format='%Y-%m-%d %H:%M')<br>
log_data2020['반납일시'] = pd.to_datetime(log_data2020['반납일시'], format='%Y-%m-%d %H:%M')<br>
log_data2019['대여일시'] = pd.to_datetime(log_data2019['대여일시'], format='%Y-%m-%d %H:%M')<br>
log_data2019['반납일시'] = pd.to_datetime(log_data2019['반납일시'], format='%Y-%m-%d %H:%M')<br>
log_data2022['자전거번호'].str.contains('SPB').value_counts() #전부 SPB이 붙어있으므로 SPB제거<br>
log_data2019['자전거번호'] = log_data2019['자전거번호'].str.slice(4).astype(int)<br>
log_data2020['자전거번호'] = log_data2020['자전거번호'].str.slice(4).astype(int)<br>
log_data2021['자전거번호'] = log_data2021['자전거번호'].str.slice(4).astype(int)<br>
log_data2022['자전거번호'] = log_data2022['자전거번호'].str.slice(4).astype(int)<br>
<br>
log_data2020.head()<br>
  </send-code>
    <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/log_data_2020_before.png" class='frame'/>
    </div>


  <div class="typography-line pt-5">
    <p>
      데이터가 너무 많아 19.1월부터 22.6월까지의 데이터만 이용하기로 했다. 열이 너무 많아서 각 년도별로 따로 실행하지 않으면
      렉이 걸리거나 심지어는 커널이 죽어버려서 따로따로 실행했다.<br><br>

      이용거리가 0미터로 잡히는 경우는 결측치로 보고 처리해야하지만 
      우선 그 이전에 자전거가 대여소에서 다른 대여소로 이동하는 이력이 모두 잡히는지 확인해본다.
      만약에 자전거가 한 곳에서 다른 곳으로 이동하는 모든 때가 기록이 되어있다면, 자전거의 유입, 유출량 뿐 아니라
      대여소별 최저치를 0으로 삼아 각 시간마다의 자전거 보유 대수를 손쉽게 알아낼 수 있을 것이다.<br><br>

      확인방식은 시간순으로 정렬된 로그에서 특정 번호의 자전거를 빌릴 때 
      이전에 반납했던 위치에 그대로 있었는지 확인하는 식이다. 
      그러나 예상하건대, 트럭으로 옮기거나 정비가는 경우가 있어서 갑자기 자전거의 위치가 점프하는 경우가 있을 것이다. 그 비율이 높지 않기를 바래본다.
    </p>
    </div>
    <send-code number="20">

check_data = log_data2020.sort_values('대여일시')<br>
num_error = 0<br>
location = [0 for i in range(100000)]<br>
for bicycle_num, start_location, end_location in zip(check_data['자전거번호'], check_data['대여대여소번호'], check_data['반납대여소번호']):<br>
&nbsp; &nbsp; if location[bicycle_num] != start_location and location[bicycle_num] != 0:<br>
&nbsp; &nbsp; &nbsp; &nbsp; num_error += 1<br>
&nbsp; &nbsp; location[bicycle_num] = end_location<br>
print('에러율 &nbsp;:', num_error/len(check_data['자전거번호'])*100, '%')<br>
  </send-code>
  <recieve-code>
    에러율 : 5.145014599793885 %
  </recieve-code>
<div class="typography-line">
    <p>
      에러율이 너무 높아서 자전거의 이력으로부터 대여소의 자전거 개수를 파악하려는 시도는 사실상 반려된다. 따라서 더 이상 미련을 두지 않고, 이상치를 전부 제거했다.
    </p>
    </div>
    <send-code number="21">
log_data2019 = log_data2019[(log_data2019['이용시간']&gt;0) &amp; ((log_data2019['이용거리'])&lt;100000) &amp; ((log_data2019['이용거리']/log_data2019['이용시간'])&lt;700) &amp; ((log_data2019['이용시간'])&lt;240)]<br>
log_data2019 = log_data2019[(log_data2019['대여대여소번호'] &lt; 9000) &amp; (log_data2019['대여대여소번호'] &gt; 100) &amp; (log_data2019['반납대여소번호'] &lt; 9000) &amp; (log_data2019['반납대여소번호'] &gt; 100)]<br>
log_data2020 = log_data2020[(log_data2020['이용시간']&gt;0) &amp; ((log_data2020['이용거리'])&lt;100000) &amp; ((log_data2020['이용거리']/log_data2020['이용시간'])&lt;700) &amp; ((log_data2020['이용시간'])&lt;240)]<br>
log_data2020 = log_data2020[(log_data2020['대여대여소번호'] &lt; 9000) &amp; (log_data2020['대여대여소번호'] &gt; 100) &amp; (log_data2020['반납대여소번호'] &lt; 9000) &amp; (log_data2020['반납대여소번호'] &gt; 100)]<br>
log_data2021 = log_data2021[(log_data2021['이용시간']&gt;0) &amp; (log_data2021['이용거리'] &gt; 0.01) &amp; ((log_data2021['이용거리'])&lt;100000) &amp; ((log_data2021['이용거리']/log_data2021['이용시간'])&lt;700) &amp; ((log_data2021['이용시간'])&lt;240)]<br>
log_data2021 = log_data2021[(log_data2021['대여대여소번호'] &lt; 9000) &amp; (log_data2021['대여대여소번호'] &gt; 100) &amp; (log_data2021['반납대여소번호'] &lt; 9000) &amp; (log_data2021['반납대여소번호'] &gt; 100)]<br>
log_data2022 = log_data2022[(log_data2022['이용시간']&gt;0) &amp; (log_data2022['이용거리'] &gt; 0.01) &amp; ((log_data2022['이용거리'])&lt;100000) &amp; ((log_data2022['이용거리']/log_data2022['이용시간'])&lt;700) &amp; ((log_data2022['이용시간'])&lt;240)]<br>
log_data2022 = log_data2022[(log_data2022['대여대여소번호'] &lt; 9000) &amp; (log_data2022['대여대여소번호'] &gt; 100) &amp; (log_data2022['반납대여소번호'] &lt; 9000) &amp; (log_data2022['반납대여소번호'] &gt; 100)]<br>
<br>
log_data2019['대여일시'] = pd.to_datetime(log_data2019['대여일시'])<br>
log_data2019['반납일시'] = pd.to_datetime(log_data2019['반납일시'])<br>
log_data2020['대여일시'] = pd.to_datetime(log_data2020['대여일시'])<br>
log_data2020['반납일시'] = pd.to_datetime(log_data2020['반납일시'])<br>
log_data2021['대여일시'] = pd.to_datetime(log_data2021['대여일시'])<br>
log_data2021['반납일시'] = pd.to_datetime(log_data2021['반납일시'])<br>
log_data2022['대여일시'] = pd.to_datetime(log_data2022['대여일시'])<br>
log_data2022['반납일시'] = pd.to_datetime(log_data2022['반납일시'])<br>
    </send-code>
  <div class="typography-line pt-5">
    <p>
      이상치를 제거한 기준은 다음과 같다.<br><br>
      이용시간 : 0분 초과, 4시간 미만(2시간이 이용권 최대 시간이므로) <br>
      이용거리 : 0m 초과, 100km 미만<br>
      속도 : 42km/h미만<br>
      대여소번호 : 100이하 또는 9000이상 제외<br><br>
다만 2020년 자료는 이용거리가 0m로 나오는 자료가 전체의 60퍼센트이므로 로그데이터는 그대로 유지하되 이용시간 분석에서 제외했다.

    </p>
    </div>


   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue';
import RecieveCode from '../../recieveCode.vue';

export default {
    name : 'dynamic-005',
  components: {
    sendCode,
    receiveCode,
    RecieveCode
},
  data() {
    return {

    };
  }
};
</script>