<template>
   <card class="pt-4">
    <div class="typography-line">
    </div>
    <send-code number="18">
fig = px.bar(new_members.groupby(['연령대','성별']).sum().loc[:,['가입수']].reset_index(), x="연령대", y="가입수", color="성별", title="연령대별 성별에 따른 가입인원수")<br/>
fig.show()<br/>
    </send-code>
  <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/age_sex_members.html"
width="800"
height="500"
class="frame"
type="text/html">
</object>
  </div>
     <div class="typography-line pt-5">
    <p>
      위의 차트는 연령대별 성별 가입인원수를 나타낸 것이다.
      성별에 관계없이 20대가 제일 많고, 30대, 40대 순으로 점점 나이가 들수록 가입인원이 줄어드는 것을 볼 수 있다.
      그러나 60대보다 70대가 더 많은데, 이는 성별을 판별할 수 있는 경우에서는 해당되지 않으나, 위에서 보았던 
70대 이상의 None의 값이 비정상적으로 높아 성별을 입력하지 않은 경우의 연령대설정이 기본이 70대 이상으로(예 : 생일이 1900년 1월 1일로 설정)되어있다든가 하는 문제가 있는 것으로 생각된다.<br/><br/>

N/F+M의 비가 연령이 올라갈 수록 낮아지기 때문에(앱의 설치에 익숙하지 않다는 점을 고려하면) 70대 N은 총합계 2000이 되지 않을 것으로 예상한다.
    </p>
    </div>
    <send-code number="19">
new_members[(new_members['연령대']=='70대이상') & (new_members['성별']=='None')]['가입수'].describe()
    </send-code>
    <receive-code>
count     546.000000<br/>
mean      176.282051<br/>
std       635.033292<br/>
min         1.000000<br/>
25%         2.000000<br/>
50%         5.000000<br/>
75%        11.750000<br/>
max      5706.000000<br/>
Name: 가입수, dtype: float64
    </receive-code>

      <div class="typography-line">
    <p>
      연령대가 70대 이상이고 성별이 None인 row들에 대해 describe함수를 사용해보았다.
    75% quantile의 값은 11이지만 mean은 176, max값이 5706인 것으로 보아, 실제 추이에서 벗어나는 이상치들이 존재하는 것이 확실해졌다.
    어느 시기의 이용자 정보들이 제대로 기록되지 않고 청크로 처리해서 넘긴 것으로 추측할 수 있었다. 연령대가 70대 이상이면서
    성별은 None이고 하루 가입 수가 100이 넘는 값들의 연령대를 모두 기타로 처리했다.(100항밖에 되지 않았다.)
    </p>
    </div>

  <send-code number="20">
new_members.loc[(new_members['연령대']=='70대이상') & (new_members['성별']=='None') & (new_members['가입수']>100),'연령대'] = '기타'<br/>
fig = px.bar(new_members.groupby(['연령대','성별']).sum().loc[:,['가입수']].reset_index(), x="연령대", y="가입수", color="성별", title="연령대별 성별에 따른 가입인원수")<br/>
fig.show()
  </send-code>
    <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/age_sex_members2.html"
width="800"
height="500"
class="frame"
type="text/html">
</object>
  </div>
    <div class="typography-line pt-5">
    <p>
    70대 N이 2000정도가 나오도록 조작하지 않고도, 이치에 맞도록 그래프의 형태가 바뀐 것을 볼 수 있다. 훨씬 더 직관적이다.
    </p>
    </div>

<send-code number="21">
fig = px.pie(new_members.groupby(['연령대']).sum(), values='가입수', title="연령별 가입인원 비율",names=new_members.groupby(['연령대']).sum().index)<br/>
fig.show()<br/>
</send-code>
    <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/age_members.html"
width="800"
height="500"
class="frame"
type="text/html">
</object>
  </div>
  <div class="typography-line pt-5">
    <p>
      연령별 가입인원은 다음과 같았다.
      연령대를 알수 없는 기타 항목을 제외하면 20대가 거의 50%에 육박하여 제일 많았으며(차트에서 기타 항목을 클릭하면 빠진다), 
30대, 40대, 10대, 50대, 60대, 70대 이상 순이었다.
직관적으로 예상 가능했던 부분으로 앱에 대한 접근성, 활동량, 그리고 자전거 대여 목적을 생각하면(자전거를 운동용으로 탄다면 40,50대가 더 많이 탈 것으로 생각되나
공유시스템의 자전거를 단순 운동 목적으로 타는 사람의 비율은 별로 높지 않을 것이다.) 이해가 가는 결과다.
      </p>
    </div>
   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue'

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