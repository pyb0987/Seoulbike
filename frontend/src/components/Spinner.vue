<template>
  <div class="spinner" v-if="loading">              
    <div>
    </div>
    <div>
    </div>
    <div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    loading: {                                              
      type: Boolean,
      required: true,
    },
  },
}
</script>

<style>
.spinner {
  position: relative;
  width: 80px;
  height: 64px;
  top: 47%;
  left: 47%;
}
.spinner div {
  display: inline-block;
  position: absolute;
  left: 6px;
  width: 13px;
  background: #868ba8;
  animation: spinner 1.2s cubic-bezier(0, 0.8, 0.8, 1) infinite;
}
.spinner div:nth-child(1) {
  left: 6px;
  animation-delay: -0.24s;
}
.spinner div:nth-child(2) {
  left: 32px;
  animation-delay: -0.12s;
}
.spinner div:nth-child(3) {
  left: 57px;
  animation-delay: 0;
}
@keyframes spinner {
  0% {
    top: 6px;
    height: 51px;
  }
  50%, 100% {
    top: 19px;
    height: 26px;
  }
}
</style>