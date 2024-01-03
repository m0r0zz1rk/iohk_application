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
          <td style="text-align: center;">
            <b v-if="appInfo.date_update !== null">{{appInfo.date_update}}</b>
            <b v-if="appInfo.date_update === null">-</b>
          </td>
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
          <td style="text-align: center;">
            <b v-if="appInfo.message.length > 0">{{appInfo.message}}</b>
            <b v-if="appInfo.message.length === 0">-</b>
          </td>
        </tr>
      </table>
    </div>
    <div v-if="selectedTab === 1" class="info-app-div">
      <table v-if="userAppFields.length > 0" style="margin: 0 auto; font-size: 16px">
        <tr v-for="field in userAppFields">
          <td style="text-align: right; width: 25%; padding-right: 30px"><ui5-label show-colon>{{ field.name }}</ui5-label></td>
          <td style="text-align: center;">
            <div v-if="InputTypes.includes(field.type)">
              <ui5-input v-if="field.type.includes('profile_')"
                         :ref="'app_user_'+field.object_id"
                         :value="getProfileInfoByField(field.type)"
                         readonly />
              <ui5-input v-if="!(field.type.includes('profile_'))"
                         :ref="'app_user_'+field.object_id"
                         :type="field.type.charAt(0).toUpperCase()+field.type.slice(1)"
                         :value="field.value" />
            </div>
            <ui5-date-picker v-if="field.type === 'date'"
                             formatPattern="dd.MM.YYYY"
                             :ref="'app_user_'+field.object_id"
                             :value="field.value" />
            <ui5-daterange-picker v-if="field.type === 'date_range'"
                                  formatPattern="dd.MM.YYYY"
                                  :ref="'app_user_'+field.object_id"
                                  :value = "field.value" />
            <ui5-select v-if="field.type === 'select'" :ref="'app_user_'+field.object_id">
              <ui5-option v-for="option in field.options" :selected="field.value === option">{{option}}</ui5-option>
            </ui5-select>
            <ui5-multi-combobox v-if="field.type === 'multiple'" :ref="'app_user_'+field.object_id">
              <ui5-mcb-item v-for="option in field.options"
                            :text="option"
                            :selected="field.value.split(',').includes(option)" />
            </ui5-multi-combobox>
            <PhoneField v-if="field.type === 'phone'"
                        v-bind:phone-value="field.value"
                        :ref="'app_user_'+field.object_id"/>
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
import PhoneField from "./PhoneField.vue";

export default {
  name: 'AppInformation',
  components: {PhoneField, AppStatus, InputFormFieldTypes},
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
          })
    },
    getProfileInfoByField(field) {
      if (field !== 'profile_fio') {
        let arr = field.split('_')
        let prof_info = ''
        if (arr.length === 3) {
          prof_info = arr[1]+'_'+arr[2]
        } else {
          prof_info = arr[1]
        }
        if (Object.keys(this.profileData).includes(prof_info)) {
          return this.profileData[prof_info]
        }
      }
      let fio = ''
      if ((Object.keys(this.profileData).includes('surname')) &&
          (Object.keys(this.profileData).includes('name'))) {
          fio = this.profileData.surname+' '+this.profileData.name
      }
      if ((Object.keys(this.profileData).includes('patronymic'))) {
        fio += ' '+this.profileData.patronymic
      }
      return fio
    }
  },
  mounted() {
    this.getAppInfo()
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
  }
  .info-app-div {
    width: 80%;
    height: 65vh;
    overflow: auto;
    margin: 0 auto;
  }
</style>