<template>
  <div>
    <base-nav
      v-model="showMenu"
      type="white"
      :transparent="true"
      menu-classes="justify-content-end"
      class="auth-navbar fixed-top"
    >
      <div slot="brand" class="navbar-wrapper">
        <a class="navbar-brand" href="#" v-if="title">{{ title }}</a>
      </div>

      <ul class="navbar-nav">
        <router-link class="nav-item" tag="li" to="/">
          <a class="nav-link text-primary">
            <i class="tim-icons icon-minimal-left"></i> Back to Main
          </a>
        </router-link>

        <router-link v-if="!isLoggedIn" class="nav-item" tag="li" to="/users/login">
          <a class="nav-link">
            <i class="tim-icons icon-single-02"></i> {{$t('sidebar.login')}}
          </a>
        </router-link>
        <router-link v-if="!isLoggedIn" class="nav-item" tag="li" to="/users/signup">
          <a class="nav-link">
            <i class="tim-icons icon-spaceship"></i> {{$t('sidebar.signup')}}
          </a>
        </router-link>

        <router-link v-if="isLoggedIn" class="nav-item" tag="li" to="/users/mypage">
          <a class="nav-link">
            <i class="tim-icons icon-settings"></i> {{$t('sidebar.profile')}}
          </a>
        </router-link>
        <div v-if="isLoggedIn" v-on:click="handleLogout" class="nav-item" tag="li">
          <a class="nav-link">
            <i class="tim-icons icon-user-run"></i> {{$t('sidebar.logout')}}
          </a>
        </div>

      </ul>
    </base-nav>

    <div class="wrapper wrapper-full-page">
      <div class="full-page" :class="pageClass">
        <div class="content">
          <zoom-center-transition
            :duration="pageTransitionDuration"
            mode="out-in"
          >
            <router-view></router-view>
          </zoom-center-transition>
        </div>
              <footer class="footer">
          <div class="container-fluid">
            <nav>
              <ul class="nav">
                <li class="nav-item">
                  <p>
                      pyb0987@naver.com
                  </p>
                </li>
                <li class="nav-item">
                  <a
                    href="https://github.com/pyb0987"
                    target="_blank"
                    rel="noopener"
                    class="nav-link"
                  >
                    github
                  </a>
                </li>
              </ul>
            </nav>
            <div class="copyright">
              &copy; {{ year }} Seoulbike
            </div>
          </div>
        </footer>
      </div>
    </div>
  </div>
</template>
<script>
import { BaseNav } from 'src/components';
import { ZoomCenterTransition } from 'vue2-transitions';
import { mapActions, mapState } from 'vuex';

export default {
  components: {
    BaseNav,
    ZoomCenterTransition
  },
  props: {
    backgroundColor: {
      type: String,
      default: 'black'
    }
  },
  data() {
    return {
      showMenu: false,
      menuTransitionDuration: 250,
      pageTransitionDuration: 200,
      year: new Date().getFullYear(),
      pageClass: 'login-page'
    };
  },
  computed: {
    title() {
      return `${this.$route.name} Page`;
    },
    ...mapState(['isLoggedIn', 'image', 'username']),
  },
  methods: {
    ...mapActions(['logout']),
    toggleNavbar() {
      document.body.classList.toggle('nav-open');
      this.showMenu = !this.showMenu;
    },
    closeMenu() {
      document.body.classList.remove('nav-open');
      this.showMenu = false;
    },
    setPageClass() {
      this.pageClass = `${this.$route.name}-page`.toLowerCase();
    },
    handleLogout() {
      this.logout();
    }
  },
  beforeDestroy() {
    this.closeMenu();
  },
  beforeRouteUpdate(to, from, next) {
    // Close the mobile menu first then transition to next page
    console.log('asdf')
    if (this.showMenu) {
      this.closeMenu();
      setTimeout(() => {
        next();
      }, this.menuTransitionDuration);
    } else {
      next();
    }

  },
  mounted() {
    this.setPageClass();
  },
  watch: {
    $route() {
      this.setPageClass();
    }
  }
};
</script>
<style lang="scss">
.navbar.auth-navbar {
  top: 0;
}

$scaleSize: 0.8;
@keyframes zoomIn8 {
  from {
    opacity: 0;
    transform: scale3d($scaleSize, $scaleSize, $scaleSize);
  }
  100% {
    opacity: 1;
  }
}

.wrapper-full-page .zoomIn {
  animation-name: zoomIn8;
}

@keyframes zoomOut8 {
  from {
    opacity: 1;
  }
  to {
    opacity: 0;
    transform: scale3d($scaleSize, $scaleSize, $scaleSize);
  }
}

.wrapper-full-page .zoomOut {
  animation-name: zoomOut8;
}
</style>
