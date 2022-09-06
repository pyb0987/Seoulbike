<template>
   <card class="pt-4">
    <send-code number="4">
age_sex_use_portion = daily_use.groupby(['연령대', '성별코드']).sum()<br/>
y_data = ['기타', '70대이상', '60대', '50대', '40대', '30대', '20대', '10대','10대미만']<br/>
x_data = [age_sex_use_portion.loc[i].loc['F':'M', '이용건수'] for i in y_data]<br/>
top_labels = ['여성', '남성']<br/>
fig = HorizontalPortionBar(top_labels, x_data, y_data, title='연령별 남녀 이용률')<br/>
fig.show()<br/>
    </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/age_sex_use_portion.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="typography-line pt-5">
    <p>연령별 남녀 이용률을 살펴보면, 20대에서는 거의 남녀가 비슷했으며 그 이외의 구간에서는 남성의 이용비율이
      60퍼센트를 상회했다. 60대에서는 거의 1:4까지 떨어졌다. 가입인원 비율과 이용비율이 차이나는 것은
      유령회원의 비중이 높을 수 있다는 것을 뜻하기도 하고, 또 그 반대쪽에서 충성회원의 비중이 높을 수 있다는 것을
      의미하기도 한다.
    </p>
    </div>

  <send-code number="5">
age_sex_use_portion['평균 이용시간(분)'] = age_sex_use_portion['이용시간(분)'] / age_sex_use_portion['이용건수']<br/>
age_sex_use_portion['평균 이동거리(m)'] = age_sex_use_portion['이동거리(m)'] / age_sex_use_portion['이용건수']<br/>
age_sex_usetime = age_sex_use_portion[age_sex_use_portion.index.get_level_values(1)!='None']<br/>
age_sex_usetime = age_sex_usetime.loc[['10대미만', '10대', '20대', '30대', '40대', '50대', '60대','70대이상', '기타']]<br/>
<br/>
fig = px.histogram(age_sex_usetime, x=age_sex_usetime.index.get_level_values(0), y="평균 이용시간(분)",<br/>
             color=age_sex_usetime.index.get_level_values(1), barmode='group',  histfunc='avg', title='연령대별 평균 이용시간',labels={"평균 이용시간(분)":"이용시간(분)" ,'x': '연령대'},
             height=400)<br/>
fig.show()<br/>
<br/>
fig = px.histogram(age_sex_usetime, x=age_sex_usetime.index.get_level_values(0), y="평균 이동거리(m)",<br/>
             color=age_sex_usetime.index.get_level_values(1), barmode='group',histfunc='avg', title='연령대별 평균 이동거리',labels={"평균 이동거리(m)":"이동거리(m)" ,'x': '연령대'},
             height=400)<br/>
fig.show()<br/>
  </send-code>
  <div class="row">
  <object data="http://localhost:8000/static/figures/age_sex_usetime.html"

height="450"
class="col-6"
type="text/html">
</object>
  <object data="http://localhost:8000/static/figures/age_sex_usedist.html"

height="450"
class="col-6"
type="text/html">
</object>
  </div>
  <div class="typography-line pt-5">
    <p>
      왼쪽 그래프는 연령대와 성별에 따른 평균 이용시간을 비교한 것이고, 오른쪽은 평균 이동거리를 비교한 것이다.
      여성이 모든 연령대에서 대체적으로 남성보다 오래타고, 멀리타는 것을 알 수 있다. 
      이는 위에서 살펴본 남녀 이용비율의 차이와 조합해 봤을 때, 하나의 가설을 만들 수 있다.<br/><br/>

      <strong>여성은 여가의 목적으로(빠르지 않고, 느긋하게, 간헐적으로) 이용하는 비중이 높고, <br/>남성은
        이동의 목적으로(빠르고, 더 자주) 이용하는 비중이 높다
      </strong>
      <br/><br/>
      아마도 이 가설의 뿌리는 필자가 이동의 목적으로 따릉이를 이용한다는 점에서 시작되었을 것이다.
      그러나 충분히 가능성 있는 접근이라고 생각한다.
    </p>
    </div>
    <send-code number="6">
daily_use['대여일자'] = pd.to_datetime(daily_use['대여일자'])<br/>
daily_use['연'] = daily_use['대여일자'].dt.year<br/>
daily_use['월'] = daily_use['대여일자'].dt.month<br/>
daily_use['일'] = daily_use['대여일자'].dt.day<br/>
daily_use['대여요일'] = daily_use['대여일자'].dt.dayofweek<br/>
daily_use['대여요일'] = daily_use.loc[:,'대여요일'].replace({0:'월', 1:'화', 2:"수", 3:'목', 4:'금', 5:'토', 6:'일'})<br/>
<br/>
use_type_portion =daily_use.groupby(['대여구분코드']).size()<br/>
use_type_portion.name = '인원수'<br/>
fig = px.pie(use_type_portion, values='인원수',title="대여종류 비율", names=use_type_portion.index, color_discrete_sequence=px.colors.sequential.Sunset)<br/>
fig.show()
  </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/use_type_portion.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>
<div class="typography-line pt-5">
    <p>
      전체 이용횟수에서 정기권 이용자가 거의 대부분을 차지했고, 그 다음은 일일권이었다. 비회원과 단체는 각각 1퍼센트 내외였다.
      정기권 이용자가 정기적으로 이용하는 그 양상을 파악하는 것이 최우선 목표가 될 것이다.
    </p>
    </div>



   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue';

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