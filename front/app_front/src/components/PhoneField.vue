<template>
  <ui5-input v-if="appChangePhoneAction"
             type="Text" v-model="componentPhoneField"  placeholder="+7 (###) ###-##-##"
             :value-state="phoneValueState" maxlength="18"
             @input = "e => checkPhoneLength(e)"
             :readonly="readOnly"
             @change="appChangePhoneAction(fieldObjectID, componentPhoneField)" required>
    <div slot="valueStateMessage">{{ phoneStateText }}</div>
  </ui5-input>
  <ui5-input v-if="!(appChangePhoneAction)"
             type="Text" v-model="componentPhoneField"  placeholder="+7 (###) ###-##-##"
             :value-state="phoneValueState" maxlength="18"
             @input = "e => checkPhoneLength(e)"
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
      componentPhoneField: this.phoneValue || ''
    }
  },
  props: {
    phoneValue: {type: String},
    readOnly: {type: Boolean},
    phoneValueState: {type: String},
    phoneStateText: {type: String},
    fieldObjectID: {type: String},
    changePhoneAction: {type: Function},
    appChangePhoneAction: {type: Function}
  },
  methods: {
    checkPhoneLength(e) {
      if (this.componentPhoneField.length > 18) {
        this.componentPhoneField = this.componentPhoneField.substring(0, 17)
      }
    },
  }
}

</script>


<style scoped>

</style>