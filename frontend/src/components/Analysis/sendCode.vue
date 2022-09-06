<template>
<collapse :multiple-active="false">
    <collapse-item headclass="text-center" title="-------------------------code-------------------------">
            
        <div class="typography-line">
            <span>[{{number}}] ------</span>
        <blockquote>
            <p class="blockquote">
                <code>
                    <slot>
                    </slot>
        </code>
        </p></blockquote>
        </div>
        </collapse-item>
    </collapse>
</template>
<script>
import {Collapse, CollapseItem } from 'src/components';

export default {
  components: {
    Collapse,
    CollapseItem
  },
  props : ['number'],
  data() {
    return {

    };
  }
};
</script>
