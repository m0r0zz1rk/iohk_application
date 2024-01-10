<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Информация о заявке">
        </ui5-card-header>
        <AppInformation v-if="eventId.length > 0"
                        v-bind:loaderFunc="useLoader"
                        v-bind:lkUser="true"
                        v-bind:eventId="eventId" />
      </ui5-card>
    </slot>
  </LkBase>
</template>

<script>

import LkBase from "../../../components/LkBase.vue";
import AppInformation from "../../../components/AppInformation.vue";

export default {
  name: 'AppView',
  components: {AppInformation, LkBase},
  data() {
    return {
      eventId: this.$route.params.eventId
    }
  },
  methods: {
    useLoader() {
      this.$refs.baseComponent.useLoader()
    }
  }
}

</script>

<style scoped>

</style>