<template>
  <div class="login-container-parent"></div>
  <div class="half_width_and_center" style="top: 10%">
    <ui5-card style="justify-content: center">
      <div style="width: 50%; margin: 0 auto; justify-content: center; text-align: center; padding-bottom: 10px">
        <h3 style="color: #00455d;">Смена пароля</h3>
        <ui5-label show-colon>Новый пароль:</ui5-label><PasswordField ref="pass1" /><br/><br/>
        <ui5-label show-colon>Подтверждение:</ui5-label><PasswordField ref="pass2" /><br/><br/>
        <ui5-button icon="private"
                    @click="e => passwordReset()">Сменить пароль</ui5-button>
      </div>
    </ui5-card>
  </div>
  <PreLoader ref="preLoader" />
</template>

<script>

import PasswordField from "../components/PasswordField.vue";
import PreLoader from "../App.vue";
import {apiRequest} from "../additional/functions/api_request.js";
import {showMessage} from "../additional/functions/message-strips.js";

export default {
  name: 'PasswordReset',
  components: {PreLoader, PasswordField},
  data() {
    return {
      repairToken: this.$route.query.token
    }
  },
  methods: {
    passwordReset() {
      if ((this.$refs.pass1.passwordStr.length === 0) || (this.$refs.pass2.passwordStr.length === 0)) {
        showMessage('error', 'Заполните оба поля пароля')
        return false
      }
      if (this.$refs.pass1.passwordStr !== this.$refs.pass2.passwordStr) {
        showMessage('error', 'Введенные пароли не совпадают')
        return false
      }
      if (this.$refs.pass1.passwordStr.length < 8) {
        showMessage('error', 'Минимальная длина пароль - 8 символов')
        return false
      }
      this.$refs.preLoader.usePreloader()
      apiRequest(
          '/api/v1/password_reset/confirm/',
          'POST',
          false,
          {
            'password': this.$refs.pass1.passwordStr,
            'token': this.repairToken
          },
          false,
          false
      )
          .then(data => {
            if (data.error) {
              showMessage('error', 'Произошла ошибка, повторите попытку позже')
            } else {
              showMessage('success', 'Пароль успешно изменен')
              this.$router.push('/')
            }
            this.$refs.preLoader.usePreloader()
          })
    }
  }
}

</script>

<style scope>

</style>