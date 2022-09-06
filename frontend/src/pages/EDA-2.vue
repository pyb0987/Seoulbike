<template>
  <div class="col-md-10 mx-auto">
    <div ref="scroll"></div>
    <card class="p-4">
    <div class="typography-line">
    <h1>
        따릉이 분석 - EDA-2
    </h1>
    <hr>
    <h3>일별 대여정보 톺아보기</h3>
    </div>
    <send-code number="0">
        daily_use = getAllCsvDask('일별 대여정보/내국인')<br/>
        for i in range(len(daily_use)):<br/>
    daily_use[i].columns = ['대여일자', '번호', '대여소', '대여구분코드', '성별코드', '연령대', '이용건수', '운동량', '탄소량', '이동거리(m)', '이용시간(분)']<br/>
daily_use = pd.concat(daily_use)<br/>
daily_use.shape<br/>
    </send-code>
    <receiveCode>
      (38435982, 11)  #38435982 rows × 11 columns의 초대형 데이터프레임이 만들어졌다.
    </receiveCode>
    <send-code number="1">

daily_use.drop(['운동량', '탄소량'], axis=1, inplace=True)<br>
print('대여구분코드 : ',daily_use['대여구분코드'].unique())<br>
daily_use['대여구분코드'] = daily_use['대여구분코드'].replace({'단체권':'단체','단체(1시간권)':'단체','정기권':'정기', '일일(비회원)': '비회원', '일일권(비회원)' : '비회원', '일일(회원)':'일일권', '일일 회원(1시간권)':'일일권', '일일 회원(2시간권)':'일일권', '일일(회원)':'일일권', '\\N': 'None'})<br>
print('대여구분코드 : ',daily_use['대여구분코드'].unique())<br>
print('성별코드 : ',daily_use['성별코드'].unique())<br>
daily_use['성별코드'] = daily_use['성별코드'].replace({'m' : 'M', 'f': 'F', '\\N' : 'None', np.NaN : 'None'})<br>
print('성별코드 : ',daily_use['성별코드'].unique())<br>
print('연령대 : ',daily_use['연령대'].unique())<br>
daily_use['연령대'] = daily_use['연령대'].replace({'~10대':'10대미만', 'AGE_002' : '20대', 'AGE_003': '30대', 'AGE_004' : '40대', 'AGE_005' : '50대', 'AGE_001' : '10대', 'AGE_008' : '기타','AGE_006':'60대', '\\N' : '기타', '70대~' : '70대이상', 'AGE_007': '70대이상' })<br>
print('연령대 : ',daily_use['연령대'].unique())<br>
<br>
daily_use = daily_use[(daily_use['대여소']!='R') &amp; (daily_use['대여구분코드'] != 'None') &amp; (daily_use['대여구분코드'] != 'BIL_021') &amp; (daily_use['이용시간(분)']&gt;0) &amp; (daily_use['이동거리(m)'] &gt; 0.01) &amp; ((daily_use['이동거리(m)']/daily_use['이용건수'])&lt;100000) &amp; ((daily_use['이동거리(m)']/daily_use['이용시간(분)'])&lt;700) &amp; ((daily_use['이용시간(분)']/daily_use['이용건수'])&lt;240)]<br>
repair_spot = daily_use[(daily_use['대여소'].str.contains('정비')) &amp; (daily_use['번호'] != 1823)]['번호'].unique()<br>
daily_use = daily_use[~daily_use['번호'].isin(repair_spot)]<br>
daily_use = daily_use[daily_use['번호'] &lt; 9000]<br>
daily_use = daily_use[daily_use['번호'] &gt; 100]<br>
daily_use.head()<br>
    </send-code>
    <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/daily_use_before_head.png" class='frame'/>
    </div>
    <div class="typography-line pt-5">
    <p>대여정보는 월 단위로 들어있었는데, 용량이 상당히 크고 파일도 많았다. 전부 불러와 합치자, 데이터프레임 열이 4000만 행에 달했다.
      운동량, 탄소량은 새로운 정보를 주지 않으므로 삭제했고, 각 행에서 카테고리들을 더 적은 수로 통합했다. 연령대에서 연령대 코드와
      구분을 말로 써놓은 것을 하나로 합치는 것이 좋은 예이다.
      그 이후 이상치를 삭제했는데, 삭제한 이상치의 내용은 다음과 같다.
      <ul>
        <li>대여구분코드 : None or BIL_021 삭제</li>
        <li>이용시간(분) : 0분 삭제 or 240분 이상 삭제(2시간이 추가과금없는 제한이므로 이를 과대하게 넘을경우 분실의 확률이 큼)</li>
        <li>이동거리(m) : 0m 삭제 or 100km이상 삭제</li>
        <li>시간당 이동거리(km/h) : 42km/h이상 삭제(선수급이 40km정도 나오므로)</li>
        <li>대여소 : 특수한 대여소로 정비를 위해 간 경우 삭제(이름이 R이거나 '정비'가 붙은 곳 중 1823번을 제외하고 삭제, 100번 미만, 혹은 9000번 이상의 번호 삭제)</li>
      </ul>
    </p>
    </div>
    <send-code number="2">
sex_use_portion =daily_use.groupby(['성별코드']).size()<br/>
sex_use_portion.name = '성별'<br/>
fig = px.pie(sex_use_portion, values='성별', title="성별별 이용건수 비율",names=sex_use_portion.index)<br/>
fig.show()<br/>
    </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/sex_use_portion.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>
    <div class="typography-line pt-5">
    <p>다음은 성별에 따른 이용건수를 나타낸 그래프이다. 비슷한 비슷한 정도의 신규가입이 있던것과는 다르게 실제로 
      이용하는 사람의 비율은 남자가 높다(None 제외). None이 신규가입자의 None과 같은 클러스터인지는 알 수 없다.
      수는 대충 비슷해보이기는 한다.</p>
    </div>
    <send-code number="3">
age_use_portion =daily_use.groupby(['연령대']).size()<br/>
age_use_portion.name = '연령대'<br/>
fig = seriesPlot(age_use_portion, title='연령대별 비율', orderArray=['10대미만', '10대', '20대','30대','40대','50대','60대','70대이상','기타'], color=True, colorScale = px.colors.sequential.Sunsetdark)<br/>
fig.show()
    </send-code>
<div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/age_use_portion.html"
  width="800"
  height="500"
  class="frame"
  type="text/html">
  </object>
  </div>
 <div class="typography-line pt-5">
    <p>연령대별로 보면 다음과 같다. 10대 미만까지 확인할 수 있다. 가끔 안장이 낮은 따릉이가 있는데, 바로 이들을 위한 자전거일 것이다.
      20대가 제일 많고, 전체적으로 예상한 것과 같은 직관적인 결과를 볼 수 있다.</p>
    </div>

    </card>

    <component v-for="item in components" :is="item.component" :key="item.id"></component>

    <div ref="endofcontent" class="text-center">
      <p  v-if="!loading">
        이 컨텐츠의 마지막 페이지입니다.
      </p>
      <div class="ms-auto">
        <Spinner :loading="loading"></Spinner>
      </div>
    </div>
  </div>
</template>

<script>
import BaseButton from '../components/BaseButton.vue';
import Spinner from '../components/Spinner.vue';
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue';

export default {
  components: {
    BaseButton,
    Spinner,
    sendCode,
    receiveCode
},
  data (){
    return {
      tab : 1,
      topicData: [],
      components: [],
      loading : true,
    }
  },
  mounted() {
    this.$refs.scroll.scrollIntoView();
    const endofcontent = this.$refs.endofcontent;
    let self = this
    const io = new IntersectionObserver(function(entries, observer){
        if(entries[0].isIntersecting){
          let promise = () => import(`src/components/Analysis/dynamic/EDA-2/${self.paddedTab}`)
      promise().then((res)=>{
          setTimeout(()=>{
            const component_id = `dynamic-component-${self.paddedTab}`  
          self.components.push({
            component : res.default,
            id: component_id     
          });
          self.tab += 1
            }, 500)
        }).catch((err)=>{ 
          observer.unobserve(entries[0].target)
          self.loading = false
      })
        }
      }, {
      root: null,
      rootMargin: '100px',
      threshold: 0.1
      })
      io.observe(endofcontent);
      },
  computed : {
    paddedTab : function(){
      return ('00' + this.tab).slice(-3)
      }
  },
  method : {
  }


}

</script>

<style>
.frame{
  border: 5px solid rgb(190, 190, 190);
  padding: 0px;
}

p{
  line-height: 33px;
}
</style>