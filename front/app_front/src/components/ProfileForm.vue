<template>
    <ui5-card>
      <ui5-card-header slot="header"
                       title-text="Профиль пользователя" />
      <div class="content content-padding">
        <form @submit.prevent="profileFormAction()">
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
            <ui5-label for="profile_age" show-colon>Возраст</ui5-label>
          </td>
          <td>
            <div id="profile_age" style="width: 100%; text-align: center"><b>{{profileData.age}}</b></div>
          </td>
        </tr>
        <tr>
          <td style="text-align: right">
            <ui5-label for="profile_email" required show-colon>Email</ui5-label>
          </td>
          <td>
            <ui5-input type="Email"
                       id="profile_email"
                       :value="profileData.email"
                       ref="profile_email" required/>
          </td>
        </tr>
        <tr>
          <td style="text-align: right">
            <ui5-label for="profile_phone" required show-colon>Телефон</ui5-label>
          </td>
          <td>
            <PhoneField ref="profile_phone"
                        v-bind:phoneValueState="loginPhoneValueState"
                        v-bind:phoneStateText="loginPhoneStateText" />
          </td>
        </tr>
        <tr>
          <td style="text-align: right">
            <ui5-label for="profile_role" required show-colon>Роль пользователя</ui5-label>
          </td>
          <td v-if="!(isAdmin)">
            <div v-if="profileData.role === 'Администраторы'" style="width: 100%; text-align: center">
              <b>Администраторы</b>
            </div>
            <ui5-select v-if="profileData.role !== 'Администраторы'" id="profile_role"
                        ref="profile_role"
                        @change="e => this.selectedRole = this.$refs.profile_role.selectedOption.innerText">
              <ui5-option :selected="profileData.role === 'Преподаватели'">Преподаватели</ui5-option>
              <ui5-option :selected="profileData.role === 'Участники'">Участники</ui5-option>
            </ui5-select>
          </td>
          <td v-if="isAdmin">
            <ui5-select id="profile_role"
                        ref="profile_role"
                        @change="e => this.selectedRole = this.$refs.profile_role.selectedOption.innerText">
              <ui5-option :selected="profileData.role === 'Администраторы'">Администраторы</ui5-option>
              <ui5-option :selected="profileData.role === 'Преподаватели'">Преподаватели</ui5-option>
              <ui5-option :selected="profileData.role === 'Участники'">Участники</ui5-option>
            </ui5-select>
          </td>
        </tr>
        <tr v-if="(!(isAdmin) && this.selectedRole === 'Преподаватели')">
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
        <tr v-if="isAdmin">
          <td style="text-align: right">
            <ui5-label for="profile_oo_fullname" show-colon>Полное наименование ОО</ui5-label>
          </td>
          <td>
            <ui5-textarea id="profile_oo_fullname"
                          ref="profile_oo_fullname"
                          :value="profileData.oo_fullname"
                          rows="10" />
          </td>
        </tr>
        <tr v-if="(!(isAdmin) && this.selectedRole === 'Преподаватели')">
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
        <tr v-if="isAdmin">
          <td style="text-align: right">
            <ui5-label for="profile_oo_shortname" show-colon>Краткое наименование ОО</ui5-label>
          </td>
          <td>
            <ui5-textarea id="profile_oo_shortname"
                          ref="profile_oo_shortname"
                          :value="profileData.oo_shortname"
                          rows="10" />
          </td>
        </tr>
      </table>
      <div class="card-center-button-div">
        <div style="margin: 0 auto; display: flex;">
          <div style="display: inline-block;">
            <ui5-button type="Submit" icon="save">Сохранить изменения</ui5-button>&nbsp;
          </div>
          <div style="display: inline-block;">
            <ui5-button type="Button" icon="shield"
                        @click="e => $refs.passwordPopover.showAt(e.target)">Изменить пароль</ui5-button>
            <ui5-popover ref="passwordPopover"
                         header-text="Смена пароля"
                         placement-type="Top">
              <form @submit.prevent="passwordFormAction()">
                <ui5-label for="password1" required show-colon>Новый пароль</ui5-label>
                <PasswordField ref="password1"/><br />
                <ui5-label for="password2" required show-colon>Подтверждение</ui5-label>
                <PasswordField ref="password2"/><br />
                <div slot="footer" class="popover-footer">
                  <div style="flex: 1;"></div>
                  <ui5-button type="Submit"
                              design="Emphasized">
                    Изменить
                  </ui5-button>
                </div>
              </form>
            </ui5-popover>
          </div>
        </div>
      </div>
    </form>
      </div>
    </ui5-card>
</template>

<script>

import PhoneField from "./PhoneField.vue";
import PasswordField from "./PasswordField.vue";
import {apiRequest} from "../additional/functions/api_request.js";

export default {
  name: 'ProfileForm',
  components: {PasswordField, PhoneField},
  data() {
    return {
      states: [],
      selectedRole: ''
    }
  },
  props: {
    profileData: {type: Object},
    profileFormAction: {type: Function},
    passwordFormAction: {type: Function},
    isAdmin: {type: Boolean}
  },
  methods: {
    async getStates() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/auth/states/',
          'GET',
          false,
          null,
          false,
          false
      )
          .then(data => {
            this.states = data.states
          })
    },
  },
  watch: {
    profileData() {
      this.$refs.profile_phone.componentPhoneField = this.profileData.phone
      this.selectedRole = this.profileData.role
    }
  },
  mounted() {
    this.getStates()
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
.popover-footer {
  display: flex;
  justify-content: flex-end;
  width: 100%;
  align-items: center;
  padding: 0.5rem 0;
}
</style>