<template>
  <base-nav
    v-model="showMenu"
    class="navbar-absolute top-navbar"
    type="white"
    :transparent="true"
  >
    <div slot="brand" class="navbar-wrapper">
      <div class="navbar-minimize d-inline"><sidebar-toggle-button /></div>
      <div
        class="navbar-toggle d-inline"
        :class="{ toggled: $sidebar.showSidebar }"
      >
        <button type="button" class="navbar-toggler" @click="toggleSidebar">
          <span class="navbar-toggler-bar bar1"></span>
          <span class="navbar-toggler-bar bar2"></span>
          <span class="navbar-toggler-bar bar3"></span>
        </button>
      </div>
      <a class="navbar-brand" href="#pablo">{{ routeName }}</a>
    </div>

    <ul class="navbar-nav" :class="$rtl.isRTL ? 'mr-auto' : 'ml-auto'">





            <base-dropdown
        tag="li"
        :menu-on-right="!$rtl.isRTL"
        title-tag="a"
        title-classes="nav-link"
        class="nav-item"
      >
        <template
          slot="title"
        >
          <i class="tim-icons icon-caps-small"></i>
          <p class="d-lg-none">{{$t('sidebar.language')}}</p>
        </template>
        <li v-for="lg in language" :key="lg" class="nav-link">
          <div @click="setLanguage(lg)" class="nav-item dropdown-item">{{lg}}</div>
        </li>


      </base-dropdown>
      
            <base-dropdown
        tag="li"
        :menu-on-right="!$rtl.isRTL"
        title-tag="a"
        title-classes="nav-link"
        class="nav-item"
        v-if="!isLoggedIn"
      >
        <template
          slot="title"
        >
          <i class="tim-icons icon-single-02"></i>
          <p class="d-lg-none">{{$t('sidebar.login')}}/{{$t('sidebar.signup')}}</p>
        </template>
        <li class="nav-link">
          <a v-on:click="handleLogin" class="nav-item dropdown-item">{{$t('accont.login')}}</a>
          
        </li>
        <li class="nav-link">
          <router-link to="/users/signup" class="nav-item dropdown-item">{{$t('accont.signup')}}</router-link>

        </li>

      </base-dropdown>


      <base-dropdown
        tag="li"
        :menu-on-right="!$rtl.isRTL"
        title-tag="a"
        class="nav-item"
        title-classes="nav-link"
        menu-classes="dropdown-navbar"
        v-else
      >

        <template
          slot="title"
        >
          <div class="photo"><img :src="image" /></div>
          <b class="caret d-none d-lg-block d-xl-block"></b>

          <b class="caret d-none d-lg-block d-xl-block"></b>
          <p class="d-lg-none">{{$t('sidebar.logout')}}</p>
        </template>
        <li class="nav-link">
          <router-link class="nav-item dropdown-item" to="/users/mypage">
            {{$t('sidebar.profile')}}
          </router-link>
        </li>
        <div class="dropdown-divider"></div>
        <li class="nav-link">
          <a class="nav-item dropdown-item" v-on:click="handleLogout">{{$t('sidebar.logout')}}</a>
        </li>
      </base-dropdown>
    </ul>
  </base-nav>
</template>
<script>
import { BaseNav, Modal } from '@/components';
import SidebarToggleButton from './SidebarToggleButton';
import { mapActions, mapState } from 'vuex';


export default {
  name: 'navbar',
  components: {
    SidebarToggleButton,
    BaseNav,
    Modal
  },
  computed: {
    routeName() {
      const { name } = this.$route;
      return this.capitalizeFirstLetter(name);
    },
    isRTL() {
      return this.$rtl.isRTL;
    },
    ...mapState(['isLoggedIn', 'image', 'username']),
  },
  data() {
    return {
      activeNotifications: false,
      showMenu: false,
      language : ['kr', 'en']
    };
  },
  methods: {
    
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    toggleNotificationDropDown() {
      this.activeNotifications = !this.activeNotifications;
    },
    closeDropDown() {
      this.activeNotifications = false;
    },
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    hideSidebar() {
      this.$sidebar.displaySidebar(false);
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    setLanguage(value){
      if (this.$i18n.locale !== value){
        this.$i18n.locale = value
      } 
    },
    handleLogin(event){
      event.preventDefault();
      this.$router.push(`/users/login?next=${this.$router.currentRoute.path}`);
    },
    handleLogout(event) {
      event.preventDefault();
      this.logout();
      this.$router.push('/');
    },
    ...mapActions(['logout']),
  },
};
</script>
<style scoped>
.top-navbar {
  top: 0px;
}
</style>
