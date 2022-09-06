<template>
   <card class="pt-4">
    <send-code number="22">
time_split_2021 = log_data2021.copy()<br>
<br>
time_split_2021['대여월'] = time_split_2021['대여일시'].dt.month<br>
time_split_2021['대여요일'] = time_split_2021['대여일시'].dt.day_of_week<br>
time_split_2021['대여일'] = time_split_2021['대여일시'].dt.day<br>
time_split_2021['대여시'] = time_split_2021['대여일시'].dt.hour<br>
time_split_2021['반납월'] = time_split_2021['반납일시'].dt.month<br>
time_split_2021['반납요일'] = time_split_2021['반납일시'].dt.day_of_week<br>
time_split_2021['반납일'] = time_split_2021['반납일시'].dt.day<br>
time_split_2021['반납시'] = time_split_2021['반납일시'].dt.hour<br>
time_split_2021.drop(['자전거번호', '대여일시', '반납일시'], axis=1, inplace=True)<br>
time_split_2021 = pd.merge(left=time_split_2021, right=share_spot.loc[:,['대여소번호','자치구']], left_on='대여대여소번호', right_on = '대여소번호')<br>
time_split_2021.drop('대여소번호', axis=1, inplace=True)<br>
time_split_2021.columns = ['대여대여소번호', '반납대여소번호', '이용시간', '이용거리', '대여월',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'대여요일', '대여일', '대여시', '반납월', '반납요일', '반납일', '반납시', '대여자치구']<br>
time_split_2021 = pd.merge(left=time_split_2021, right=share_spot.loc[:,['대여소번호','자치구']], left_on='반납대여소번호', right_on = '대여소번호')<br>
time_split_2021.drop('대여소번호', axis=1, inplace=True)<br>
time_split_2021.columns = ['대여대여소번호', '반납대여소번호', '이용시간', '이용거리', '대여월',<br>
&nbsp; &nbsp; &nbsp; &nbsp;'대여요일', '대여일', '대여시', '반납월', '반납요일', '반납일', '반납시', '대여자치구', '반납자치구']<br>
<br>
hour_2021_대여 = time_split_2021.copy()<br>
hour_2021_반납 = time_split_2021.copy()<br>
<br>
hour_2021_대여['이용횟수'] = 1<br>
hour_2021_대여 = hour_2021_대여.loc[:,['대여요일', '대여시', '대여자치구', '이용시간', '이용거리', '대여월','이용횟수']].groupby(['대여월','대여요일', '대여시', '대여자치구']).sum()<br>
hour_2021_대여 = hour_2021_대여.reset_index()<br>
hour_2021_대여 = pd.merge(left = hour_2021_대여, right = district.loc[:,['지역','대여소']], left_on = '대여자치구', right_on = '지역').drop('지역', axis=1)<br>
hour_2021_대여['이용시간'] = hour_2021_대여['이용시간']/hour_2021_대여['대여소']<br>
hour_2021_대여['이용거리'] = hour_2021_대여['이용거리']/hour_2021_대여['대여소']<br>
hour_2021_대여['이용횟수'] = hour_2021_대여['이용횟수']/hour_2021_대여['대여소']<br>
hour_2021_대여['상태'] = '대여'<br>
hour_2021_반납['이용횟수'] = 1<br>
hour_2021_반납 = hour_2021_반납.loc[:,['반납요일', '반납시', '반납자치구', '이용시간', '이용거리', '반납월','이용횟수']].groupby(['반납월','반납요일', '반납시', '반납자치구']).sum()<br>
hour_2021_반납 = hour_2021_반납.reset_index()<br>
hour_2021_반납 = pd.merge(left = hour_2021_반납, right = district.loc[:,['지역','대여소']], left_on = '반납자치구', right_on = '지역').drop('지역', axis=1)<br>
hour_2021_반납['이용시간'] = hour_2021_반납['이용시간']/hour_2021_반납['대여소']<br>
hour_2021_반납['이용거리'] = hour_2021_반납['이용거리']/hour_2021_반납['대여소']<br>
hour_2021_반납['이용횟수'] = hour_2021_반납['이용횟수']/hour_2021_반납['대여소']<br>
hour_2021_반납['상태'] = '반납'<br>
hour_2021_대여.columns = ['월', '요일', '시', '자치구', '이용시간', '이용거리', '이용횟수', '대여소', '상태']<br>
hour_2021_반납.columns = ['월', '요일', '시', '자치구', '이용시간', '이용거리', '이용횟수', '대여소', '상태']<br>
monthly_hourly_use = hour_2021_대여.groupby(['월', '시']).mean().reset_index().pivot(index='월', columns='시', values='이용횟수')<br>
fig = pivotToTimeplot(monthly_hourly_use, title='월별 시간별 대여소당 자전거 대여 추이', yaxis = '시', yRange=[0,18], order = False, duration=1000)<br>
fig.show()<br>
    </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/monthly_hourly_use.html"
  width="800"
  height="480"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="typography-line pt-5">
    <p>
      데이터를 정제하여 월별 시간별 대여소당 대여량의 평균값을 살펴보았다. 로그데이터로부터 1시간 단위로 대여량과 반납량을 나누어 묶었고, 이 그래프는 그 중 '대여량'에 대한 그래프이다.
      1월에 이용자가 제일 적고 모든 월에서 출근/퇴근시간의 이용자가 제일 많은 것을 확인할 수 있다.<br><br>

더워지는 7월-8월에는 출근시간의 이용자가 더 큰폭으로 감소하고 추워지는 10-11월에는 퇴근시간의 이용자가 더 큰폭으로 감소한다는 재밌는 점이 있지만, 그럼에도 월별로 보이는 차이는
스케일의 차이에 불과하지 그 양상은 서로 비슷해 보인다.

    </p>
    </div>

  <send-code number="23">
weekly_hourly_borrow = hour_2021_대여.groupby(['요일','상태','시']).mean().reset_index().pivot(index='요일', columns='시', values='이용횟수')<br>
weekly_hourly_borrow.index = week<br>
weekly_hourly_borrow.index.name = '요일'<br>
fig = pivotToTimeplot(weekly_hourly_borrow, title='요일별 시간별 대여소당 자전거 대여 추이', yaxis = '시', yRange=[0,15], order = False, duration=1000)<br>
fig.show()<br>
  </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/weekly_hourly_borrow.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>


  <div class="typography-line pt-5">
    <p>
평일의 대여는 모두 8시와 18시에 피크를 보이는 것을 알 수 있다. 출근시간과 퇴근시간이다. 정기권 이용자가 '이동을 위해' 자전거를 이용하는 움직임이 극대화되는 시간대이다.
흥미로운 점은 8시에 피크가 있기는 하나 그 양 자체는 17시와 19시에도 못미친다. 즉 날을 통틀어 시간이 지날수록 사용량이 점점 증가하다가 18시 이후 줄어들기 시작한다.
한편, 주말의 사용량은 잔잔하게 증가하기 시작해 16-17시에 피크를 찍는다. 평일과 주말은 그 양상에서 큰 차이를 보인다.<br/><br/>

평일은 평일끼리 비슷하고, 주말은 주말끼리 비슷하다.<br/><br/>

또 확인해본 결과, 각 날의 대여와 반납은 그리 큰 차이를 보이지 않는다. 
사실 빌려도 2시간 안에 갖다놓아야하니 그렇게 큰 차이가 있기는 힘들다. 평균 이용시간이 20분정도에 크치는 것과 맥락이 상통한다.
법정공휴일은 어떨까 생각해보자. 법정공휴일은 출퇴근을 자전거로 하는 사람들의 이용압력이 없으므로 토, 일과 비슷한 양상을 보일 것이다.
    </p>
    </div>
    <send-code number="24">
holiday_hourly_use = time_split_2021[(time_split_2021['대여월'] == 2) &amp; (time_split_2021['대여일'] == 12)].groupby('대여시').size()<br>
holiday_hourly_use.name = '설날 대여량'<br>
fig = seriesPlot(holiday_hourly_use, title=None, order=None, orderArray=None,color=False, colorScale = None)<br>
holiday_hourly_use = time_split_2021[(time_split_2021['대여월'] == 5) &amp; (time_split_2021['대여일'] == 5)].groupby('대여시').size()<br>
holiday_hourly_use.name = '어린이날 대여량'<br>
fig2 = seriesPlot(holiday_hourly_use, title=None, order=None, orderArray=None,color=False, colorScale = None)<br>
holiday_hourly_use = time_split_2021[(time_split_2021['대여월'] == 8) &amp; (time_split_2021['대여일'] == 15)].groupby('대여시').size()<br>
holiday_hourly_use.name = '광복절 대여량'<br>
fig3 = seriesPlot(holiday_hourly_use, title=None, order=None, orderArray=None,color=False, colorScale = None)<br>
holiday_hourly_use = time_split_2021[(time_split_2021['대여월'] == 9) &amp; (time_split_2021['대여일'] == 21)].groupby('대여시').size()<br>
holiday_hourly_use.name = '추석 대여량'<br>
fig4 = seriesPlot(holiday_hourly_use, title=None, order=None, orderArray=None,color=False, colorScale = None)<br>
holiday_hourly_use = time_split_2021[(time_split_2021['대여월'] == 10) &amp; (time_split_2021['대여일'] == 9)].groupby('대여시').size()<br>
holiday_hourly_use.name = '한글날 대여량'<br>
fig5 = seriesPlot(holiday_hourly_use, title=None, order=None, orderArray=None,color=False, colorScale = None)<br>
holiday_hourly_use = time_split_2021[(time_split_2021['대여월'] == 12) &amp; (time_split_2021['대여일'] == 25)].groupby('대여시').size()<br>
holiday_hourly_use.name = '크리스마스 대여량'<br>
fig6 = seriesPlot(holiday_hourly_use, title=None, order=None, orderArray=None,color=False, colorScale = None)<br>
del holiday_hourly_use<br>
fig = pxMerger([fig, fig2, fig3,fig4, fig5,fig6], 3, 2)<br>
fig.update_layout(<br>
&nbsp; &nbsp; height=1000,<br>
&nbsp; &nbsp; width=1000,<br>
&nbsp; &nbsp; title_text="법정공휴일 시간별 대여량",<br>
&nbsp; &nbsp; xaxis_title = '시',<br>
&nbsp; &nbsp; yaxis1_title = '설날',<br>
&nbsp; &nbsp; yaxis2_title = '어린이날',<br>
&nbsp; &nbsp; yaxis3_title = '광복절',<br>
&nbsp; &nbsp; yaxis4_title = '추석',<br>
&nbsp; &nbsp; yaxis5_title = '한글날',<br>
&nbsp; &nbsp; yaxis6_title = '크리스마스'<br>
<br>
&nbsp; &nbsp; )<br>
  </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/holiday_hourly_use.html"
  width="1025"
  height="1030"
  class="frame"
  type="text/html">
  </object>
  </div>
<div class="typography-line pt-5">
    <p>
      법정공휴일의 이용량 또한 주말과 비슷한 양상을 보이는 것을 볼 수 있다. 
      서로의 그래프를 비교해보면 어떤 점을 발견할 수 있는데, 어두운 날에는(크리스마스, 설날) 더 이른시간에 타는 경향이 있다는 것이다.
      설날과 크리스마스의 피크는 광복절과 추석의 피크보다 확실히 이른 시간에 있다.<br/><br/>

      겨울에는 이른 시간대에 이용이 몰리는 경향을 잡아내는 것은 이 분석이 해야하는 일 중 하나가 될 것이다. 
    </p>
    </div>



   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue';

export default {
    name : 'dynamic-006',
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