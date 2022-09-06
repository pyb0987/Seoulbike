import DashboardLayout from 'src/pages/Layout/DashboardLayout.vue';
import AuthLayout from 'src/pages/Pages/AuthLayout.vue';
import IndexLayout from 'src/pages/Layout/IndexLayout.vue'
// GeneralViews
import NotFound from 'src/pages/GeneralViews/NotFoundPage.vue';


 const Seoulbike = () =>
 import(/* webpackChunkName: "seoulbike" */ 'src/pages/Seoulbike.vue');
 const BikeBoard = () =>
 import(/* webpackChunkName: "seoulbike" */ 'src/pages/seoulbike/BikeBoard.vue');
 const Spots = () =>
 import(/* webpackChunkName: "seoulbike" */ 'src/pages/seoulbike/Spots.vue');
 const Login = () =>
 import(/* webpackChunkName: "pages" */ 'src/pages/Pages/Login.vue');
 const MyPage = () =>
 import(/* webpackChunkName: "pages" */ 'src/pages/seoulbike/MyPage.vue');
 const Wizard = () => import('src/pages/Forms/Wizard.vue');
 const NewPassword = () =>
 import(/* webpackChunkName: "pages" */ 'src/pages/seoulbike/NewPassword.vue');

const EDA1 = () =>
import(/* webpackChunkName: "analysis" */ 'src/pages/EDA-1.vue');
const EDA2 = () =>
import(/* webpackChunkName: "analysis" */ 'src/pages/EDA-2.vue');
const MachineLearning = () =>
import(/* webpackChunkName: "analysis" */ 'src/pages/MachineLearning.vue');


let seoulbike = {
  path : '/seoulbike',
  component : DashboardLayout,
  redirect : '/seoulbike/spots',
  name : 'Seoulbike',
  children : [
    {
      path : 'supervise',
      name : 'Seoulbike',
      components : {default : BikeBoard},
      meta : {private : true, unauthed : false} //private
    },
    {
      path : 'spots',
      name : 'Seoulbike Spots',
      components : {default : Spots},
      meta : {private : false, unauthed : false}
    },
  ]
}

let users = {
    path: '/users',
    component: DashboardLayout,
    redirect: '/users/signup',
    name: 'Users',
    children: [
      {
        path: 'signup',
        name: 'Sign Up',
        components: { default: Wizard },
        meta : {private : false, unauthed : true}
      },
      {
        path: 'login',
        name: 'Log In',
        components: { default: Login },
        meta : {private : false, unauthed : true}
      },
      {
        path: 'mypage',
        name: 'My Page',
        components: { default: MyPage },
        meta : {private : true, unauthed : false} //private
      },
      {
        path: 'renew-password',
        name: 'Renew Password',
        components: { default: NewPassword },
        meta : {private : false, unauthed : true}
      },
    ]
  };

let analysis = {
  path: '/analysis',
  component: DashboardLayout,
  redirect: '/analysis/eda-1',
  name: 'Analysis',
  children: [
    {
      path: 'eda-1',
      name: 'EDA-1',
      components: { default: EDA1 },
      meta : {private : false, unauthed : false}
    },
    {
      path: 'eda-2',
      name: 'EDA-2',
      components: { default: EDA2 },
      meta : {private : false , unauthed : false}
    },
    {
      path: 'machinelearning',
      name: 'Machine Learning',
      components: { default: MachineLearning },
      meta : {private : false , unauthed : false}
    }
  ]
  
  }



const routes = [
  {
    path: '/',
    redirect: '/index',
    name: 'Home'
  },
  users,
  seoulbike,
  analysis,
  {
    path: '/',
    component: IndexLayout,
    redirect: '/index',
    name: 'Dashboard layout',
    children: [
      {
        path: 'index',
        name: 'index',
        components: { default: Seoulbike }
      },
    ]
  },
  {
    path: '*',
    component: AuthLayout,
    name: 'Not Found',
    children: [
      {
        path: '*',
        name: 'Not Found',
        components: { default: NotFound }
      } 
    ]
  },
];

export default routes;
