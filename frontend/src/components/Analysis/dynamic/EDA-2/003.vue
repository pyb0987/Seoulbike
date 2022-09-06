<template>
   <card class="pt-4">
    <send-code number="10">

N=7<br>
c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]<br>
week = ['월','화','수','목','금','토','일']<br>
fig = go.Figure(data=[go.Violin(<br>
&nbsp; &nbsp; y=monthly_use[monthly_use['대여요일']==week[i]]['이용건수'],<br>
&nbsp; &nbsp; marker_color=c[i],<br>
&nbsp; &nbsp; name= week[i]<br>
&nbsp; &nbsp; ) for i in range(int(N))])<br>
<br>
# format the layout<br>
fig.update_traces(box_visible=True, meanline_visible=True)<br>
fig.update_layout(<br>
&nbsp; &nbsp; xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),<br>
&nbsp; &nbsp; yaxis=dict(zeroline=False, gridcolor='white'),<br>
<br>
&nbsp; &nbsp; title='주별 자전거 이용량'<br>
)<br>
<br>
fig.show()<br>
    </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/weekly_use.html"
  width="800"
  height="480"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="typography-line pt-5">
    <p>주별로 전체적인 추이를 보는 것은 그렇게 가시적인 인사이트를 주지 못하는 것 같다. 
      겨울인 주와 여름인 주가 모두 있기 때문에 꼬리가 길게 늘어진다. 
      다만 화, 토, 일은 비교적으로 사람들이 '안타는 선택을 하는 경우'가 있으며 
      월, 수,목, 금요일은 위쪽으로 조금 몰려있는 것으로 보아, 이때 타는 사람들은 '정말 자전거를 좋아하는 사람들'으로 해석할 수 있을 것처럼 보인다.

    </p>
    </div>

  <send-code number="11">

weekly_use_type = daily_use_df.groupby(['대여요일','대여구분코드']).sum().reset_index()<br>
fig = px.bar(weekly_use_type.loc[:,['대여요일','대여구분코드','이용건수']], x='대여요일', y='이용건수', color='대여구분코드', title="요일별 대여구분코드에 따른 이용건수")<br>
fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':week})<br>
fig.show()<br>
  </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/weekly_use_type.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>


  <div class="typography-line pt-5">
    <p>
      대여구분코드에 따른 요일별 차이를 보았더니 어떤 점이 눈에 띈다.
      자전거타기를 좋아하는 '정기권'층은 오히려 토, 일요일에는 잘 타지 않는 것으로 드러났다. 
      정기권을 뺀 나머지는 일요일의 이용건수가 월요일의 최대 두 배까지 올라가지만, 평일에도 자전거를 이용하는 '정기권'층은 일요일에 2/3수준으로 줄어드는 것을 볼 수 있다.<br/><br/>


      따라서 자전거를 자주타는'정기권'층은 자전거를 타는 것을 여가로 하는 비율은 더 적다는 것을 추측할 수 있다. 정기권이 대여소별 이용량에 주는 영향은 평일에 극대화되지만, 주말에는
      조금 다른 접근법을 적용해야 함을 알 수 있다.<br/><br/>
    </p>
    </div>
    <send-code number="12">
weekly_use_type['평균 이용시간(분)'] = weekly_use_type['이용시간(분)']/weekly_use_type['이용건수']<br>
weekly_use_type['평균 이동거리(m)'] = weekly_use_type['이동거리(m)']/weekly_use_type['이용건수']<br>
fig = go.Figure()<br>
fig.add_trace(go.Bar(<br>
&nbsp; &nbsp; x=weekly_use_type[weekly_use_type['대여구분코드']=='정기']['대여요일'],<br>
&nbsp; &nbsp; y=weekly_use_type[weekly_use_type['대여구분코드']=='정기']['평균 이용시간(분)'],<br>
&nbsp; &nbsp; name='정기',<br>
&nbsp; &nbsp; marker_color='midnightblue'<br>
))<br>
fig.add_trace(go.Bar(<br>
&nbsp; &nbsp; x=weekly_use_type[weekly_use_type['대여구분코드']=='일일권']['대여요일'],<br>
&nbsp; &nbsp; y=weekly_use_type[weekly_use_type['대여구분코드']=='일일권']['평균 이용시간(분)'],<br>
&nbsp; &nbsp; name='일일권',<br>
&nbsp; &nbsp; marker_color='lightslategray'<br>
))<br>
fig.add_trace(go.Bar(<br>
&nbsp; &nbsp; x=weekly_use_type[weekly_use_type['대여구분코드']=='비회원']['대여요일'],<br>
&nbsp; &nbsp; y=weekly_use_type[weekly_use_type['대여구분코드']=='비회원']['평균 이용시간(분)'],<br>
&nbsp; &nbsp; name='비회원',<br>
&nbsp; &nbsp; marker_color='lightsalmon'<br>
))<br>
fig.add_trace(go.Bar(<br>
&nbsp; &nbsp; x=weekly_use_type[weekly_use_type['대여구분코드']=='단체']['대여요일'],<br>
&nbsp; &nbsp; y=weekly_use_type[weekly_use_type['대여구분코드']=='단체']['평균 이용시간(분)'],<br>
&nbsp; &nbsp; name='단체',<br>
&nbsp; &nbsp; marker_color='indianred',<br>
))<br>
<br>
<br>
fig.update_layout(title='요일별 대여구분코드에 따른 이용시간', barmode='group', xaxis={'categoryorder':'array', 'categoryarray':week})<br>
fig.show()<br>
  </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/weekly_use_type_time.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>
<div class="typography-line pt-5">
    <p>
      그와 비슷하게, 이용시간을 대상으로 한 비교에서도 정기권 유저들은 자전거를 적게 타는 것을 알 수 있었다. 특히나 모든 요일에 대해서 더 타는 시간이 적었다.
      따릉이를 정기권으로 이용하는 사람들은 '이동의 목적을 가지고 자주타겠다는 목적으로 정기권을 사는 경우'가 흔하기 때문이라고 추측한다.<br><br>
      따릉이를 정기적으로 이용하는 사람들은(전체의 75%) 따릉이를 이용의 목적으로 이용하는 경향이 강하다면, 그 변화를 감지하는 것이 목표인 우리에게는 희소식이 아닐 수 없다.
    </p>
    </div>



   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue';

export default {
    name : 'dynamic-003',
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