import VueRouter from 'vue-router';
import routes from './routes';
import { ACCESS_TOKEN, REFRESH_TOKEN, refreshToken } from '../login/auth';



// configure router
const router = new VueRouter({
  routes, // short for routes: routes
  linkActiveClass: 'active',
  scrollBehavior (to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      window.scrollTo({top: 0, left: 0});
    }
  }
});


const Authenticated = () => (
    (ACCESS_TOKEN in window.localStorage) && (REFRESH_TOKEN in window.localStorage));
router.beforeEach(async(to, from, next) => {

  if(to.meta.private){
    if (!Authenticated()) {
      next(`/users/login?next=${to.path}`);
    }
  }
  if(to.meta.unauthed){
    if (Authenticated()) {
      //next(from.path);
    }
  }
  next();
});



export default router;
