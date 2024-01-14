<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Информация о заявке">
        </ui5-card-header>
        <AppInformation ref="appInfoComponent"
                        v-if="appId.length > 0"
                        v-bind:loaderFunc="useLoader"
                        v-bind:showDialog="openDialog"
                        v-bind:appId="appId" />
      </ui5-card>
    </slot>
  </LkBase>
  <ui5-dialog ref="rejectedDialog">
    <ui5-bar slot="header">
      <ui5-title level="H5" slot="startContent">Отклонение заявки</ui5-title>
      <ui5-button design="Emphasized"
                  slot="endContent"
                  icon="decline"
                  @click="e => this.$refs.rejectedDialog.close(e.current)"></ui5-button>
    </ui5-bar>
    <ui5-label show-colon>Сообщение к заявке</ui5-label>
    <ui5-textarea ref="appMessage" />
    <div slot="footer" class="popover-footer">
      <div style="flex: 1;"></div>
      <ui5-button icon="decline"
                  design="Emphasized"
                  @click="e => appDecline(e)">
        Отклонить
      </ui5-button>
    </div>
  </ui5-dialog>
</template>

<script>

import LkBase from "../../../components/LkBase.vue";
import AppInformation from "../../../components/AppInformation.vue";

export default {
  name: 'AdminAppView',
  components: {AppInformation, LkBase},
  data() {
    return {
      appId: this.$route.params.appId
    }
  },
  methods: {
    useLoader() {
      this.$refs.baseComponent.useLoader()
    },
    openDialog() {
      this.$refs.rejectedDialog.show()
    },
    appDecline(e) {
      this.$refs.rejectedDialog.close(e.current)
      this.$refs.appInfoComponent.appDecline(
          this.$refs.appMessage.value
      )
    }
  }
}

</script>

<style scoped>

</style>