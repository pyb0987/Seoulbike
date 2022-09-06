<template>
   <card class="pt-4">
    <div class="typography-line">
    </div>
    <send-code number="24">
monthly_members = new_members.groupby(['가입연도', '가입월']).sum()<br/>
monthly_members = monthly_members.reset_index()<br/>
monthly_members['가입연월'] = monthly_members['가입연도']+plotdf['가입월']<br/>
fig = px.bar(monthly_members, x='가입연월', y="가입수", labels=dict(x="가입연월"))<br/>
fig.update_layout(title_text='연월별 신규 가입인원')<br/>
fig.show()<br/>
fig = TimeSeriesPlot(plotdf, '가입연도', '가입월', '가입수', title='1년 주기 월별 가입인원 추이')<br/>
fig.show()<br/>
    </send-code>
  <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/monthly_members.html"
height="500"
class="col-6"
type="text/html">
</object>
 <object data="http://localhost:8000/static/figures/yearly_members.html"
height="500"
class="col-6"
type="text/html">
</object>
  </div>
  
     <div class="typography-line pt-5">
    <p>
  왼쪽의 그래프는 월별로 신규가입인원을 나타낸 것이고, 오른쪽의 그래프는 같은 것을 12개월 단위로 쪼개어
  선그래프로 나타낸 것이다.
  가입인원의 그래프는 확실하게 계절적 주기성을 띄고 있는 것을 볼 수 있다. 추운계절인 11월부터 3월까지는
신규인원들이 자전거를 대여할 동기부여가 떨어지는 것을 확인 할 수 있다.
그 차이는 생각한 것보다도 훨씬 컸는데, 이는 (당연히 고려해야 하지만) 계절적인 특성을 구하고자 하는 '대여소별 자전거 대수예측'에 반영해야하며
시계열 분석으로 예측을 해야할 수도 있다는 생각을 하게 만들었다.<br/><br/>
또 가입인원은 그 이후로 계속 증가하다 7, 8월은 오히려 떨어지는 것을 볼 수 있는데, 이는 자전거를 타기에 비교적으로 더운 날씨이기 때문인
것으로 보인다. 자전거를 대여할 동기부여는 계절적(또는 온도적) 특성에 지대한 영향을 받는다는 인사이트를 도출할 수 있다.<br/><br/>

또 가입인원이 2020년에 정점을 찍고 점점 내려오는 것이 확인된다.
</p>
    </div>
    <send-code number="25">
monthly_spot = pd.DataFrame(share_spot.groupby(['연', '월']).size())<br/>
monthly_spot.columns = ['설치 대수']<br/>
monthly_spot['연'] = monthly_spot.index.get_level_values(0)<br/>
monthly_spot['월'] = monthly_spot.index.get_level_values(1)<br/>
monthly_spot['설치연월'] = monthly_spot['연']+monthly_spot['월']<br/>
monthly_spot = pd.merge(left = monthly_members['가입연월'], right = monthly_spot, how='left', left_on = '가입연월', right_on='설치연월').fillna(0)<br/>
monthly_spot.drop('설치연월', axis=1, inplace=True)<br/>
monthly_spot.columns = ['설치연월', '설치 대수', '연', '월']<br/>
<br/>
fig = px.bar(monthly_spot, x='설치연월', y="설치 대수")<br/>
fig.update_layout(title_text='연월별 대여소 설치 대수')<br/>
fig.show()
    </send-code>
  <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/monthly_spot.html"
width="800"
height="500"
class="frame"
type="text/html">
</object>
  </div>
      <div class="typography-line pt-5">
    <p>
      연월별 따릉이 대여소 설치 건수는 신규가입인원의 추이와 별로 연관이 없는 것처럼 보인다.
      당연히 대여소가 늘어나면 신규가입인원도 늘겠지만(접할 기회가 더 많아지므로) 그 증가의 방식이
      두 그래프에서 서로 관계가 없는 것처럼 보인다. 아마 신규가입인원이 2020년까지 매년 증가하고 2021년부터는 그 수가 줄은 이유는
       따릉이 사업이 그 외연을 확장하는 동안 계속 신규 유입이 되다가 이제 안정기에 들어선 것으로 사료된다.<br/><br/>

또는 이를 천천히 올라가는 그래프로 보고 2020년만 높은 이유를 설명하는 변수로 코로나의 발발을 들수도 있겠다. 그렇게 해석할 경우,
평시 신규가입자 수는 계속 비슷한 수준을 유지할 것이며 사업의 미래가 밝다는 것을 암시할 수도 있다.

    </p>
    </div>


   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue'

export default {
    name : 'dynamic-009',
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