# Seoulbike
<h3>따릉이 수요 예측 웹사이트 프로젝트</h3>

<ul>
<li>제작인원 : 1명</li>
<li>제작기간 : 2022-07-13 ~ 2022-08-11(1달)</li>
<li>제작목적 : 따릉이 대여소의 지도, 실시간 분석결과를 제공하여 따릉이 잠재적 고객의 편의성을 높이기 위한 취지로 제작</li>
<li>프레임워크 : Django v4.0.3 / Vue.js v2.6.14</li>

</ul>
<h5>따릉이 수요 예측 웹사이트 프로젝트</h5>
2015년 시범운행을 시작해 2017년부터 본격적으로 서비스를 시작한 따릉이 공유자전거 대여서비스는 이제는 매우 커져서
대여소만 2000개, 자전거 대수는 5만대에 이르는 거대한 서비스가 되었다.<br/><br/>

당신이 서울에 살고 있다면, 굳이 한강변에 가지 않더라도 어디서나 따릉이를 타는 시민들을 볼 수 있고, 또 그 수도 많다는 것을
한눈에 알 수 있다. 따릉이는 시작부터 공공사업의 성격을 띄었기 때문에 7년전과 같이 가격은 1시간에 1000원으로 유지되었으며
티머니GO와 같은 공공기관의 앱에 이용권 혜택을 주는 등, 소위 퍼주기식인 기조를 유지해왔다.<br/><br/>

서울시의 생활인구이동에 따른 교통체증 타개나, 시민들의 운동 생활화, 환경보존 등, 많은 요소에서 긍정적인
효과를 가지고 있는 이 사업은 성공적인 외연확장으로 서울시민들이 뽑은 '달라진 서울 풍경' 1위에 꼽히기도 했다. 서울 시민 3명 중
1명은 따릉이 회원이며 밴치마킹으로 삼았던 '밸리브' 사업보다도 성공적으로 안착했다는 평가를 받는다.<br/><br/>

파리가 2007년 도입한 공공자전거 밸리브는 2020년 기준 2만3600대를 운영 중이다. 
런던 BCH는 1만3600대(2017년), 뉴욕 시티바이크 1만2000대(2018년) 등 다른 도시들과 비교해도 많다.<br/><br/>

그러나 최근 코로나 발발과 맞물리면서 관련 노동자의 수는 감축되고, 오히려 그동안 따릉이를 이용하는 사람들은 늘어났다.
서울시는 매년 100억원씩 발생하는 적자를 해결하기 위해 광고 유치를 하반기부터 진행할 예정이라고 밝혔다.<br/><br/>

3년차 정기권을 구매한 필자도 일상에서 자전거를 어디서나 대여해 
돈과 시간도 아끼고, 운동까지 겸할 수 있다는 것이 마음에 들었고, 또 현재도 애용중이다. 따릉이를 이용해 본 적이 있는
사람이라면 알겠지만, 생각보다 대여소가 촘촘히 배치되어 있어, 시가지라면 5분 이내로 걸어서 근처 대여소를 찾을 수 있다.<br/><br/>

다만 사람들이 많은 곳에는 그만큼 자전거 수요도 많아 정작 찾아갔더니 자전거가 부족한 경우가 발생할 수도 있다.
보통 그런 곳에는 설치된 자전거 대여소도 규모가 크지만 수요를 감당하기에는 역부족인것 같다.
홍대, 신도림, 종로, 강남, 건대에서 그와 같은 경험을 했고 근처 다른 대여소로 걸어가는 발걸음은 생각보다 길다.<br/><br/>

따릉이 앱에서는 각 대여소마다 따릉이의 잔여대수를 제공하고 있다. 만약 1대나 2대가 남았다면 서둘러야 한다.
그것을 본 다른 사람들도 서두를 것이기 때문이다. 필자는 본인이 겪은 굉장히 사소하고 시덥잖은 문제에서 해결책을 찾기 위해
소위 '머신러닝'이라고 부르는 간드러지는 데이터분석 기법을 이용해보기로 했다.<br/><br/>

2시간 후에 일정이 끝나는 데 근처 대여소에 따릉이가 5대 남았다면? 내가 있는 곳이 신림동 언덕배기라면 괜찮을 수도 있다.
하지만 마포구 시내라면? 조금 힘들수도 있겠다. 하지만 빌리는 사람이 많은 대여소는 반납하는 사람도 많지
않을까? 그러나 또 이것은 시간에 따라, 요일에 따라 다를 것이다. 이 프로젝트는 이러한
질문에 답하기 위해 시작했다.<br/><br/>

다음은 이 프로젝트로 기대할 수 있는 3가지 스케일의 솔루션이다.<br/><br/>
<ol>
<li>내가 따릉이를 이용 계획을 가질 때, 헛걸음을 하지 않도록 동선을 짜도록 도와준다.</li>
<li>다른 사람들도 따릉이를 이용할 때 같은 혜택을 받을 수 있도록 한다.</li>
<li>따릉이 사업을 관리하는 서울시의 입장에서, 어떤 대여소가 어떤 시간에 추가적인 따릉이 배치가 필요할지 파악하는데 도움을 준다.</li>
</ol>

    
