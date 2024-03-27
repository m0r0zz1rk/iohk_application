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
                        v-bind:setResult="openResultDialog"
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
  <ui5-dialog ref="resultDialog">
    <ui5-bar slot="header">
      <ui5-title level="H5" slot="startContent">Результат по заявке</ui5-title>
      <ui5-button design="Emphasized"
                  slot="endContent"
                  icon="decline"
                  @click="e => this.$refs.resultDialog.close(e.current)"></ui5-button>
    </ui5-bar>
    <div v-if="resultHTML.length > 0">
      <TinyMCE ref='resultTinyMCE'
               v-bind:Information="resultHTML"
               v-bind:editorHeight="500" />
    </div>
    <div slot="footer" class="popover-footer">
      <div style="flex: 1;"></div>
      <ui5-button icon="complete"
                  design="Emphasized"
                  @click="e => appResult(e)">
        Установить результат
      </ui5-button>
    </div>
  </ui5-dialog>
</template>

<script>

import LkBase from "../../../components/LkBase.vue";
import AppInformation from "../../../components/AppInformation.vue";
import TinyMCE from "../../../components/TinyMCE.vue";

export default {
  name: 'AdminAppView',
  components: {TinyMCE, AppInformation, LkBase},
  data() {
    return {
      componentKey: 0,
      appId: this.$route.params.appId,
      resultHTML: ''
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
    },
    openResultDialog(result) {
      if (result.length !== 0) {
        this.resultHTML = result
      } else {
        this.resultHTML = '<p>Результат</p>'
      }
      this.$refs.resultDialog.show()
      this.componentKey += 1
    },
    appResult(e) {
      this.$refs.resultDialog.close(e.current)
      this.$refs.appInfoComponent.appResult(
          this.$refs.resultTinyMCE.editorText
      )
    }
  }
}

</script>

<style scoped>

</style>