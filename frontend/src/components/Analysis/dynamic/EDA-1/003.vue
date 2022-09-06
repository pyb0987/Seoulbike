<template>
   <card class="pt-4">
    <div class="typography-line">
      <h3>대여소 톺아보기</h3>
    <p>대여소 정보는 <a href="https://data.seoul.go.kr/dataList/datasetList.do#" target="_blank">
      https://data.seoul.go.kr/dataList/datasetList.do#</a>에서 가져와 분석을 위해 결측값을 제거했다.</p>
    </div>
    <send-code number="7">
        share_spot = pd.read_csv(data_dir + '대여소\대여소정보.csv',engine='python',encoding='CP949', index_col=0)<br/>
        share_spot[['LCD', 'QR']] = share_spot[['LCD', 'QR']].fillna(0).astype(int)<br/>
        share_spot['설치시기'].fillna(method='bfill', inplace = True)<br/>
        share_spot.drop(columns='운영방식',inplace = True)<br/>
        share_spot['연'] = share_spot['설치시기'].str.split('-').str[0]<br/>
share_spot['월'] = share_spot['설치시기'].str.split('-').str[1]<br/>
share_spot['일'] = share_spot['설치시기'].str.split('-').str[2]<br/>
share_spot.drop(columns='설치시기',inplace = True)<br/>
share_spot.info()
    </send-code>
    <receiveCode>           
        Int64Index: 2653 entries, 102 to 5855<br/>
        Data columns (total 10 columns):<br/>
        #   Column     Non-Null Count  Dtype  <br/>
        ---  ------     --------------  -----  <br/>
        0   보관소(대여소)명  2653 non-null   object <br/>
        1   자치구        2653 non-null   object <br/>
        2   상세주소       2653 non-null   object <br/>
        3   위도         2653 non-null   float64<br/>
        4   경도         2653 non-null   float64<br/>
        5   LCD        2653 non-null   float64<br/>
        6   QR         2653 non-null   float64<br/>
        7   연         2653 non-null   float64<br/>
        8   월         2653 non-null   float64<br/>
        9   일         2653 non-null   float64<br/>
        dtypes: float64(7), object(3)<br/>
        memory usage: 184.7+ KB<br/>
    </receiveCode>


  <send-code number="8">
    share_spot_map = heatMapMap(share_spot['위도'], share_spot['경도'])<br/>
    share_spot_map
  </send-code>
  <div class="d-flex justify-content-center">

    <object data="http://localhost:8000/static/figures/share_spot_map.html"
width="600"
height="600"
class="frame"
type="text/html">
</object>
  </div>
    <div class="typography-line pt-5">
    <p>지도에 히트맵을 표시해본 결과는 다음과 같다. 사람이 많을 만한 공간에 많이 배치되어 있는 것을
      알 수 있다.  충정로, 시청, 을지로, 종로 부근과, 김포국제공항 앞 
공항대로의 밀도가 특히 높다. 강남구와 서초구에는 예상했던 것과는 반대로 그렇게 높은
밀도로 분포되어 있지는 않은 것이 보인다.</p>
    </div>
   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue'

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