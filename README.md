# Seoulbike
<h3>따릉이 수요 예측 웹사이트 프로젝트</h3>

<ul>
<li>제작인원 : 1명</li>
<li>제작기간 : 2022-07-13 ~ 2022-08-11(1달)</li>
<li>제작목적 : 따릉이 대여소의 지도, 각 대여소마다의 실시간 분석결과를 제공하여 따릉이 잠재적 고객의 편의성을 높이기 위한 취지로 제작</li>
<li>프레임워크 : Django v4.0.3 / Vue.js v2.6.14</li>

</ul>
<br/>
<br/>
<h4>구성</h4>
<ul>
<li>backend/ :   백엔드(장고) 폴더</li>
    <ul>
    <li>auth/ :     로그인 사용자의 백엔드 jwt인증을 담당</li>
    <li>config/ :   local, prod의 setting과 관리자 api를 담당</li>
    <li>seoulbike/ :     주기능 app</li>
        <ul>
        <li>buildAnalysis.py :   서버 실행시에 인스턴스를 생성하여 예측결과를 내놓는데 사용하는 Forecast class와 예측을 위한 날씨정보를 얻는데 사용하는 weatherForecast class를 포함</li>
        <li>cron.py :   실시간 정보를 부하없이 제공하기 위해 각 사용자의 호출마다 따릉이 api를 호출하지 않고, 서버에서 5분마다 따릉이 api를 호출한 결과를 저장 후 제공하기 위한 cronjob. 또 1시간마다 그 히스토리를 DB에 저장하여 향후 분석의 window로 사용함.</li>
        <li>models.py :  대여소, 회원, 댓글, 대여히스토리의 모델을 담당</li>
        <li>permissions.py :  비로그인 시에도 서비스를 이용할 수 있도록 IsAdminUserOrReadOnly, IsAuthenticatedOrReadAndWrite를 만듦</li>
        <li>views.py :  ModelViewset을 이용. Admin과 User의 view를 분리. search filter, partial update, 중복 아이디체크, 대여소 즐겨찾기 field의 json pasre, 비밀번호 변경, 비밀번호 확인과 암호화 등을 구현</li>
        </ul>
    <li>static/ :  백엔드에서 사용할 정적 파일들을 보관</li>
         <ul>
        <li>models/ :  각 대여소의 머신러닝 모델</li>
        <li>scalers/ :  각 머신러닝 모델의 X_train을 스케일할 때 사용했던 스케일러</li>
        </ul>
    <li>templates/ :  비밀번호 리셋을 위한 이메일에 첨부할 html을 포함</li>
    </ul>
    <br/>
<li>frontend/ : 프론트엔드(vue.js) 폴더 - 이미 만들어진 template으로부터 시작</li>
    <ul>
    <li>src/</li>
        <ul>
        <li>components/ : 페이지의 구성 요소를 담은 폴더</li>
            <ul>
            <li>Analysis/ : 분석 소개 페이지의 Lazy loading component들</li>
            <li>bike/ : 지도 페이지에서 자주 사용되는 댓글 template과 지도 template을 보관</li>    
            <li>forms/SubmitCard.vue :  form의 일반적인 형태를 구성</li>   
            <li>AnalysisBoard.vue :  대여소의 예측결과와 히스토리를 그래프로 제공하는 component</li>  
            <li>bikeTable.vue :  대여소 테이블 component</li>  
            <li>reviewTable.vue :  댓글의 작성과 수정, 비밀번호 작성, 페이징을 담당하는 component</li> 
            </ul>
        <li>locales/ : 2개 언어 지원을 위한 i18n의 kr.json, en.json을 보관</li>    
        <li>login/auth.js :  jwt 로그인 관리를 위한 localstorage 세팅과 refresh token의 시용 및 재발급을 담당</li>    
        </ul>
        <li>pages/ : 페이지를 담은 폴더</li>
            <ul>
            <li>Forms/ : 회원가입을 위한 Wizard</li>
            <li>seoulbike/ : 관리자 페이지, 마이 페이지, 비밀번호 리셋 페이지, 지도 페이지를 보관</li>    
            <li>EDA-1.vue, EDA-2.vue, MachineLearning.vue : 분석 소개 페이지</li>   
            <li>Seoulbike.vue : 로그인과 지도보기를 할 수 있는 홈페이지</li>  
            </ul>
        <li>plugins/errorHandler.js : 에러 alert 출력을 위한 플러그인</li>
        <li>storage/userspots.js : localStorage를 이용한 대여소 즐겨찾기 기능 구현</li>
        <li>store/index.js : Vuex를 이용한 유저정보 store</li>
    </ul>
</ul>
<br/>
<br/>
<h4>개요</h4>
2015년 시범운행을 시작해 2017년부터 본격적으로 서비스를 시작한 따릉이 공유자전거 대여서비스는 이제는 매우 커져서
대여소만 2000개, 자전거 대수는 5만대에 이르는 거대한 서비스가 되었다. 3년차 정기권을 구매한 필자도 일상에서 자전거를 어디서나 대여해 
돈과 시간도 아끼고, 운동까지 겸할 수 있다는 것이 마음에 들었고, 또 현재도 애용중이다. 따릉이를 이용해 본 적이 있는
사람이라면 알겠지만, 생각보다 대여소가 촘촘히 배치되어 있어, 시가지라면 5분 이내로 걸어서 근처 대여소를 찾을 수 있다.<br/><br/>

다만 사람들이 많은 곳에는 그만큼 자전거 수요도 많아 정작 찾아갔더니 자전거가 부족한 경우가 발생할 수도 있다.
보통 그런 곳에는 설치된 자전거 대여소도 규모가 크지만 수요를 감당하기에는 역부족인것 같다.
홍대, 신도림, 종로, 강남, 건대에서 그와 같은 경험을 했고 근처 다른 대여소로 걸어가는 발걸음은 생각보다 길다.<br/><br/>

따릉이 앱에서는 각 대여소마다 따릉이의 잔여대수를 제공하고 있다. 만약 1대나 2대가 남았다면 서둘러야 한다.
그것을 본 다른 사람들도 서두를 것이기 때문이다. 필자는 본인이 겪은 굉장히 사소하고 시덥잖은 문제에서 해결책을 찾기 위해
소위 '머신러닝'이라고 부르는 간드러지는 데이터분석 기법을 이용해보기로 했다. 2시간 후에 일정이 끝나는 데 근처 대여소에 따릉이가 5대 남았다면? 
내가 있는 곳이 신림동 언덕배기라면 괜찮을 수도 있다. 하지만 마포구 시내라면? 조금 힘들수도 있겠다. 하지만 빌리는 사람이 많은 대여소는 반납하는 사람도 많지
않을까? 그러나 또 이것은 시간에 따라, 요일에 따라 다를 것이다. 이 프로젝트는 이러한
질문에 답하기 위해 시작했다.<br/><br/>

다음은 이 프로젝트로 기대할 수 있는 3가지 스케일의 솔루션이다.<br/>
<ol>
<li>내가 따릉이를 이용 계획을 가질 때, 헛걸음을 하지 않도록 동선을 짜도록 도와준다.</li>
<li>다른 사람들도 따릉이를 이용할 때 같은 혜택을 받을 수 있도록 한다.</li>
<li>따릉이 사업을 관리하는 서울시의 입장에서, 어떤 대여소가 어떤 시간에 추가적인 따릉이 배치가 필요할지 파악하는데 도움을 준다.</li>
</ol>

    
