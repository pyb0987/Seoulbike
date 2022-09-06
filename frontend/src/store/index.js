import Vue from 'vue';
import Vuex from 'vuex';
import createPersistedState from 'vuex-persistedstate'
import { loginUser, logoutUser, jwtInterpreter, BASE_URL } from '../login/auth';
import { LogoutSpotSet } from 'src/storage/userspots'
Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    username: null,
    user_id: null,
    image: BASE_URL +"/media/" + "image/placeholder.jpg",
    isLoggedIn: false,
    is_superuser : false,
  },
  mutations: {
    loginSuccess(state, value) {
      console.log('mutatino', value)
      state.username = value.infoObj['username'];
      state.user_id = value.infoObj['user_id'];
      state.is_superuser = value.infoObj['is_superuser'];
      if(!!value.infoObj['image']){
        state.image = value.infoObj['image'];
      }

      state.isLoggedIn = true;
    },
    logout(state) {
      state.username = null;
      state.isLoggedIn = false;
      state.is_superuser = false;
      state.image = BASE_URL +"/media/" + "image/placeholder.jpg";
      state.user_id = null;
    },
  },
  getters:{
    getID(state) {   
      return state.user_id;
    }
  },
  actions: {
    login({ commit }, { username, password }) {
      return loginUser(username, password)
        .then((res) => {
          let infoObj = jwtInterpreter(res.access);
          console.log(infoObj)
          commit({ type: 'loginSuccess', infoObj });
          return Promise.resolve(infoObj['user_id']);
        }).catch((error) => {
          commit({ type: 'logout' });
          return Promise.reject(error);
        });
    },
    update({ commit }, { data}) {
        let infoObj = data
        if (!!infoObj.image){
          infoObj.image = BASE_URL + infoObj.image
        }
        commit({ type: 'loginSuccess', infoObj });
    },
    logout({ commit, getters }) {
      let user_id = getters.getID
      LogoutSpotSet(user_id)
      logoutUser();

      commit('logout');
    },
  },
  modules: {
  },
  plugins : [
    createPersistedState()
  ]
});