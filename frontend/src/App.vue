<template>
  <router-view></router-view>
</template>

<script>

import { mapActions, mapState } from 'vuex';

export default {
  computed: {
    ...mapState(['isLoggedIn']),
  },
  methods: {
    initializeLayout() {
      if (!this.$rtl.isRTL) {
        // Just make sure rtl css is off when we are not on rtl
        this.$rtl.disableRTL();
      }
    },
    handleLogout(event) {
      event.preventDefault();
      this.logout();
      this.$router.push('/');
    },
    ...mapActions(['logout']),
  },
  mounted() {
    this.initializeLayout();
  }
};
</script>
