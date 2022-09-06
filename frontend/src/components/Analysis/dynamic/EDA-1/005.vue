<template>
   <card class="pt-4">
    <send-code number="11">
    spot_per_pop = pd.merge(left = pd.DataFrame(spot_district), right = district[['지역','인구']], how='left', left_on = '자치구', right_on='지역').set_index('지역')<br/>
tmp = spot_per_pop['대여소']<br/>
spot_per_pop['대여소'] = spot_per_pop['대여소']/spot_per_pop.max(axis=0)['대여소']<br/>
spot_per_pop['인구'] = spot_per_pop['인구']/spot_per_pop.max(axis=0)['인구']<br/>
fig = dfPlot(spot_per_pop, spot_per_pop.index, ['대여소', '인구'], title='자치구별 인구&대여소 비율', orderArray=spot_per_pop.sort_values('인구', ascending = False).index)<br/>
fig.show()
    </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/spot_per_pop2.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="typography-line pt-5">
    <p>따라서 면적대비 비교는 별로 의미가 없고, 인구수 대비 비교가 차라리 나을 것이다.
      송파구에서의 인구수 대비 대여소 비율을 1이라고 가정했을 때, 각 자치구의 비율은 어떻게 되는지 확인해보았다. 
      다른 구는 그 비율이 모두 1.2가 되지 않지만 종로구와 중구는 그것의 거의 두배가 될 정도로 높다.<br/><br/>

종로구와 중구가 높은 이유는 일일 통행인구 비율이 높기 때문인 것 같다.
지금까지 데이터로는 그 사실을 캐치하기 힘들었기 때문에 이런 차이가 반영되지 않은 것으로 생각된다.
서울 내부의 생활이동을 파악하는 것은 또 다른 데이터분석 주제가 될 정도로 큰 것이지만
우선은 서울시에서 제공하는 <a href="https://data.seoul.go.kr/livPopu/html/dashboard.html" target="_blank">https://data.seoul.go.kr/livPopu/html/dashboard.html</a> 에서 .
22년 4월 1달간 생활이동인구의 데이터만 가지고 그 개요만 살펴보았다.</p>
    </div>

  <send-code number="12">
  live_Pop = pd.read_csv(data_dir+'자치구/22년4월생활이동인구.csv', encoding='cp949', index_col=0)<br/>
  spot_district = live_Pop.merge(spot_district,left_index=True, right_index=True)<br/>
spot_district['총이동인구'] = spot_district['유입']+spot_district['유출']<br/>
spot_district.drop(['유입', '유출'], axis=1, inplace = True)<br/>
spot_district['대여소'] = spot_district['대여소']/spot_district.max(axis=0)['대여소']<br/>
spot_district['총이동인구'] = spot_district['총이동인구']/spot_district.max(axis=0)['총이동인구']<br/>
spot_district['대여소/이동인구 비율'] = (spot_district['대여소']/spot_district['총이동인구']).round(3)<br/>
spot_district = spot_district['대여소/이동인구 비율']<br/>
spot_district.name = '대여소/이동인구'<br/>
fig = seriesPlot(spot_district, title="자치구별 이동인구 대비 대여소 비율", order = 'total descending', color=True, colorScale = px.colors.sequential.Sunsetdark)<br/>
fig.show()<br/>
  </send-code>
  <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/spot_per_live_pop.html"
width="800"
height="500"
class="frame"
type="text/html">
</object>
  </div>
  <div class="typography-line pt-5">
    <p>아직 최고치와 최저치가 2배정도 차이나지만 그래도 지금까지 본것에 비해면 꽤나 온건한 그래프가 나왔다.
      그래프를 보면, 중구, 강남구는 인구수 대비 많은 수가 설치되었으나, 이동인구에 비하면 그것마저도
      아직 부족한 상황인 것을 알 수 있다. 이동인구의 수가 많아도 그 이동인구의 연령대별 비율에 따른 차이가
      있을 수 있다는 생각이 들었지만, 그것은 자전거 대여비율로 살펴보도록 하고, 여기서 다루지는 않겠다.<br/><br/>
      우선은 자치구마다 대여소의 개수들을 나타낸 데이터프레임을 저장했다.
      </p>
    </div>
  <send-code number="13">
spot_district = pd.DataFrame(share_spot.groupby('자치구').size())<br/>
district = pd.merge(left=district, right=spot_district, left_on = '지역', right_on = spot_district.index)<br/>
district.columns = ['지역', '인구', '면적', '인구밀도(명/㎢)', '대여소']
  </send-code>


   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue'

export default {
    name : 'dynamic-005',
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