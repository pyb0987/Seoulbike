<template>
    <div class="row pb-3">
        <div class="col-2 d-flex align-items-center flex-column">
            <img class="userImage" :src="imgsrc" alt="userImage" />
        <h5 class="title">{{this.username}}</h5>
    </div>
    <div class="col-10 col-md-8 form-floating">
        <blockquote class="col-12">
        <slot name="quote">

        </slot>
        </blockquote>
    </div>
    <div class="col-12 col-md-2">
        <slot name="button"></slot>
    </div>       
    </div>
</template>

<script>
export default {
    name : 'review',
    components: {
    },
    props : ['imgsrc', 'username'],
    data() {
    return {
    }
    },

}
</script>