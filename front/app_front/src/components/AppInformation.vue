<template>
  <ui5-toolbar>
    <ui5-toolbar-button icon="save" text="Сохранить" />
    <ui5-toolbar-button icon="paper-plane" text="Отправить" />
    <ui5-toolbar-button icon="undo" text="Отозвать" />
    <ui5-toolbar-button icon="delete" text="Удалить" />
  </ui5-toolbar>
  <ui5-tabcontainer fixed
                    collapsed
                    @tab-select="e => changeTab(e.detail.tabIndex)">
    <ui5-tab text="Основная информация" :selected="selectedTab === 0" />
    <ui5-tab text="Заявка пользователя" :selected="selectedTab === 1" />
    <ui5-tab text="Заявки участников от пользователя" :selected="selectedTab === 2" />
  </ui5-tabcontainer><br/><br/>
  <div class="info-app-container">
    <div v-if="selectedTab === 0" class="info-app-div">
      <table style="margin: 0 auto; font-size: 16px">
        <tr>
          <td style="text-align: right; width: 25%; padding-right: 30px"><ui5-label show-colon>Дата подачи заявки</ui5-label></td>
          <td style="text-align: center;"><b>{{appInfo.date_create}}</b></td>
        </tr>
        <tr>
          <td style="text-align: right; padding-right: 30px"><ui5-label show-colon>Дата последнего обновления заявки</ui5-label></td>
          <td style="text-align: center;"><b>{{appInfo.date_update}}</b></td>
        </tr>
        <tr>
          <td style="text-align: right; padding-right: 30px"><ui5-label show-colon>Мероприятие</ui5-label></td>
          <td style="text-align: center;"><b>{{appInfo.event}}</b></td>
        </tr>
        <tr>
          <td style="text-align: right; padding-right: 30px"><ui5-label show-colon>Статус заявки</ui5-label></td>
          <td style="text-align: center;">
            <AppStatus v-if="appInfo.status.length > 0" v-bind:status="appInfo.status" />
          </td>
        </tr>
        <tr>
          <td style="text-align: right; padding-right: 30px"><ui5-label show-colon>Сообщение по заявке</ui5-label></td>
          <td style="text-align: center;">{{appInfo.message}}</td>
        </tr>
      </table>
    </div>
    <div v-if="selectedTab === 1" class="info-app-div">
      <table v-if="userAppFields.length > 0" style="margin: 0 auto; font-size: 16px">
        <tr v-for="field in userAppFields">
          <td style="text-align: right; width: 25%; padding-right: 30px"><ui5-label show-colon>{{ field.name }}</ui5-label></td>
          <td style="text-align: center;">
            <div v-if="InputTypes.includes(field.type)">
              <ui5-input />
            </div>
          </td>
        </tr>
      </table>
    </div>
  </div>
</template>

<script>

import {apiRequest} from "../additional/functions/api_request.js";
import AppStatus from "./badges/AppStatus.vue";
import InputFormFieldTypes from "../additional/consts/html_app_form_field_types.js"

export default {
  name: 'AppInformation',
  components: {AppStatus, InputFormFieldTypes},
  props: {
    eventId: {type: String},
    lkUser: {type: Boolean}
  },
  data() {
    return {
      InputTypes: InputFormFieldTypes,
      selectedTab: 0,
      profileData: {},
      appInfo: {
        date_create: null,
        date_update: null,
        event: '',
        status: '',
        message: ''
      },
      userAppFields: []
    }
  },
  methods: {
    InputFormFieldTypes() {
      return InputFormFieldTypes
    },
    changeTab(index) {
      switch (index) {
        case 0:
          this.getAppInfo()
          break

        case 1:
          this.getUserAppFields()
          break

        default:
          console.log('LOL')
      }
      this.selectedTab = index
    },
    async getAppInfo() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/apps/app_info/'+this.eventId+'/',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            this.appInfo = data
          })
    },
    async getProfileInfo() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/auth/profile/',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            if (data.error) {
              showMessage('error', data.error, false)
            } else {
              this.profileData = data
              console.log(this.profileData)
            }
          })
    },
    async getUserAppFields() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/apps/app_user_fields/'+this.eventId+'/',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            this.userAppFields = data['success']
            console.log(this.userAppFields)
          })
    }
  },
  mounted() {
    this.getAppInfo()
    console.log(InputFormFieldTypes)
    if (this.lkUser) {
      this.getProfileInfo()
    }
  }
}

</script>

<style scoped>
  .info-app-container {
    position: relative;
    width: 100%;
    justify-content: center;
    align-content: center;
    overflow: auto;
  }
  .info-app-div {
    width: 80%;
    margin: 0 auto;
  }
</style>