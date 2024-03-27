<template>
  <ui5-input :type="fieldType"
             style="width: 100%"
             placeholder="Пароль"
             required :value-state="this.valueState"
             @input="e => passwordStr = e.target.value">
    <ui5-icon v-show="!(passwordShow)"
              interactive
              slot="icon"
              name="show"
              @click="showHidePassword();">
    </ui5-icon>
    <ui5-icon v-show="passwordShow"
              interactive
              slot="icon"
              name="hide"
              @click="showHidePassword();">
    </ui5-icon>
    <div slot="valueStateMessage">{{ valueStateText }}</div>
  </ui5-input>
</template>

<script>
export default {
  name: 'PasswordField',
  data() {
    return {
      fieldType: 'Password',
      passwordShow: false,
      passwordStr: '',
      valueState: 'None',
      valueStateText: ''
    }
  },
  methods: {
    showHidePassword() {
      if (this.fieldType === 'Password') {
        this.fieldType = 'Text'
        this.passwordShow = true
      } else {
        this.fieldType = 'Password'
        this.passwordShow = false
      }
    }
  }
}

</script>

<style scoped>
  .password_field {
    background: none;
    padding: 2px;
    font-weight: 700;
    width: 75%;
    transition: .2s;
  }

</style>