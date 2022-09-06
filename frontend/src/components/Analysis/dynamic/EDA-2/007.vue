<template>
   <card class="pt-4">
    <send-code number="25">
hour_2021_대여['유입량'] = hour_2021_반납['이용횟수']-hour_2021_대여['이용횟수']<br>
<br>
weekday_lent_state = (-1) * hour_2021_대여.groupby(['요일','시']).mean().loc['평일']['유입량'].cumsum()<br>
weekday_lent_state = weekday_lent_state - weekday_lent_state.min()<br>
weekday_lent_state.name = '평일 대여상태'<br>
weekend_lent_state = (-1) * hour_2021_대여.groupby(['요일','시']).mean().loc['휴일']['유입량'].cumsum()<br>
weekend_lent_state = weekend_lent_state - weekend_lent_state.min()<br>
weekend_lent_state.name = '휴일 대여상태'<br>
<br>
<br>
fig = pxMerger([px.line(weekday_lent_state),px.line(weekend_lent_state)], 2, 1)<br>
fig.update_layout(<br>
&nbsp; &nbsp; title='시간별 대여소당 자전거 대여상태 추이',<br>
&nbsp; &nbsp; legend_tracegroupgap = 400)<br>
fig.update_xaxes(title_text="시")<br>
fig.update_yaxes(title_text="대여숫자")<br>
<br>
fig.show()<br>
    </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/weekday_lent_state.html"
  width="925"
  height="930"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="typography-line pt-5">
    <p>
      반납량과 대여량의 차이인 유입량이라는 항목을 만들었다. 이 항목은 앞으로 매우 중요하게 다뤄질 것이다.
      또한 한 대여소에 존재하는 자전거의 대수는 유입량의 누적합과 같을 것이므로(정확히는 적분 상수만큼 차이가 난다)
      대여소의 자전거 대수를 예측하는 것은 이러한 방식으로 간접적으로 구해질 것이다.<br/><br/>
      <strong>
      반납량-대여량=유입량<br/>
      대여상태=유입량의 누적합<br/><br/>
      </strong>
평일의 경우 이용하는 사람의 총 수는 8시에 피크를 찍었지만, 대여상태의 숫자(현재 이용중인 총 숫자)는 오전 7시에 급격하게 증가했다가 9시까지 매우 약간 감소한 후, 18시까지 계속 상승했다.

이는 길거리에서 따릉이를 볼 확률이 사람이 붐비는 8시나 9시나 별 다름없다는 것을 의미하지는 않는다. 
왜냐하면 8시에 빌려서 다시 반납하는 이용객이 많다는 것을 위에서 확인했기 때문이다. 
그러나 이는 따릉이를 빌리기위해 대여소에 갔을 경우 8시나 9시나 비슷하게 대여소에 따릉이가 남아있을 것이라는 것을 의미한다. 
이것만으로도 조금 놀라운 결과이다.<br/><br/>

하지만 정말 그럴까? 사람들은 주거지역에서 상업지역으로 출근하는 경향이 있으므로 자치구의 그 비율에 따라 차이를 보일 것이다.
    </p>
    </div>

  <send-code number="26">

fig = px.density_heatmap(pd.concat([hour_2021_대여, hour_2021_반납]), x="시", y="자치구", z="이용횟수", facet_row="요일", facet_col='상태', histfunc="avg")<br>
fig.update_layout( &nbsp; <br>
<br>
&nbsp; &nbsp; width=1200,<br>
&nbsp; &nbsp; height = 800,<br>
&nbsp; &nbsp; title='자치구별 시간별 대여소당 자전거 대여/반납 추이')<br>
fig.show()<br>

  </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/dist_hourly_use.html"
  width="1225"
  height="830"
  class="frame"
  type="text/html">
  </object>
  </div>


  <div class="typography-line pt-5">
    <p>
      다음은 자치구별 평일과 휴일의 시간당 대여/반납량을 나타낸 히트맵이다.
      자치구가 많아 개별 자치구의 추이는 눈에 잘 들어오지않지만 전체적인 추세는 파악할 수 있다. 
      모든 자치구에서 평일 오전 8시, 18시가 피크임을 확인할 수 있다.
      대여를 많이하는 자치구는 반납도 많이 하는 경향이 있음을 확인할 수 있다.

    </p>
    </div>
    <send-code number="27">

pd.concat([hour_2021_대여.groupby(['요일','시','자치구']).mean()<br>
&nbsp; &nbsp; .loc['평일',8]['이용횟수'],hour_2021_반납.groupby(['요일','시','자치구'])<br>
&nbsp; &nbsp; .mean().loc['평일',8]['이용횟수']],axis=1)<br>
&nbsp; &nbsp; .corr(method ='pearson').iloc[0,1]<br>

  </send-code>
  <receive-code>
    0.8544188162665571
  </receive-code>
  <send-code number="28">
(plotdf_2021['대여자치구']==plotdf_2021['반납자치구']).value_counts()
  </send-code>
  <receive-code>
True &nbsp; &nbsp; 18876830<br>
False &nbsp; &nbsp; 7318823<br>
dtype: int64<br>
  </receive-code>

<div class="typography-line pt-5">
    <p>
      pearson 상관계수를 측정하면 평일 오전 8시의 자치구별 대여와 반납횟수 사이에서 0.8515의 높은 상관계수를 볼 수 있다.
      즉 대여량이 더 많은 자치구가 반납량도 더 많다.
      여기에는 두가지 가능성이 있다.<br>
      <ol>
        <li>대부분의 자전거 이동은 자치구 내 이동이다.</li>
        <li>실제로 '따릉이를 빌리기위해 대여소에 갔을 경우 8시나 9시나 비슷하게 대여소에 따릉이가 남아있을 것'이다.</li>
      </ol>
      1에 대한 확인은 비교적 쉽게 할 수 있다.
      대략 72%의 이동이 자치구 내에서 일어나는 것을 알 수 있다. <br><br>
      
      대여량과 반납량이 상관관계를 보이는 이유는 자치구 자체가 점이 아니라
      크기를 가지고 있는 지역이므로 한 출발지로부터 이동하는 이용객이 그리 멀리 떨어지지 않은 곳에(같은 자치구 안에)
      반납을 할 가능성이 높기 때문인 것으로 판명났다.
      주의하지 않으면 잘못된 결론에 빠지기 쉽다.

    </p>
    </div>



   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue';

export default {
    name : 'dynamic-007',
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