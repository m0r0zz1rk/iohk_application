<template>
  <LkBase ref="baseComponent">
    <slot>
      <div class="card-div">
        <form @submit.prevent="checkUniqueData()">
          <ui5-card>
            <ui5-card-header slot="header"
                             title-text="Профиль пользователя" />
            <div class="content content-padding">
              <table style="border: 0; width: 50vw; margin: 0 auto;">
                <tr>
                  <td style="text-align: right; width: 15%;">
                    <ui5-label for="profile_state" required show-colon>Госудаство</ui5-label>
                  </td>
                  <td>
                    <ui5-select id="profile_state" ref="profile_state" required>
                      <ui5-option v-for="state in states"
                                  :selected="state.name === profileData.state">
                        {{state.name}}
                      </ui5-option>
                    </ui5-select>
                  </td>
                </tr>
                <tr>
                  <td style="text-align: right">
                    <ui5-label for="profile_surname" required show-colon>Фамилия</ui5-label>
                  </td>
                  <td>
                    <ui5-input type="Text" ref="profile_surname" :value="profileData.surname" required />
                  </td>
                </tr>
                <tr>
                  <td style="text-align: right">
                    <ui5-label for="profile_name" required show-colon>Имя</ui5-label>
                  </td>
                  <td>
                    <ui5-input type="Text" ref="profile_name" :value="profileData.name" required />
                  </td>
                </tr>
                <tr>
                  <td style="text-align: right">
                    <ui5-label for="profile_patronymic" show-colon>Отчество</ui5-label>
                  </td>
                  <td>
                    <ui5-input type="Text"
                               id="profile_patronymic"
                               ref="profile_patronymic"
                               :value="profileData.patronymic" />
                  </td>
                </tr>
                <tr>
                  <td style="text-align: right">
                    <ui5-label for="profile_sex" required show-colon>Пол</ui5-label>
                  </td>
                  <td>
                    <ui5-switch id="profile_sex"
                                ref="profile_sex"
                                :checked="profileData.sex"
                                text-on="М"
                                text-off="Ж" />
                  </td>
                </tr>
                <tr>
                  <td style="text-align: right">
                    <ui5-label for="profile_birthday" required show-colon>Дата рождения</ui5-label>
                  </td>
                  <td>
                    <ui5-date-picker id="profile_birthday"
                                     ref="profile_birthday"
                                     :value="profileData.birthday"
                                     format-pattern="dd.MM.yyyy" required />
                  </td>
                </tr>
                <tr>
                  <td style="text-align: right">
                    <ui5-label for="profile_email" required show-colon>Email</ui5-label>
                  </td>
                  <td>
                    <ui5-input type="Email"
                               id="profile_email"
                               v-model="profileEmailField"
                               ref="profile_email" required/>
                  </td>
                </tr>
                <tr>
                  <td style="text-align: right">
                    <ui5-label for="profile_phone" required show-colon>Телефон</ui5-label>
                  </td>
                  <td>
                    <ui5-input type="Text" id="profile_phone" ref="profile_phone"
                               v-model="profilePhoneField"
                               @input = "e => checkPhoneLength()" required/>
                    <input v-model="profilePhoneField" v-mask="'+7 (###) ###-##-##'" hidden>
                  </td>
                </tr>
                <tr>
                  <td style="text-align: right">
                    <ui5-label for="profile_role" required show-colon>Роль пользователя</ui5-label>
                  </td>
                  <td>
                    <div v-if="profileData.role === 'Администраторы'" style="width: 100%; text-align: center">
                      <b>Администраторы</b>
                    </div>
                    <ui5-select v-if="profileData.role !== 'Администраторы'" id="profile_role"
                                ref="profile_role"
                                @change="this.selectedRole = this.$refs.profile_role.selectedOption.innerText">
                      <ui5-option :selected="profileData.role === 'Преподаватели'">Преподаватели</ui5-option>
                      <ui5-option :selected="profileData.role === 'Участники'">Участники</ui5-option>
                    </ui5-select>
                  </td>
                </tr>
                <tr v-if="this.selectedRole === 'Преподаватели'">
                  <td style="text-align: right">
                    <ui5-label for="profile_oo_fullname" required show-colon>Полное наименование ОО</ui5-label>
                  </td>
                  <td>
                    <ui5-textarea id="profile_oo_fullname"
                                  ref="profile_oo_fullname"
                                  :value="profileData.oo_fullname"
                                  rows="10" required />
                  </td>
                </tr>
                <tr v-if="this.selectedRole === 'Преподаватели'">
                  <td style="text-align: right">
                    <ui5-label for="profile_oo_shortname" required show-colon>Краткое наименование ОО</ui5-label>
                  </td>
                  <td>
                    <ui5-textarea id="profile_oo_shortname"
                                  ref="profile_oo_shortname"
                                  :value="profileData.oo_shortname"
                                  rows="10" required />
                  </td>
                </tr>
              </table>
            </div><br/>
            <div class="card-center-button-div">
              <div style="margin: 0 auto; display: flex;">
                <div style="display: inline-block;">
                  <ui5-button type="Submit" icon="save">Сохранить изменения</ui5-button>&nbsp;
                </div>
                <div style="display: inline-block;">
                  <ui5-button type="Button" icon="shield" @click="$refs.passwordChangeDialog.show()">Изменить пароль</ui5-button>
                </div>
              </div>
            </div>
          </ui5-card>
        </form>
      </div>
    </slot>
  </LkBase>
  <form @submit.prevent="changePassword()">
    <ui5-dialog ref="passwordChangeDialog" id="password-dialog">
      <ui5-bar slot="header" design="Header">
        <ui5-title level="H5" slot="startContent">Смена пароля</ui5-title>
        <ui5-button design="Emphasized"
                    slot="endContent"
                    icon="decline"
                    @click="$refs.passwordChangeDialog.close()"></ui5-button>
      </ui5-bar>
      <ui5-label for="profile_password1" required show-colon>Новый пароль</ui5-label>
      <PasswordField ref="profile_password1"/><br />
      <ui5-label for="profile_password2" required show-colon>Подтверждение</ui5-label>
      <PasswordField ref="profile_password2"/><br />
      <ui5-bar slot="footer" design="Footer">
        <ui5-button type="Submit" class="dialogCloser" slot="endContent" icon="save">Сохранить</ui5-button>
      </ui5-bar>
    </ui5-dialog>
  </form>
</template>

<script>

import LkBase from "../components/LkBase.vue";
import PasswordField from "../components/PasswordField.vue";
export default {
  components: {
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
              this.profilePhoneField = data.phone
              this.profileEmailField = data.email
              this.selectedRole = data.role
              if (this.afterLoad) {
                this.$refs.baseComponent.useLoader()
                this.afterLoad = false
              }
            }
          })
    },
    async getStates() {
      await fetch(this.$store.state.backendUrl+'/api/v1/auth/states/', {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'application/json;charset=UTF-8',
        },
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              showMessage('error', 'Произошла ошибка при получении списка государств, повторите попытку позже')
              return false
            }
          })
          .then(data => {
            this.states = data.states
          })
    },
    async checkUniqueData() {
      let date_birth = convertToJSDate(this.$refs.profile_birthday.value)
      let age = Math.floor((new Date() - new Date(date_birth).getTime()) / 3.15576e+10)
      let data = {
        'state': this.$refs.profile_state.selectedOption.innerText,
        'surname': this.$refs.profile_surname.value,
        'name': this.$refs.profile_name.value,
        'patronymic': this.$refs.profile_patronymic.value,
        'sex': this.$refs.profile_sex._state.checked,
        'birthday': this.$refs.profile_birthday.value,
        'age': age,
        'email': this.$refs.profile_email.value,
        'phone': this.profilePhoneField,

        'oo_fullname': '',
        'oo_shortname': ''
      }
      if (this.profileData.role === 'Администраторы') {
        data.role = 'Администраторы'
      } else {
        data.role = this.$refs.profile_role.selectedOption.innerText
      }
      if (data.role === 'Преподаватели') {
        data.oo_fullname = this.$refs.profile_oo_fullname.value
        data.oo_shortname = this.$refs.profile_oo_shortname.value
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
          'phone': this.profilePhoneField
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
                  'email': that.profileEmailField
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
      if (this.$refs.profile_password1.passwordStr.length < 8) {
        this.$refs.profile_password1.valueState = 'Error'
        this.$refs.profile_password1.valueStateText = 'Минимальная длина пароля - 8 символов'
        return false
      } else {
        this.$refs.profile_password1.valueState = 'None'
      }
      if (this.$refs.profile_password1.passwordStr !== this.$refs.profile_password2.passwordStr) {
        this.$refs.profile_password1.valueState = 'Error'
        this.$refs.profile_password2.valueState = 'Error'
        this.$refs.profile_password1.valueStateText = 'Введенные пароли не совпадают'
        this.$refs.profile_password2.valueStateText = 'Введенные пароли не совпадают'
        return false
      } else {
        this.$refs.profile_password1.valueState = 'None'
        this.$refs.profile_password2.valueState = 'None'
      }
      let password = this.$refs.profile_password1.passwordStr
      this.$refs.passwordChangeDialog.close()
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
              this.$refs.passwordChangeDialog.open()
            } else {
              showMessage('success', data['success'])
            }
            this.$refs.baseComponent.useLoader()
          })
    },
    checkPhoneLength() {
        if (this.profilePhoneField.length > 18) {
          this.profilePhoneField = this.profilePhoneField.substring(0, 17)
        }
    },
    onLoad() {
      this.$refs.baseComponent.useLoader()
      this.getStates()
      this.getProfileData()
    }
  },
  mounted() {
    this.onLoad()
  },
  watch: {
    phone() {
      this.checkPhoneLength()
    }
  }
}
</script>

<style scoped>

.card-center-button-div {
  display: flex;
  width: 100%;
  margin: 0 auto;
  justify-content: center;
  padding-bottom: 15px;
  padding-top: 15px;
}

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