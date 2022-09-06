<template>
   <card class="pt-4">
    <send-code number="13">
m = folium.Map(location=[37.55, 126.98], titles="따릉이 대여소 이용현황", zoom_start=12)<br>
<br>
for i in range(0,len(metro_use_relation)):<br>
&nbsp; &nbsp; latitude = metro_use_relation.iloc[i]['위도']<br>
&nbsp; &nbsp; longitude = metro_use_relation.iloc[i]['경도']<br>
&nbsp; &nbsp; location=(latitude, longitude)<br>
&nbsp; &nbsp; use = metro_use_relation.iloc[i]['이용건수']<br>
&nbsp; &nbsp; red = str(hex(int((int(float(use))//10000)/7*(0-56)+56))).replace('0x', '').zfill(2)<br>
&nbsp; &nbsp; green = str(hex(int((int(float(use))//10000)/7*(75-176)+176))).replace('0x', '').zfill(2)<br>
&nbsp; &nbsp; blue = str(hex(int((int(float(use))//10000)/7*(35-0)+0))).replace('0x', '').zfill(2)<br>
&nbsp; &nbsp; opacity = str(hex(int((int(float(use))//10000)/7*(255-180)+180))).replace('0x', '').zfill(2)<br>
&nbsp; &nbsp; color = '#'+red+green+blue+opacity<br>
<br>
&nbsp; &nbsp; folium.CircleMarker(location, radius=(metro_use_relation.iloc[i]['이용건수']/400)**0.5,color=color,fill_color=color,<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; popup='이용건수 : '+str(metro_use_relation.iloc[i]['이용건수'])).add_to(m)<br>
<br>
<br>
folium.LayerControl(collapsed=False).add_to(m)<br>
m<br>
    </send-code>
      <div class="d-flex justify-content-center">
  <object data="http://localhost:8000/static/figures/spot_use_map.html"
  width="800"
  height="480"
  class="frame"
  type="text/html">
  </object>
  </div>
      <div class="typography-line pt-5">
    <p>
      따릉이 대여소 각각 그 이용량이 면적에 비례하는 원을 그리면 다음과 같았다.
      서울 외각으로 나갈수록 원의 크기가 점점 작아지는 경향성을 확인할 수 있다. 강서구, 영등포구와, 송파구, 광진구의 활발한 이용률이 보인다. 
      중구, 노원구, 서초구, 강남구는 대여소마다 매우 고르게 이용하는 모습을 볼 수 있다.<br><br>

      한편 따릉이의 이용 분포를 파악하는 것은 힘든 문제임이 드러났는데, 왜냐하면 적은 몇 개의 대여소에서 지나치게 많은 이용량을 보이는 것이 확인되었기 때문이다.
      당초의 계획은 구별로 클러스터화 하는 것이었는데, 이러한 분포를 보여서야 구 단위로 어떤 경향성을 찾겠다는 것은, 말그대로 '경향성'의 수준에서는 가능할지 몰라도
      예측의 측면에서는 부질없는 시도일 것이라는 생각이 들었다. 만약 그렇다면, 2600개나 되는 대여소에 대해 원핫 인코딩을 하거나 모델을 다 따로 만들어야(이것이 훨씬 현실적이다)
      할 것이다.
       </p>
    </div>

  <send-code number="14">

from selenium import webdriver<br>
from selenium.webdriver.common.by import By<br>
from selenium.webdriver.common.keys import Keys<br>
from selenium.webdriver.support.ui import WebDriverWait<br>
from selenium.webdriver.support import expected_conditions as EC<br>
<br>
import time<br>
import requests<br>
from bs4 import BeautifulSoup<br>
import re<br>
driver = webdriver.Chrome("../chromedriver")<br>
<br>
driver.get("https://map.naver.com/v5/directions")<br>
<br>
try:<br>
&nbsp; &nbsp; start_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#directionStart0")))<br>
&nbsp; &nbsp; direction_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#directionGoal1")))<br>
except:<br>
&nbsp; &nbsp; driver.close()<br>
<br>
N = len(share_spot['대여소번호'])<br>
number = share_spot['대여소번호']<br>
dist = share_spot['자치구']<br>
addr = share_spot['상세주소']<br>
distance_set = []<br>
p = re.compile('(^[가-힣]+역)') &nbsp; &nbsp; #역 이름 찾기<br>
for k in range(len(share_spot['대여소번호'])):<br>
&nbsp; &nbsp; start_addr = addr[k].replace('지하', '').replace(' &nbsp;', ' ').strip() #'지하'라고 써져있을 경우 검색이 안됨<br>
&nbsp; &nbsp; if dist[k] not in start_addr:<br>
&nbsp; &nbsp; &nbsp; &nbsp; start_addr = dist[k] +" " +start_addr<br>
&nbsp; &nbsp;<br>
&nbsp; &nbsp; print(start_addr, '찾을 차례')<br>
&nbsp; &nbsp; start_input.clear()<br>
&nbsp; &nbsp; start_input.send_keys(start_addr)<br>
&nbsp; &nbsp; start_input.send_keys(Keys.ENTER)<br>
&nbsp; &nbsp; time.sleep(0.5)<br>
&nbsp; &nbsp; direction_input.clear()<br>
&nbsp; &nbsp; direction_input.send_keys("지하철")#지하철 검색<br>
&nbsp; &nbsp; direction_input.send_keys(Keys.ENTER)<br>
&nbsp; &nbsp; time.sleep(0.8)<br>
&nbsp; &nbsp; wait_until = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.icon_directions")))<br>
&nbsp; &nbsp; list_search = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.list_search")))<br>
&nbsp; &nbsp; result_names = list_search.find_elements_by_css_selector('.link_search .search_title_text')<br>
<br>
&nbsp; &nbsp; print('역 목록 확인중')<br>
&nbsp; &nbsp;<br>
<br>
&nbsp; &nbsp; station_names = [] &nbsp;#클릭하여 거리를 잴 대상들/ 중복된 역이 있는지 확인할 list<br>
&nbsp; &nbsp; distance_list = [] &nbsp; #역으로부터 거리가 저장됨<br>
&nbsp; &nbsp; for i in range(len(result_names)):<br>
&nbsp; &nbsp; &nbsp; &nbsp; result_name = result_names[i].text<br>
&nbsp; &nbsp; &nbsp; &nbsp; try: &nbsp; &nbsp; &nbsp;#역 이름이 존재하는 지 확인<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; m = p.match(result_name)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; station_name = m.group()<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if(station_name not in station_names): &nbsp; #중복되지 않으면 추가<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; station_names.append(station_name)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; if len(station_names) &gt;=3: &nbsp;#맨 앞의 3개 역만 확인<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; break<br>
&nbsp; &nbsp; &nbsp; &nbsp; except:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; continue<br>
&nbsp; &nbsp; print('역 목록 확인완료', station_names)<br>
&nbsp; &nbsp; for i in range(len(station_names)):<br>
&nbsp; &nbsp; &nbsp; &nbsp; if len(start_input.get_attribute('value')) &lt; 1:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; start_input.send_keys(start_addr)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; start_input.send_keys(Keys.ENTER)<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; time.sleep(0.5)<br>
&nbsp; &nbsp; &nbsp; &nbsp; direction_input.clear()<br>
&nbsp; &nbsp; &nbsp; &nbsp; direction_input.send_keys(station_names[i])<br>
&nbsp; &nbsp; &nbsp; &nbsp; direction_input.send_keys(Keys.ENTER)<br>
&nbsp; &nbsp; &nbsp; &nbsp; time.sleep(0.5)<br>
&nbsp; &nbsp; &nbsp; &nbsp; direction_button = driver.find_element_by_css_selector('button.btn.btn_direction')<br>
&nbsp; &nbsp; &nbsp; &nbsp; direction_button.click()<br>
&nbsp; &nbsp; &nbsp; &nbsp; time.sleep(0.5)<br>
&nbsp; &nbsp; &nbsp; &nbsp; walk_button = driver.find_element_by_css_selector('a.link_tab.walk')<br>
&nbsp; &nbsp; &nbsp; &nbsp; walk_button.click()<br>
&nbsp; &nbsp; &nbsp; &nbsp; try:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; distance = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".summary_box .summary_text")))<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; distance_list.append(distance.text)<br>
&nbsp; &nbsp; &nbsp; &nbsp; except:<br>
&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; distance_list.append('50km') &nbsp;##50km 이상일경우에는 제공하지 않음<br>
&nbsp; &nbsp; &nbsp; &nbsp; print('역 확인', i+1, '번째 완료')<br>
&nbsp; &nbsp; distance_set.append(dict(zip(station_names, distance_list)))<br>
&nbsp; &nbsp;<br>
&nbsp; &nbsp; print(str(k+1)+'/'+str(N),(k+1)/N*100 , &nbsp;'% 완료')<br>
driver.close()<br>
  </send-code>
  <send-code number="15">
metro_use_relation = daily_use[daily_use['대여일자']&gt;='2022-01-01'].loc[:,['번호','이용건수']].groupby('번호').sum()<br>
metro_use_relation = pd.merge(left =metro_use_relation,right = &nbsp;share_spot.loc[:,['대여소번호','근처역','근처역거리', '위도','경도']], how='left', left_on =metro_use_relation.index, right_on='대여소번호')<br>
metro_use = getAllCsvDask('지하철이용량')<br>
for i in range(len(metro_use)):<br>
&nbsp; &nbsp; metro_use[i].columns = ['노선명', '역명', '승차총승객수', '하차총승객수', '등록일자','wrongField']<br>
metro_use = pd.concat(metro_use)<br>
metro_use.index.name = '사용일자'<br>
metro_use.reset_index(inplace=True)<br>
metro_use['사용일자'] = pd.to_datetime(metro_use['사용일자'].astype(str).str.slice(0,4)+'-'+metro_use['사용일자'].astype(str).str.slice(4,6)+'-'+metro_use['사용일자'].astype(str).str.slice(6,8))<br>
metro_use['총승객수'] = metro_use['승차총승객수']+metro_use['하차총승객수']<br>
metro_use.drop(['등록일자','wrongField'], axis=1, inplace=True)<br>
metro_station_use = metro_use.groupby('역명').sum()<br>
metro_station_use.index = metro_station_use.index + '역'<br>
metro_station_use.index = metro_station_use.index.str.replace(r"\((.*)\)", "") #괄호 제거<br>
metro_use_relation = pd.merge(left = metro_use_relation,right = metro_station_use,how='inner', left_on='근처역' , right_on=metro_station_use.index)<br>
metro_use_relation.drop(['하차총승객수', '승차총승객수'], axis=1, inplace=True)<br>
res = ols('이용건수 ~ 근처역거리 + 총승객수', data=metro_use_relation).fit()<br>
fitted = res.predict(metro_use_relation)<br>
res.summary()<br>
  </send-code>
    <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/metro_use_relation_ols.png" class='frame' style="background-color: #fff"/>
    </div>
    <send-code number="16">
residual = metro_use_relation['이용건수'] - fitted<br>
fig = plt.figure(figsize=(20, 5))<br>
ax1 = fig.add_subplot(1,3,1)<br>
ax2 = fig.add_subplot(1,3,2)<br>
ax3 = fig.add_subplot(1,3,3)<br>
sns.regplot(fitted, residual, lowess=True, line_kws={'color': 'red'}, ax=ax1 )<br>
stats.probplot(residual, dist=stats.norm,plot=ax2)<br>
sr = stats.zscore(residual)<br>
sns.regplot(fitted, np.sqrt(np.abs(sr)), lowess=True, line_kws={'color': 'red'}, ax=ax3 )<br>
fig.show()<br>
    </send-code>
    <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/metro_use_relation_pp.png" class='frame' style="background-color: #fff"/>
    </div>


  <div class="typography-line pt-5">
    <p>
      대여소 별로 이용량을 파악할 좋은 방법이 있을까 생각하던 와중, 주변에 지하철 역이 있다면 그 이용량이 어떻게 변화하는지 궁금해졌다.
      주변에 지하철 역이 있다면 사람들이 많이 통행하는 곳이라는 의미이므로 따릉이를 타려는 사람들도 많겠지만, 
      지하철 역 자체가 따릉이를 타려는 사람들에게 그것이 일종의 타지 않게끔하는 압력이 될 수 도 있다고 생각했기 때문에 회귀분석을 해보기로 했다. 
      2653개 대여소에 대해 제일 가까운 지하철역까지의 거리를 측정해야 하므로 selenium을 사용했다. (selenium.ipynb) 16개 대여소에서는 작동하지 않아 손으로 입력했다.<br/><br/>


      지하철역 및 대여소가 세워진 일자 또한 제각각이므로 이에 받는 영향을 최소화하기 위해 2022년의 정보만 가지고 평가했다. 
      또 근처의 지하철 역이 붐비는 역일 경우, 사람 자체가 많아 사용량에 유의미한 영향을 줄 것으로 생각되므로 각 역의 이용량 또한 종속변수로 추가했다.<br/><br/>
      <strong>
        F-검정 귀무 가설: 절편만 있는 모형과 모형의 적합성이 동일<br/>
       대립 가설: 절편만 있는 모형보다 모형의 적합성이 유의하게 높음<br/><br/>
      </strong>
      F-검정의 statistic의 p-value는 3e-26수준으로 회귀모형이 통계적 유의성을 가진 다는 것을 확인할 수 있다.<br/><br/>
<strong>
  각 계수에 대한 t검정 귀무 가설: 값이 0인 모형과 설명력이 동일<br/>
 대립 가설: 값이 0인 모형보다 설명력이 유의하게 높음<br/><br/>
</strong>
 t값이 절편에 대해 28.5, 거리에 대해 -8.6, 승객수에 대해 6.8 수준으로 '의심의 여지가 없이' 높은 것을 확인할 수 있다. 
 그러나 qq plot의 모양과 오차항의 잔차의 모양이 좋지않다. 잔차의 정규성과 등분산성이 만족하지 않으므로 이 모형을 채택할 수 없다. log변환을 실행한 후 다시 시도해보자.<br/>
    </p>
    </div>
    <send-code number="17">
cd, _ = OLSInfluence(res).cooks_distance<br>
cd.sort_values(ascending=False)[1:10]<br>
#1527, 17, 387, 1531, 5, 1354의 자료가 극단 값으로 보이고 이들을 제거해보기로 한다.<br>
metro_use_relation_log = metro_use_relation.copy()<br>
metro_use_relation_log.drop([1527, 17, 387, 1531, 5, 1354], inplace=True)<br>
metro_use_relation_log['이용건수'] = np.log1p(metro_use_relation_log['이용건수'])<br>
<br>
res = ols('이용건수 ~ 근처역거리 + 총승객수', data=metro_use_relation_log).fit()<br>
fitted = res.predict(metro_use_relation_log)<br>
residual = metro_use_relation_log['이용건수'] - fitted<br>
fig = plt.figure(figsize=(20, 5))<br>
ax1 = fig.add_subplot(1,3,1)<br>
ax2 = fig.add_subplot(1,3,2)<br>
ax3 = fig.add_subplot(1,3,3)<br>
sns.regplot(fitted, residual, lowess=True, line_kws={'color': 'red'}, ax=ax1 )<br>
stats.probplot(residual, dist=stats.norm,plot=ax2)<br>
sr = stats.zscore(residual)<br>
sns.regplot(fitted, np.sqrt(np.abs(sr)), lowess=True, line_kws={'color': 'red'}, ax=ax3 )<br>
fig.show()<br>
res.summary()<br>
  </send-code>
    <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/metro_use_relation_log_ols.png" class='frame' style="background-color: #fff"/>
    </div>
        <div class="d-flex justify-content-center">
      <img src="http://localhost:8000/static/figures/metro_use_relation_log_pp.png" class='frame' style="background-color: #fff"/>
    </div>

<div class="typography-line pt-5">
    <p>
      이번엔 분포가 너무 치우치지 않고 적당히 잘 나온 것 같으므로 이 회귀모형을 채택하자. 
      그러면 log(이용건수) = 8.5487 - 0.0003(근처역거리) + 2.173e-8(총승객수) => (이용건수) = 5160/e^(0.0003(근처역거리))*e^(2.173e-8(총승객수))<br><br>

      이용건수는 근처역의 6개월단위 총승객수가 531만명 늘 수록 2배씩 늘며 반대로 2310미터 거리가 멀어질마다 절반으로 주는 경향이 있다는 사실을 알 수 있다.
    </p>
    </div>



   </card>
    
</template>
<script>
import sendCode from 'src/components/Analysis/sendCode.vue';
import receiveCode from 'src/components/Analysis/recieveCode.vue';
import SendCode from '../../sendCode.vue';

export default {
    name : 'dynamic-004',
  components: {
    sendCode,
    receiveCode,
    SendCode
},
  data() {
    return {

    };
  }
};
</script>