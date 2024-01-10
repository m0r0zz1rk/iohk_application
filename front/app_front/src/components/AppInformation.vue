<template>
  <ui5-toolbar v-if="lkUser">
    <ui5-toolbar-button v-if="['REVOKED', 'DRAFT', 'CREATED', 'REJECTED'].includes(appInfo.status)"
                        icon="save"
                        text="Сохранить"
                        @click="e => appSave()" />
    <ui5-toolbar-button v-if="appInfo.status === 'CREATED'"
                        icon="paper-plane"
                        text="Отправить"
                        @click="e => appChangeStatus('SHIPPED')" />
    <ui5-toolbar-button v-if="appInfo.status === 'SHIPPED'"
                        icon="undo"
                        text="Отозвать"
                        @click="e => appChangeStatus('REVOKED')" />
  </ui5-toolbar>
  <ui5-toolbar v-if="!(lkUser)">
    <ui5-toolbar-button icon="save" text="Сохранить" @click="e => appSave()" />
    <ui5-toolbar-button icon="paper-plane" text="Отправить" />
    <ui5-toolbar-button icon="undo" text="Отозвать" />
    <ui5-toolbar-button icon="delete" text="Удалить" />
  </ui5-toolbar>
  <ui5-tabcontainer fixed
                    collapsed
                    @tab-select="e => changeTab(e.detail.tab._state.text)">
    <ui5-tab text="Основная информация" :selected="selectedTab === 'main'" />
    <template v-if="(appRequired.user_app) && (appRequired.part_app)">
      <ui5-tab text="Заявка пользователя" :selected="selectedTab === 'user_app'" />
      <ui5-tab text="Заявки участников от пользователя" :selected="selectedTab === 'part_app'" />
    </template>
    <ui5-tab v-if="(appRequired.user_app) && (!(appRequired.part_app))"
             text="Заявка пользователя"
             :selected="selectedTab === 'user_app'" />
    <ui5-tab v-if="(!(appRequired.user_app)) && (appRequired.part_app)"
             text="Заявки участников от пользователя"
             :selected="selectedTab === 'part_app'" />
  </ui5-tabcontainer><br/><br/>
  <div class="info-app-container">
    <div class="info-app-div" v-bind:class="{'show-div': infoDiv, 'hide-div': !(infoDiv)}">
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
    <div class="info-app-div user-app-div" v-bind:class="{'show-div': userAppDiv, 'hide-div': !(userAppDiv)}">
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
                         :value="field.value"
                         :readonly="!(canChange)"
                         @change="e => fieldValueSave(field.object_id, e.target.value)" />
            </div>
            <ui5-date-picker v-if="field.type === 'date'"
                             formatPattern="dd.MM.YYYY"
                             :ref="'app_user_'+field.object_id"
                             :value="field.value"
                             :readonly="!(canChange)"
                             @change="e => fieldValueSave(field.object_id, e.target.value)" />
            <ui5-daterange-picker v-if="field.type === 'date_range'"
                                  formatPattern="dd.MM.YYYY"
                                  :ref="'app_user_'+field.object_id"
                                  :value = "field.value"
                                  :readonly="!(canChange)"
                                  @change="e => fieldValueSave(field.object_id, e.target.value)" />
            <ui5-select v-if="field.type === 'select'"
                        :ref="'app_user_'+field.object_id"
                        :disabled="!(canChange)"
                        @change="e => fieldValueSave(field.object_id, e.target._state._text)">
              <ui5-option selected></ui5-option>
              <ui5-option v-for="option in field.options" :selected="field.value === option">{{option}}</ui5-option>
            </ui5-select>
            <ui5-multi-combobox v-if="field.type === 'multiple'"
                                :ref="'app_user_'+field.object_id"
                                :readonly="!(canChange)">
                <ui5-mcb-item v-for="option in field.options"
                              :text="option"
                              :selected="field.value.split(',').includes(option)"/>
            </ui5-multi-combobox>
            <PhoneField v-if="field.type === 'phone'"
                        v-bind:phone-value="field.value"
                        v-bind:appChangePhoneAction="fieldValueSave"
                        v-bind:fieldObjectID="field.object_id"
                        v-bind:readOnly="!(canChange)"
                        :ref="'app_user_'+field.object_id"
            />
          </td>
        </tr>
      </table>
    </div>
    <div class="info-app-div" v-bind:class="{'show-div': participantAppDiv, 'hide-div': !(participantAppDiv)}">
      <PartAppsTable v-if="partAppFields.length > 0"
                     v-bind:canChange="canChange"
                     v-bind:eventId="eventId"
                     v-bind:recsURL="partAppRecsURL"
                     v-bind:recAddURL="'/api/v1/users/app_form_fields/part_app_save/'+this.eventId+'/'"
                     v-bind:recEditURL="'/api/v1/users/app_form_fields/part_app_edit/'+this.eventId+'/'"
                     v-bind:recDeleteURL="'/api/v1/users/app_form_fields/part_app_delete/'"
                     v-bind:addButton="true"
                     v-bind:dataTableHeight="56"
                     v-bind:partAppFields="partAppFields"  />
    </div>
  </div>
</template>

<script>

import {apiRequest} from "../additional/functions/api_request.js";
import AppStatus from "./badges/AppStatus.vue";
import InputFormFieldTypes from "../additional/consts/html_app_form_field_types.js"
import PhoneField from "./PhoneField.vue";
import app from "../App.vue";
import PartAppsTable from "./tables/PartAppsTable.vue";

export default {
  name: 'AppInformation',
  components: {PartAppsTable, PhoneField, AppStatus, InputFormFieldTypes},
  props: {
    eventId: {type: String},
    lkUser: {type: Boolean},
    loaderFunc: {type: Function}
  },
  data() {
    return {
      canChange: false,
      InputTypes: InputFormFieldTypes,
      selectedTab: 'main',
      profileData: {},
      appRequired: {},
      appInfo: {
        date_create: null,
        date_update: null,
        event: '',
        status: '',
        message: ''
      },
      userAppFields: [],
      partAppRecsURL: '/api/v1/users/app_form_fields/part_recs/'+this.eventId+'/',
      partAppFields: [],
      infoDiv: true,
      userAppDiv: false,
      participantAppDiv: false
    }
  },
  methods: {
    changeTab(tab) {
      this.infoDiv = false
      this.userAppDiv = false
      this.participantAppDiv = false
      switch (tab) {
        case 'Основная информация':
          this.selectedTab = 'main'
          this.getAppInfo()
          this.infoDiv = true
          break

        case 'Заявка пользователя':
          this.selectedTab = 'user_app'
          this.getUserAppFields()
          this.userAppDiv = true
          break

        default:
          this.selectedTab = 'part_app'
          this.participantAppDiv = true
      }
    },
    async getAppInfo() {
      this.canChange = false
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
            if (['DRAFT', 'CREATED', 'REJECTED', 'REVOKED'].includes(this.appInfo.status)) {
              this.canChange = true
            }
          })
    },
    async getAppRequiredInfo() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/event_app_required/'+this.eventId+'/',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            this.appRequired = data
            if (data.user_app) {
              this.getUserAppFields()
            }
            if (data.part_app) {
              this.getPartAppFields()
            }
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
          this.$store.state.backendUrl+'/api/v1/users/apps/user_app_fields/'+this.eventId+'/',
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
    async getPartAppFields() {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/app_form_fields/part/'+this.eventId+'/',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            this.partAppFields = data['success']
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
    },
    async fieldValueSave(field_id, value) {
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/app_form_fields/save/',
          'POST',
          true,
          {
            field_id: field_id,
            value: value
          },
          false,
          false
      )
          .then(data => {})
    },
    async appSave() {
      let data = []
      let value = null
      let value_empty = false
      this.userAppFields.map((field) => {
        if ((field.type.includes('profile_')) ||
            (['text', 'number', 'email', 'date', 'date_range'].includes(field.type))) {
          value = this.$refs['app_user_'+field.object_id][0].value
        } else if (field.type === 'select') {
          value = this.$refs['app_user_'+field.object_id][0]._state._text
        } else if (field.type === 'phone') {
          value = this.$refs['app_user_'+field.object_id][0].componentPhoneField
        } else if (field.type === 'multiple') {
          value = ''
          if (this.$refs['app_user_'+field.object_id][0].selectedValues.length > 0) {
            this.$refs['app_user_'+field.object_id][0].selectedValues.map((val) => {
              value += val._state.text+','
            })
            value = value.slice(0, -1)
          }
        }
        if (value.length === 0) {
          showMessage('error', 'Заполните все поля заявки пользователя')
          value_empty = true
          return false
        }
        if (!(['text', 'number', 'email', 'date', 'date_range', 'select', 'phone'].includes(field.type))) {
          data.push({
            field_id: field.object_id,
            value: value
          })
        }
      })
      if (value_empty) { return false }
      this.loaderFunc()
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/apps/save/',
          'POST',
          true,
          {
            event_id: this.eventId,
            fields: data
          },
          false,
          true
      )
          .then(resp => {
            if (resp.status !== 200) {
              showMessage('error', 'Произошла ошибка, повторите попытку позже')
            } else {
              showMessage('success', 'Заявка успешно сохранена')
              this.getAppInfo()
            }
            this.loaderFunc()
          })
    },
    async appChangeStatus(new_status) {
      this.loaderFunc()
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/users/apps/status_change/',
          'POST',
          true,
          {
            event_id: this.eventId,
            status: new_status
          },
          false,
          true
      )
          .then(resp => {
            if (resp.status !== 200) {
              showMessage('error', 'Произошла ошибка, повторите попытку позже')
            } else {
              showMessage('success', 'Статус заявки успешно изменен')
              this.getAppInfo()
            }
            this.loaderFunc()
          })
    }
  },
  mounted() {
    this.getAppInfo()
    this.getAppRequiredInfo()
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
    height: 65vh;
    overflow: auto;
    margin: 0 auto;
  }
  .user-app-div {
    width: 80%;
  }
  .show-div {
    position: relative;
  }
  .hide-div {
    position: absolute;
    top: -9999px;
    left: -9999px;
  }
</style>