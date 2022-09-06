<template>
   <card class="pt-4">
    <div class="typography-line">
      <h3>신규가입자 톺아보기</h3>
    </div>
    <send-code number="14">
new_members = getAllCsv('신규가입자')<br/>
new_members[0].columns = ['사용자', '연령대', '성별', '가입수']<br/>
new_members[0].index.name = '가입일자'<br/>
new_members[1].columns = ['사용자', '성별', '연령대', '가입수']<br/>
new_members[1].index.name = '가입일자'<br/>
new_members[2].columns = ['사용자', '성별', '연령대', '가입수']<br/>
new_members[2].index.name = '가입일자'<br/>
new_members[3].columns = ['사용자', '연령대', '성별', '가입수']<br/>
new_members[3].index.name = '가입일자'<br/>
new_members = pd.concat(new_members)<br/>
new_members.head()<br/>
new_members.info()
    </send-code>
    <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/new_members_before_head.png" class='frame'/>
    </div>
    <receive-code>
class 'pandas.core.frame.DataFrame'<br/>
Index: 28749 entries, 2018-07-20 to 2022-06-30<br/>
Data columns (total 4 columns):<br/>
 #   Column  Non-Null Count  Dtype <br/>
---  ------  --------------  ----- <br/>
 0   사용자     28749 non-null  object<br/>
 1   연령대     28749 non-null  object<br/>
 2   성별      24537 non-null  object<br/>
 3   가입수     28749 non-null  int64 <br/>
dtypes: int64(1), object(3)<br/>
memory usage: 1.1+ MB<br/>
    </receive-code>

      <div class="typography-line pt-5">
    <p>
      신규가입자 데이터는 연단위로 나누어져 csv파일로 저장되어 있기 때문에, 직접 만든 함수를 사용하여
      특정 폴더에 있는 파일들을 모두 불러와 데이터프레임으로 합쳤다.
      다른 컬럼은 모두 결측값이 없고 성별에 Nan값이 있는 것을 확인할 수 있다. 가입수는 연령별로, 성별로, 가입일별로 집계되어 있다.
    </p>
    </div>

  <send-code number="15">
  print('사용자 : ',new_members['사용자'].unique())<br/>
new_members['사용자'] = new_members['사용자'].replace("'회원-내국인'", '회원-내국인').replace("'회원-외국인관광객'", '회원-외국인관광객')<br/>
print('사용자 : ',new_members['사용자'].unique())<br/>
print('연령대 : ',new_members['연령대'].unique())<br/>
new_members['연령대'] = new_members['연령대'].replace("'~10대'", '10대').replace("'20대'", '20대').replace("'30대'", '30대').replace("'40대'", '40대').replace("'50대'", '50대').replace("'60대'", '60대').replace("'70대~'", '70대이상')<br/>
print('연령대 : ',new_members['연령대'].unique())<br/>
print('성별 : ',new_members['성별'].unique())<br/>
new_members['성별'] = new_members['성별'].replace("'F'", 'F').replace("'M'", 'M').replace("''", np.NaN)<br/>
print('성별 : ',new_members['성별'].unique())<br/>
print('가입일자 "\'"의 개수 : ',new_members.index.str.contains("'").sum())<br/>
print('가입일자 "\'"의 개수 : ',new_members.index.str.contains("'").sum())<br/>
new_members.index = new_members.index.str.replace("'", "")<br/>
print('가입일자 "\'"의 개수 : ',new_members.index.str.contains("'").sum())
  </send-code>
<receive-code>
  사용자 :  ['회원-내국인' "'회원-내국인'" "'회원-외국인관광객'"]<br/>
사용자 :  ['회원-내국인' '회원-외국인관광객']<br/>
연령대 :  ['10대' '20대' '30대' '40대' '50대' '60대' '70대이상' '기타' "'~10대'" "'20대'" "'30대'"
 "'40대'" "'50대'" "'60대'" "'70대~'"]<br/>
연령대 :  ['10대' '20대' '30대' '40대' '50대' '60대' '70대이상' '기타']<br/>
성별 :  [nan 'F' 'M' "'F'" "'M'" "''"]<br/>
성별 :  [nan 'F' 'M']<br/>
가입일자 "'"의 개수 :  8095<br/>
가입일자 "'"의 개수 :  8095<br/>
가입일자 "'"의 개수 :  0<br/>
</receive-code>
  <div class="typography-line">
    <p>또 각 칼럼에는 여러가지 카테고리가 있고 개중에는 표시방식이 중간에 바뀌어 같은 것을 뜻하면서도, 이름이 다른 카테고리가 존재했다.
      전부 바로 잡아주었다.
      </p>
    </div>
  <send-code number="16">
new_members.sort_values('가입수', ascending=False).iloc[10:20]
  </send-code>
    <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/new_member_sorted_nan.png" class='frame'/>
    </div>
    <div class="typography-line pt-5">
    <p>
일간 가입자 상위 10-20위 항목을 확인하였으나, 어떤 점이 도드라진다. 전부, 성별 미기재거나, 연령대가 20대, 70대이상, 기타이다.
상위 300개 항목에서 모두 이렇게 나오는 것을 확인했으며 이는 
성별 미기재 인원은 남성, 여성 둘 다 있기 때문인 것으로 보인다. <br/><br/>

따릉이를 네이버 또는 카카오톡으로 회원가입 시도했을 경우 성별은 필수 기재사항이나
서울형 통합이동서비스 티머니GO를 통해 가입할 때는 확인할 수 없는 데이터로 처리되므로 이로 인한 추이가 아닐까 생각한다.

티머니Go를 확인해보았더니 따릉이 한달 무료이용권을 주고 
가입자 데이터는 기록되지 않으므로, 그로인한 데이터 오염으로 생각할 수 있을 것 같다. 다운로드 수는 200만 정도이므로
NaN의 총 개수와 얼추 일치한다.<br/><br/>

결측치를 삭제하는 것은 무리라고 판단하여 'None'이라는 카테고리로 넣었고,
시간적인 변화를 살펴보기 위해 인덱스를 연도, 월, 요일로 분리했다.

      </p>
    </div>
  <send-code number="17">
new_members['성별'].fillna('None', inplace = True)<br/>
new_members['가입연도'] =new_members.index.str.split('-').str[0]<br/>
new_members['가입월'] =new_members.index.str.split('-').str[1]<br/>
new_members['가입요일'] = pd.to_datetime(new_members.index).day_of_week<br/>
  </send-code>
   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue'

export default {
    name : 'dynamic-006',
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