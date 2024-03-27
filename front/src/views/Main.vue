<template>
  <LkBase ref="baseComponent">
    <slot>
      <div class="main-grid-container">
        <ui5-card class="main-grid-card">
          <ui5-card-header slot="header"
                           :title-text="profileData.surname+' '+profileData.name+' '+profileData.patronymic"
                           :subtitle-text="profileData.position">
            <img alt="Аватар" class="shellbar-logo" src="/media/imgs/Avatar.jpg" slot="avatar">
            undefined
          </ui5-card-header>
          <div class="content content-padding">
            <ui5-title level="H5" style="padding-block-end: 1rem;">Подробная информация</ui5-title>
            <div class="content-group">
              <ui5-label>Дата рождения</ui5-label>
              <ui5-title level="H6">{{ profileData.birthday }}</ui5-title>
            </div>
            <div class="content-group">
              <ui5-label>Номер телефона</ui5-label>
              <ui5-title level="H6">{{ profileData.phone }}</ui5-title>
            </div>
            <div class="content-group">
              <ui5-label>Email</ui5-label>
              <ui5-title level="H6">{{ profileData.email }}</ui5-title>
            </div>
          </div>
          <div class="card-center-button-div">
            <ui5-button class="card-center-button" icon="business-card"
                        @click="this.$router.push('/profile')">Перейти в профиль</ui5-button>
          </div>
        </ui5-card>
        <ui5-card v-if="!(isAdmin)" class="main-grid-card">
          <ui5-card-header slot="header"
                           title-text="Последние заявки">
          </ui5-card-header>
          <ui5-list id="apps-main-card-list" separators="None">
            <ui5-li id="apps-main-card-li" v-for="app in appsList"
                    :description="'Дата обновления: '+getDateUpdate(app.date_update)"
                    :additional-text="'Статус: '+app.app_status"
                    :additional-text-state="additionalTextState(app.app_status)"
                    @click="e => $router.push('/apps/app_detail/'+app.event_id+'/')">
              Мероприятие: {{app.event_name}}
            </ui5-li>
          </ui5-list>
        </ui5-card>
        <ui5-card v-if="isAdmin">
          <ui5-card-header slot="header"
                           title-text="Заявки опубликованных мероприятий">
          </ui5-card-header>
          <ui5-list id="apps-main-card-list" style="padding-top: 15px;">
            <ui5-li v-for="event in appsCountForEvents" id="apps-main-card-li"
                    :description="'Сроки проведения: '+event.event_date_range"
                    :additional-text="'Заявок: '+event.apps_count"
                    @click="e => $router.push('/admin_apps/?' +
                     'event_name='+event.event_name+'&event_date_range='+event.event_date_range)">
              {{event.event_name}}
            </ui5-li>
          </ui5-list>
        </ui5-card>
      </div>
    </slot>
  </LkBase>
</template>

<script>
import LkBase from '../components/LkBase.vue'
import {apiRequest} from "../additional/functions/api_request.js";
import store from "../modules/store/index.js";
import {showMessage} from "../additional/functions/message-strips.js";

export default {
  name: 'Main',
  components: {
    LkBase,
  },
  data() {
    return {
      isAdmin: false,
      profileData: {},
      systemsData: {},
      rolesData: {},
      appsList: [],
      appsCountForEvents: [],
      systemLoads: true,
      rolesLoads: true,
    }
  },
  methods: {
    useLoader() {
      this.$refs.baseComponent.useLoader()
      setTimeout(() =>
              this.$refs.baseComponent.useLoader(),
          5000
      )
    },
    async checkAdmin() {
      apiRequest(
          '/api/v1/auth/check_admin/',
          'GET',
          true,
          null,
          false,
          true
      )
          .then(resp => {
            this.isAdmin = resp.status === 200;
            if (!(this.isAdmin)) {
              this.getUserApps()
            } else {
              this.getAppsCountForEvents()
            }
          })
    },
    getDateUpdate(date_update) {
      if (date_update !== null) {return date_update}
      else {return '-'}
    },
    additionalTextState(status) {
      let state = 'None'
      switch (status) {
        case 'Черновик':
        case 'Сохранена':
        case 'Отозвана':
          break

        case 'Отправлена':
          state = 'Warning'
          break

        case 'Принята':
          state = 'Success'
          break

        case 'Отклонена':
          state = 'Error'
          break

        default:
          break
      }
      return state
    },
    async getProfileData() {
      apiRequest(
          '/api/v1/auth/profile/',
          'GET',
          true,
          null,
          false,
          false,
          false
      )
          .then(data => {
            if (data.error) {
              showMessage('error', data.error, false)
            } else {
              this.profileData = data
              this.$refs.baseComponent.useLoader()
            }
          })
    },
    async getUserApps() {
      apiRequest(
          '/api/v1/users/apps/list/?size=3&start=0',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            if (data.results) {
              this.appsList = data.results
            }
          })
    },
    async getAppsCountForEvents() {
      apiRequest(
          '/api/v1/admins/main/apps_count/',
          'GET',
          true,
          null,
          false,
          false
      )
          .then(data => {
            if (data.success) {
              this.appsCountForEvents = data.success
            }
          })
    },
    onLoad() {
      this.checkAdmin()
      this.$refs.baseComponent.useLoader()
      this.getProfileData()
    }
  },
  mounted() {
    this.onLoad()
  }
}
</script>

<style>
.main-grid-container {
  display: grid;
  width: 99%;
}
ui5-panel {
  white-space: normal;
  word-break: break-word;
}
ui5-list {
  white-space: normal;
  word-break: break-word;
}
ui5-li {
  word-break: break-word;
  white-space: normal;
}
ui5-list {
  --sapList_Active_Background: #00455d;
}
ui5-button {
  --sapButton_Emphasized_Background: #00455d;
  --sapButton_Background: #00455d;
  --sapButton_Emphasized_BorderColor: #00455d;
  --sapButton_Emphasized_TextColor: #ffffff;
  --sapButton_Emphasized_Hover_Background: #ffffff;
  --sapButton_Emphasized_Hover_TextColor: #00455d;
  --sapButton_Emphasized_Hover_BorderColor: #00455d;
  --sapButton_Emphasized_Active_Background: #00455d;
  --sapButton_Emphasized_Active_BorderColor: #00455d;
  --sapButton_BorderColor: #00455d;
  --sapButton_TextColor: #ffffff;
  --sapButton_Hover_Background: #ffffff;
  --sapButton_Hover_BorderColor: #00455d;
  --sapButton_Hover_TextColor: #00455d;
  --sapButton_Active_Background: #00455d;
  --sapButton_Active_BorderColor: #00455d;
  --sapButton_Lite_TextColor: #cb5b11;
}
.ui5-calheader-midcontainer .ui5-calheader-middlebtn{
  color: orange;
}
ui5-busy-indicator {
  --_ui5-v1-17-0_busy_indicator_color: #00455d;
}
ui5-popover {
  --_ui5-v1-20-0_token_text_color: #cb5b11;
  --sapContent_IconColor: #cb5b11;
  --sapContent_NonInteractiveIconColor: #cb5b11;
}
ui5-date-picker {
  --sapButton_Lite_TextColor: #cb5b11;
}
.card-center-button-div {
  display: flex;
  width: 100%;
  margin: 0 auto;
  justify-content: center;
  padding-bottom: 15px;
  padding-top: 15px;
}
.card-center-button {
  margin: 0 auto;
}
.content,
.content-group {
  display: flex;
  flex-direction: column;
  padding-block-end: 1rem;
}
.content-padding {
  padding: 0.5rem 1rem 0 1rem;
  box-sizing: border-box;
}
</style>