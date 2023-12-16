<template>
  <ui5-input type="Text" v-model="componentPhoneField"
             :value-state="phoneValueState" maxlength="18"
             @input = "e => checkPhoneLength()"
             @change="changePhoneAction && changePhoneAction()" required>
    <div slot="valueStateMessage">{{ phoneStateText }}</div>
  </ui5-input>
  <input v-model="componentPhoneField" v-mask="'+7 (###) ###-##-##'" hidden>
</template>


<script>

export default {
  name: 'PhoneField',
  data() {
    return {
      componentPhoneField: ''
    }
  },
  props: {
    phoneValueState: {type: String},
    phoneStateText: {type: String},
    changePhoneAction: {type: Function}
  },
  methods: {
    checkPhoneLength() {
      if (this.componentPhoneField.length > 18) {
        this.componentPhoneField = this.componentPhoneField.substring(0, 17)
      }
    },
  }
}

</script>


<style scoped>

</style>