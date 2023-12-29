<template>
  <LkBase ref="baseComponent">
    <slot>
        <ui5-card class="half_width_and_center">
          <ui5-card-header slot="header"
                           :title-text="profileData.surname+' '+profileData.name+' '+profileData.patronymic"
                           :subtitle-text="profileData.position">
            <img alt="Аватар" src="/media/imgs/Avatar.jpg" slot="avatar">
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
    </slot>
  </LkBase>
</template>

<script>
import LkBase from '../components/LkBase.vue'
import {apiRequest} from "../additional/functions/api_request.js";

export default {
  name: 'Main',
  components: {
    LkBase,
  },
  data() {
    return {
      profileData: {},
      systemsData: {},
      rolesData: {},
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
    async getProfileData() {
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
              this.$refs.baseComponent.useLoader()
            }
          })
    },
    onLoad() {
      this.$refs.baseComponent.useLoader()
      this.getProfileData()
    }
  },
  mounted() {
    this.onLoad()
  }
}
</script>

<style scoped>

ui5-card::slotted(.ui5-card-root) {
  overflow: auto;
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
}
ui5-popover {
  width: 20vw;
}
ui5-busy-indicator {
  --_ui5-v1-17-0_busy_indicator_color: #00455d;
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