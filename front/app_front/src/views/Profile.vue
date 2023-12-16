<template>
  <LkBase ref="baseComponent">
    <slot>
      <div class="card-div">
        <ProfileForm ref="profile_form"
                     v-bind:isAdmin="false"
                     v-bind:profileData="profileData"
                     v-bind:profileFormAction="checkUniqueData"
                     v-bind:passwordFormAction="changePassword" />
      </div>
    </slot>
  </LkBase>
</template>

<script>

import LkBase from "../components/LkBase.vue";
import PasswordField from "../components/PasswordField.vue";
import PhoneField from "../components/PhoneField.vue";
import ProfileForm from "../components/ProfileForm.vue";
export default {
  components: {
    ProfileForm,
    PhoneField,
    PasswordField,
    LkBase
  },
  data() {
    return {
      afterLoad: true,
      states: [],
      profileData: [],
      profilePhoneField: '',
      profileEmailField: '',
      selectedRole: ''
    }
  },
  methods: {
    async getProfileData() {
      await fetch(this.$store.state.backendUrl+'/api/v1/auth/profile/', {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Authorization': 'Token '+getCookie('iohk_token')
        }
      })
          .then(resp => resp.json())
          .then(data => {
            if (data.error) {
              showMessage('error', data.error, false)
            } else {
              this.profileData = data
              this.$refs.profile_form.$refs.profile_phone.componentPhoneField = data.phone
              this.selectedRole = data.role
              if (this.afterLoad) {
                this.$refs.baseComponent.useLoader()
                this.afterLoad = false
              }
            }
          })
    },
    async checkUniqueData() {
      if (this.$refs.profile_form.$refs.profile_phone.componentPhoneField.length !== 18) {
        showMessage('error', 'Некорректный формат номера телефона')
        return false
      }
      let date_birth = convertToJSDate(this.$refs.profile_form.$refs.profile_birthday.value)
      let age = Math.floor((new Date() - new Date(date_birth).getTime()) / 3.15576e+10)
      let data = {
        'state': this.$refs.profile_form.$refs.profile_state.selectedOption.innerText,
        'surname': this.$refs.profile_form.$refs.profile_surname.value,
        'name': this.$refs.profile_form.$refs.profile_name.value,
        'patronymic': this.$refs.profile_form.$refs.profile_patronymic.value,
        'sex': this.$refs.profile_form.$refs.profile_sex._state.checked,
        'birthday': this.$refs.profile_form.$refs.profile_birthday.value,
        'age': age,
        'email': this.$refs.profile_form.$refs.profile_email.value,
        'phone': this.$refs.profile_form.$refs.profile_phone.componentPhoneField,
        'oo_fullname': '',
        'oo_shortname': ''
      }
      if (this.profileData.role === 'Администраторы') {
        data.role = 'Администраторы'
      } else {
        data.role = this.$refs.profile_form.$refs.profile_role.selectedOption.innerText
      }
      if (data.role === 'Преподаватели') {
        data.oo_fullname = this.$refs.profile_form.$refs.profile_oo_fullname.value
        data.oo_shortname = this.$refs.profile_form.$refs.profile_oo_shortname.value
      }
      this.$refs.baseComponent.useLoader()
      let that = this
      await fetch(this.$store.state.backendUrl+'/api/v1/auth/check_change_phone/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
        body: JSON.stringify({
          'phone': this.$refs.profile_form.$refs.profile_phone.componentPhoneField
        })
      })
          .then(async function(response) {
            if (response.status !== 200) {
              showMessage('error', 'Указанный номер телефона уже использован')
              that.$refs.baseComponent.useLoader()
              return false
            } else {
              await fetch(that.$store.state.backendUrl+'/api/v1/auth/check_change_email/', {
                method: 'POST',
                headers: {
                  'X-CSRFToken': getCookie("csrftoken"),
                  'Content-Type': 'web_app/json',
                  'Authorization': 'Token '+getCookie('iohk_token')
                },
                body: JSON.stringify({
                  'email': that.$refs.profile_form.profileEmailField
                })
              })
                  .then(async function(response) {
                    if (response.status !== 200) {
                      showMessage('error', 'Указанный email уже использован')
                      that.$refs.baseComponent.useLoader()
                    } else {
                      await that.profileChange(data)
                    }
                  })
            }
          })
    },
    async profileChange(data) {
      await fetch(this.$store.state.backendUrl+'/api/v1/auth/change_profile/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
        body: JSON.stringify(data)
      })
          .then(response => {
            if (response.status === 200) {
              return response.json()
            } else {
              showMessage('error', 'Произошла ошибка, повторите попытку позже')
              this.$refs.baseComponent.useLoader()
            }
          })
          .then(data => {
            if (data['error']) {
              showMessage('error', data['error'])
            } else {
              showMessage('success', data['success'])
            }
            this.getProfileData()
            this.$refs.baseComponent.useLoader()
          })
    },
    async changePassword() {
      if (this.$refs.profile_form.$refs.password1.passwordStr.length < 8) {
        this.$refs.profile_form.$refs.password1.valueState = 'Error'
        this.$refs.profile_form.$refs.password1.valueStateText = 'Минимальная длина пароля - 8 символов'
        return false
      } else {
        this.$refs.profile_form.$refs.password1.valueState = 'None'
      }
      if (this.$refs.profile_form.$refs.password1.passwordStr !== this.$refs.profile_form.$refs.password2.passwordStr) {
        this.$refs.profile_form.$refs.password1.valueState = 'Error'
        this.$refs.profile_form.$refs.password2.valueState = 'Error'
        this.$refs.profile_form.$refs.password1.valueStateText = 'Введенные пароли не совпадают'
        this.$refs.profile_form.$refs.password2.valueStateText = 'Введенные пароли не совпадают'
        return false
      } else {
        this.$refs.profile_form.$refs.password1.valueState = 'None'
        this.$refs.profile_form.$refs.password2.valueState = 'None'
      }
      let password = this.$refs.profile_form.$refs.password1.passwordStr
      this.$refs.profile_form.$refs.passwordPopover.close()
      this.$refs.baseComponent.useLoader()
      await fetch(this.$store.state.backendUrl+'/api/v1/auth/change_password/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
        body: JSON.stringify({
          'password': password,
        })
      })
          .then(response => {
            if (response.status === 200) {
              return response.json()
            } else {
              showMessage('error', 'Произошла ошибка, повторите попытку позже')
              this.$refs.baseComponent.useLoader()
            }
          })
          .then(data => {
            if (data['error']) {
              showMessage('error', data['error'])
            } else {
              showMessage('success', data['success'])
            }
            this.$refs.baseComponent.useLoader()
          })
    },
    onLoad() {
      this.$refs.baseComponent.useLoader()
      this.getProfileData()
    }
  },
  mounted() {
    this.onLoad()
  },
}
</script>

<style scoped>



ui5-dialog::part(header),
ui5-dialog::part(footer) {
  padding-inline: 0;
}

.card-div {
  width: 70%;
  height: 99%;
  overflow: auto;
  margin: 0 auto;
}

ui5-card {
  width: 99%;
}
</style>