<template>
   <card class="pt-4">
    <send-code number="33">
fig = px.imshow(weather.corr().round(3), text_auto=True)<br>
fig.show()
    </send-code>
    <send-code number="34">
fig = px.histogram(weather, x="기온", histnorm='probability density')<br>
fig2 = px.histogram(weather, x="강수량(mm)", histnorm='probability density')<br>
fig3 = px.histogram(weather, x="풍속(m/s)", histnorm='probability density')<br>
fig4 = px.histogram(weather, x="전운량(10분위)", histnorm='probability density')<br>
fig5 = px.histogram(weather, x="습도(%)", histnorm='probability density')<br>
fig = pxMerger([fig, fig2, fig3,fig4,fig5], 3, 2)<br>
fig.update_layout(<br>
&nbsp; &nbsp; height=700,<br>
&nbsp; &nbsp; width=1000,<br>
&nbsp; &nbsp; title_text="각 기상 관측치별 확률분포 히스토그램",<br>
&nbsp; &nbsp; xaxis1_title = '기온',<br>
&nbsp; &nbsp; xaxis2_title = '강수량(mm)',<br>
&nbsp; &nbsp; xaxis3_title = '풍속(m/s)',<br>
&nbsp; &nbsp; xaxis4_title = '전운량(10분위)',<br>
&nbsp; &nbsp; xaxis5_title = '습도(%)'<br>
&nbsp; &nbsp; )<br>

    </send-code>
    <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/weather_corr.html"
  width="725"
  height="730"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/weather_factors.html"
  width="1025"
  height="730"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="typography-line pt-5">
    <p>
      각 변수의 다중공선성은 걱정하지 않아도 되는 수준이다. 
      하지만 강수량, 습도, 전운량, 안개, 비가 서로 클러스터로 묶여있는 것을 볼 수 있다. 연역적으로도 도출 가능한 결론이다.<br/><br/>
전운량은 데이터 성격 자체는 범주형 자료에 해당하나, 구름의 양을 수치화 한 것으로, 수치형 데이터로 해석한다. 기온, 풍속, 습도는 이상치가 없는 고른 분포를 하고 있음을 알 수 있다.
강수량의 경우에는 정규화를 진행할 때, 0에 해당하는 값이 너무 많아서 StandardScaler로 정규화 하더라도, 그렇게 큰 변화가 있지 않았고 Box-cox변환을 수행할 경우에는
-36의 람다값이 나와 사실상 해석 불가능한 수치를 반환했다. 따라서 그냥 비가 내리는지 안내리는지가 더 중요한 요소라고 판단하여 MinMaxScaler로 정규화했다.
나머지 요소들도 모두 같은 방식으로 스케일링했다.<br/><br/>

이제 비로소 준비가 되었다고 판단하여 머신러닝을 수행했다.

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