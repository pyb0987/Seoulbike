<template>
   <card class="pt-4">
    <send-code number="9">
        share_spot_district_year = share_spot.groupby(['연','자치구']).size().reset_index().pivot(index='연', columns='자치구', values=0).fillna(0).cumsum()<br/>
fig = pivotToTimeplot(share_spot_district_year, title='자치구별 대여소 현황', yaxis = '대여소 개수', yRange=[0, 220], order = True)<br/>
fig.show()
    </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/share_spot_district_year.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="typography-line pt-5">
    <p>따릉이는 2016년까지는 마포구 등, 특정 자치구에 시범설치 후에 2017년부터 본격적으로 운영이 시작되었다.
      2020년에도 많은 수가 설치되었는데 송파구, 강서구, 강남구 등등 소위 '잘 사는' 동네가 더 많은 대여소를 가지고 있다.
      송파구의 경우에는 지도에서는 그렇게 밀도가 높아보이지 않았는데, 이는 송파구가 넓은 구이기 때문인 것이라고 생각된다.</p>
    </div>

  <send-code number="10">
    district = pd.read_table(data_dir+'자치구/인구밀도.txt', sep='\t')<br/>
district['인구'] = district['인구'].str.replace(',','').astype(float).astype(int)   #쉼표를 제거<br/>
district['인구밀도(명/㎢)'] = district['인구밀도(명/㎢)'].str.replace(',','').astype(float).astype(int)<br/>
district.drop('기간', axis=1, inplace=True)<br/>
<br/>
spot_district = share_spot.groupby('자치구').size()<br/>
spot_district.name = '대여소'<br/>
spot_per_space = pd.merge(left = pd.DataFrame(spot_district), right = district[['지역','면적']], how='left', left_on = '자치구', right_on='지역').set_index('지역')<br/>
<br/>
spot_per_space['대여소'] = spot_per_space['대여소']/spot_per_space.max(axis=0)['대여소']<br/>
spot_per_space['면적'] = spot_per_space['면적']/spot_per_space.max(axis=0)['면적']<br/>
fig = dfPlot(spot_per_space, spot_per_space.index, ['대여소', '면적'], title='자치구별 면적&대여소 비율', orderArray=spot_per_space.sort_values('면적', ascending = False).index)<br/>
fig.show()<br/>
  </send-code>
  <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/spot_per_space.html"
width="800"
height="400"
class="frame"
type="text/html">
</object>
  </div>
  <div class="typography-line pt-5">
    <p>지역구별 인구와 면적 데이터는 인터넷에서 쉽게 구할 수 있다. 조금만 다듬으면 이미 지역구별 대여소 개수를
      알고 있으므로 면적 당 대여소의 개수를 구할 수 있다. 다만 여기서는 대여소 수와 면적은 scale이 맞지 않으므로 최대값을 1로 정규화했다.<br/>
      결과적으로 강서구, 강남구, 송파구에 많은 대여소가 배치된 것은 절대적으로 큰 면적을 가지고있기 때문인 것으로 판명났다. 면적당 개수로는
      그렇게 도드라지는 면이 없었다. 다만 중구의 면적대비 대여소 개수는 꽤나 높아 보인다. 중구에는 대여소가 많이 설치되어 있지 않지만
      그 크기가 매우 작으므로 사실은 매우 촘촘히 설치되어 있는 것이다. 
    </p>
    </div>
    <div class="row">
      <img src="http://localhost:8000/static/figures/S-Map-중구.png" class="col-6" />
    <img src="http://localhost:8000/static/figures/S-Map-관악구.png" class="col-6" />
    </div>
      <div class="row">
        <div class="col-6">
          <p><i class="tim-icons icon-minimal-up"></i>중구</p>
        </div>
        <div class="col-6">
          <p><i class="tim-icons icon-minimal-up"></i>관악구</p>
        </div>
    </div>

    <div class="typography-line">
    <p>관악구 신림동에서 잠시 지냈던 적이 있는데 지금 생각해보면 따릉이를 거의 본적이 없던 것 같다.
또 언덕이 너무 많고 높아서 따릉이를 타봤자 어짜피 끌고 가야할 지도 모른다.
이 점에 착안해 서울시에서 제공하는 S-map 해발고도 히트맵을 확인해 보았다.<br/><br/>
그랬더니 확실하게 차이가 보였다. 알고보니 중구는 서울에서 유일하게 99.9% 면적이 생활이용되고 있는 구였다.
다른 구들은 하천, 산 등 때문에 그렇게 하고 있지 못하다.
</p>
    </div>


   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue'

export default {
    name : 'dynamic-004',
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