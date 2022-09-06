<template>
   <card class="pt-4">
    <send-code number="7">
age_use_type = daily_use.groupby(['대여구분코드', '연령대','성별코드']).sum().unstack(fill_value=0).stack()['이용건수']<br/>

fig = make_subplots(rows=3, cols=1)<br>
stack = ['정기', '일일권', '단체']<br>
age_code = ['10대미만', '10대', '20대', '30대', '40대', '50대', '60대','70대이상', '기타']<br>
<br>
for i in range(3):<br>
&nbsp; &nbsp; fig.add_trace(<br>
&nbsp; &nbsp; &nbsp; &nbsp; go.Bar(<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; name="None",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; x=age_code,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; y=age_use_type[stack[i]][age_use_type[stack[i]].index.get_level_values(1)=='None'].loc[age_code],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; offsetgroup=0,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; marker_color='red',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; legendgroup = i+1<br>
&nbsp; &nbsp; &nbsp; &nbsp; ),<br>
&nbsp; &nbsp; &nbsp; &nbsp; row=i+1,<br>
&nbsp; &nbsp; &nbsp; &nbsp; col=1,<br>
&nbsp; &nbsp; )<br>
&nbsp; &nbsp; fig.add_trace(<br>
&nbsp; &nbsp; &nbsp; &nbsp; go.Bar(<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; name="남성",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; x=age_code,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; y=age_use_type[stack[i]][age_use_type[stack[i]].index.get_level_values(1)=='M'].loc[age_code],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; offsetgroup=0,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; base=age_use_type[stack[i]][age_use_type[stack[i]].index.get_level_values(1)=='None'].loc[age_code],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; marker_color='blue',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; legendgroup = i+1<br>
&nbsp; &nbsp; &nbsp; &nbsp; ),<br>
&nbsp; &nbsp; &nbsp; &nbsp; row=i+1,<br>
&nbsp; &nbsp; &nbsp; &nbsp; col=1,<br>
<br>
&nbsp; &nbsp; )<br>
&nbsp; &nbsp; fig.add_trace(<br>
&nbsp; &nbsp; &nbsp; &nbsp; go.Bar(<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; name="여성",<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; x=age_code,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; y=age_use_type[stack[i]][age_use_type[stack[i]].index.get_level_values(1)=='F'].loc[age_code],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; offsetgroup=0,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; base=age_use_type[stack[i]][age_use_type[stack[i]].index.get_level_values(1)=='M'].loc[age_code]+age_use_type[stack[i]][age_use_type[stack[i]].index.get_level_values(1)=='None'].loc[age_code],<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; marker_color='green',<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; legendgroup = i+1<br>
&nbsp; &nbsp; &nbsp; &nbsp; ),<br>
&nbsp; &nbsp; &nbsp; &nbsp; row=i+1,<br>
&nbsp; &nbsp; &nbsp; &nbsp; col=1,<br>
<br>
&nbsp; &nbsp; )<br>
&nbsp; &nbsp; fig.update_layout(<br>
&nbsp; &nbsp; height=1000,<br>
&nbsp; &nbsp; width=800,<br>
&nbsp; &nbsp; title_text="대여종류별 연령&amp;성별 차트",<br>
&nbsp; &nbsp; xaxis3_title = '연령대',<br>
&nbsp; &nbsp; yaxis1_title = '정기권',<br>
&nbsp; &nbsp; yaxis2_title = '일일권',<br>
&nbsp; &nbsp; yaxis3_title = '단체',<br>
&nbsp; &nbsp; legend_tracegroupgap = 240<br>
<br>
&nbsp; &nbsp; )<br>
<br>
<br>
fig.show()<br>
    </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/age_use_type.html"
  width="825"
  height="1030"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="typography-line pt-5">
    <p>각 대여종류별로 연령, 성별에 따른 이용의 추이를 보면 다음과 같다. 
      일일권은 압도적으로 20대가 많이 구매했는데, 보통 늦은 시간까지 귀가하지 않고 놀다가 집에 갈때
일일권을 사서 택시 대신 타고 가는 경우를 많이 봤다. 일일권 자체가 '자주타지는 않을 것이지만 지금은 필요한'경우에
사게 될 것이므로 이러한 경우가 두각될 것이다.<br/><br/>

30대의 단체권 비율은 눈에 띄게 낮았다. 아마 단체로 무언가를 하기가 쉽지 않은 나이라 그런 것 같다.
따릉이 단체권은 통상의 단체권과 달리 2~5명을 대상으로 하고, 일일권과 1인당 가격이 같다. 따라서 굳이 단체권을
사야할 필요는 결코 없다.
여러명이 타려는데 휴대폰을 사용할 수 있는 인원에 제한이 있는 경우에 빛을 발할 것이다. 
    </p>
    </div>

  <send-code number="8">
monthly_use = daily_use[(daily_use['연']==2021)].loc[:,['대여일자','이용건수','대여구분코드', '성별코드', '이동거리(m)','이용시간(분)','대여요일']].groupby('대여일자').sum()<br/>
monthly_use['평균이용시간(분)'] = monthly_use['이용시간(분)']/monthly_use['이용건수']<br/>
monthly_use['평균이동거리(m)'] = monthly_use['이동거리(m)']/monthly_use['이용건수']<br/>
<br/>
monthly_use = monthly_use.reset_index()<br/>
monthly_use['대여일자'] = pd.to_datetime(monthly_use['대여일자'])<br/>
monthly_use['대여요일'] = monthly_use['대여일자'].dt.dayofweek<br/>
monthly_use['대여주']= monthly_use['대여일자'].dt.weekofyear.astype('category')<br/>
monthly_use['대여월']=monthly_use['대여일자'].dt.month.astype('category')<br/>
monthly_use['대여년']=monthly_use['대여일자'].dt.year.astype('category')<br/>
monthly_use['대여요일'] = monthly_use.loc[:,'대여요일'].replace({0:'월', 1:'화', 2:"수", 3:'목', 4:'금', 5:'토', 6:'일'})<br/>
<br/>
N=12<br>
c = ['hsl('+str(h)+',50%'+',50%)' for h in np.linspace(0, 360, N)]<br>
fig = go.Figure(data=[go.Box(<br>
&nbsp; &nbsp; y=monthly_use[monthly_use['대여월']==i+1]['이용건수'],<br>
&nbsp; &nbsp; marker_color=c[i],<br>
&nbsp; &nbsp; name= str(i+1)+'월'<br>
&nbsp; &nbsp; ) for i in range(int(N))])<br>
<br>
# format the layout<br>
fig.update_layout(<br>
&nbsp; &nbsp; xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),<br>
&nbsp; &nbsp; yaxis=dict(zeroline=False, gridcolor='white'),<br>
&nbsp; &nbsp; title='월별 자전거 이용량'<br>
)<br>
<br>
fig.show()<br>
  </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/monthly_use.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>


  <div class="typography-line pt-5">
    <p>
      월별 이용량 그래프도 월별 신규 가입자 그래프와 같은 형태를 보이는 것을 볼 수 있다. 겨울에는 더 적은 수를 이용하고, 여름에는 더 많이 이용한다. 
      논리적인 순서는 반대일 것이다. 겨울에 이용압력이 더 적기 때문에, 이용량이 더 낮고, 그렇기 때문에 신규 가입인원이 적은 것이다.<br/><br/>

      위 그래프에서 재밌는 점이 있는데, 이상치가 아래쪽으로만 존재하고, 위쪽으로는(많은 이용량을 가지는 이상치는) 존재하지 않는다는 것이다. 이상치가 아래쪽으로 편중되는
      이유는 비가 내리는 날에는 확실히 사람들이 자전거를 덜 타기 때문이다.<br/><br/>

      대여구분코드는 어떤 차이를 보여줄지 확인해보자
    </p>
    </div>
    <send-code number="9">

daily_use_df = daily_use[(daily_use['연']==2021)].loc[:,['대여일자','이용건수','대여구분코드', '성별코드', '이동거리(m)','이용시간(분)','대여요일']].groupby(['대여일자', '대여구분코드']).sum()<br/>
daily_use_df = daily_use_df.reset_index()<br/>
daily_use_df['대여일자'] = pd.to_datetime(daily_use_df['대여일자'])<br/>
daily_use_df['대여요일'] = daily_use_df['대여일자'].dt.dayofweek<br/>
daily_use_df['대여주']= daily_use_df['대여일자'].dt.weekofyear.astype('category')<br/>
daily_use_df['대여월']=daily_use_df['대여일자'].dt.month.astype('category')<br/>
daily_use_df['대여년']=daily_use_df['대여일자'].dt.year.astype('category')<br/>
daily_use_df['대여요일'] = daily_use_df.loc[:,'대여요일'].replace({0:'월', 1:'화', 2:"수", 3:'목', 4:'금', 5:'토', 6:'일'})<br/>
<br/>
monthly_use_type = daily_use_df.groupby(['대여월','대여구분코드']).sum().reset_index()<br/>
fig = px.bar(monthly_use_type.loc[:,['대여월','대여구분코드','이용건수']], x='대여월', y='이용건수', color='대여구분코드', title="월별 대여구분코드에 따른 이용건수")<br/>
fig.show()<br/>
  </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/monthly_use_type.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>
<div class="typography-line pt-5">
    <p>
      정기, 일일권, 비회원, 단체에 의한 이용 모두 1월에 제일 적고 9월에 제일 많다. 사실 필자는 따릉이를 탐에 있어 계절을 별로 가리지 않기 때문에
      정기권 층의 조금 더 결속된 모습을 기대했으나, 그러지는 않았다. 그럼에도 불구하고 정기권을 구매한 층이 겨울에도 덜 이탈하는 경향을 보였다.
      정기권의 경우에는 1월에 60만건, 9월에 270만건으로 4.5배의 차이가 난다. 
      일일권의 경우에는 1월에 13만건, 9월에 80만건으로 약 6배의 차이가 난다. 비슷하게 비회원은 25배, 단체는 8배의 차이가 난다.<br/><br/>

      1월에 단체로 자전거를 타러가는 집단은 조금 이상한(최소한 흔하지는 않은) 집단일 확률이 높다는 것을 알 수 있다. 정기권일수록, 
      자전거에 진심이거나, 또는 정기권을 구매했다는 사실 자체에서 압력을 받아 1월에도 이용을 더 많이 하게 되는 경향성을 확인할 수 있다.
    </p>
    </div>



   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue';

export default {
    name : 'dynamic-002',
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