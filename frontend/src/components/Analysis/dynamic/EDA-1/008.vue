<template>
   <card class="pt-4">
    <div class="typography-line">
    </div>
    <send-code number="22">
fig = px.pie(new_members.groupby(['성별']).sum(), values='가입수', title="성별 가입인원 비율",names=new_members.groupby(['성별']).sum().index)<br/>
fig.show()
    </send-code>
  <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/sex_members.html"
width="800"
height="500"
class="frame"
type="text/html">
</object>
  </div>
     <div class="typography-line pt-5">
    <p>
      단순 성별에 따라 분류를 한 그래프는 다음과 같다.
      여성과 남성이 비슷하게 가입한 것을 볼 수 있다. 남자가 여성보다 훨씬 더 많을 것으로(2:1정도) 생각했지만
      전혀 아니었다. 알 수 없는 None을 빼면 남성과 여성의 비율은 51.2 : 48.8이었다. 아마 None이 티머니GO와 같은
      앱에서 무료이용권 광고를 보고 유입된 인원이 맞다면 None에서는 여성의 비율이 더 높을 것이라는 생각이 들었다.
</p>
    </div>
    <send-code number="23">
top_labels = ['여자', '남자']<br/>
colors = ['rgba(164, 163, 204, 0.85)', 'rgba(71, 58, 131, 0.8)']<br/>
y_data = ['70대이상', '60대', '50대', '40대', '30대', '20대', '10대']<br/>
x_data = [new_members.groupby(['연령대','성별']).sum().loc[i]['가입수'][:2] for i in y_data]<br/>
<br/>
fig = HorizontalPortionBar(top_labels, x_data, y_data, colors, '연령별 남녀 비율')<br/>
fig.show()
    </send-code>
  <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/age_sex_portion.html"
width="800"
height="500"
class="frame"
type="text/html">
</object>
  </div>
      <div class="typography-line pt-5">
    <p>
      연령별 남녀비율을 비교하면 다음과 같았다.
      전반적으로 남성이 여성보다 많으나, 20대에서는 유일하게 여성이 과반수였다.
      나이가 들수록 여성의 비율이 떨어지는 경향이 있었다. 그럼에도 앞에서 보았듯이 20대의 비중이 매우 커, 
      이 초과분만으로 여성 남성 비율을 거의 1대1로 만드는데 일조했다.
      성인식이 세대별로 변화하는 과정을 나타내는 그래프로 보아도 어느정도는 맞을 것 같다.
    </p>
    </div>


   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue'

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