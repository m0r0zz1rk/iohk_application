<template>
  <ui5-shellbar primary-title="Система подачи заявок" secondary-title="ИОХК"
                @profile-click="$refs.profileMenu.showAt($event.detail.targetRef)"
                @logo-click="goToIOHKSite()">
    <ui5-button icon="menu" slot="startButton" @click="showHideMenu"></ui5-button>
    <img slot="logo" alt="Логотип" src="/media/favicon.ico">
    <ui5-avatar slot="profile" ref="avatarButton" color-scheme="Accent1" icon="customer"></ui5-avatar>
  </ui5-shellbar>
  <ui5-popover placement-type="Bottom" ref="profileMenu" >
    <div class="action-popover-header">
      <ui5-title style="padding: 0.25rem 1rem 0rem 1rem; font-size: 16px;">Действия</ui5-title>
    </div>
    <div class="action-popover-content" style="margin-top: 1rem;">
      <ui5-list separators="None">
        <ui5-li icon="account" @click="goToProfile()"><p style="font-size: 14px;">Профиль</p></ui5-li>
        <ui5-li icon="log" @click="logout()"><p style="font-size: 14px;">Выход</p></ui5-li>
      </ui5-list>
    </div>
  </ui5-popover>
  <SideNavigation v-bind:sideNavCollapsed="sideNavCollapsed" />
  <div class="base-div"></div>
  <div v-show="contentShow" class="content-div">
    <slot></slot>
  </div>
  <LkLoader ref="lkLoader" />
  <PreLoader ref="preLoader" />
</template>

<script>
import LkLoader from '../components/LkLoader.vue'
import PreLoader from '../App.vue'
import store from "../modules/store/index.js";
import SideNavigation from "./SideNavigation.vue";
export default {
  name: 'Base',
  components: {
    SideNavigation,
    LkLoader,
    PreLoader
  },
  data() {
    return {
      contentShow: true,
      sideNavCollapsed: true,
      isAdmin: false
    }
  },
  methods: {
    closeLoginPreloader() {
      this.$refs.preLoader.usePreloader(true)
    },
    showHideMenu() {
      this.sideNavCollapsed=!(this.sideNavCollapsed)
      setTimeout(this.changeBackgroundColor, 25)
    },
    changeBackgroundColor() {
      if (this.sideNavCollapsed) {
        return false
      }
      setTimeout(function() {
        let subItems = document.querySelector('#side_nav').shadowRoot.querySelector('.ui5-sn-root').querySelectorAll('[level="2"]')
        for (let i=0;i<subItems.length;i++) {
          subItems[i].shadowRoot.querySelector('[part="native-li"]').style['background'] = '#00455d'
          subItems[i].shadowRoot.querySelector('[part="title"]').style['color'] = 'white'
          subItems[i].shadowRoot.querySelector('[part="icon"]').shadowRoot.querySelector('[part="root"]').style['color'] = 'white'
        }
      }, 0)
    },
    useLoader() {
      this.contentShow = !(this.contentShow)
      this.$refs.lkLoader.useLoader()
    },
    goToProfile() {
      this.$router.push('/profile')
    },
    logout: function () {
      this.$store.dispatch('AUTH_LOGOUT')
          .then(() => {
            this.$router.push('/')
          })
    },
    async checkAdmin() {
      await fetch(store.state.backendUrl+'/api/v1/auth/check_admin/', {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+store.state.iohk_token
        },
      })
          .then(resp => {
            this.isAdmin = resp.status === 200;
          })
    },
    goToIOHKSite() {
      window.open('https://iohk.ru', '_blank')
    }
  },
  mounted() {
    this.checkAdmin()
    this.$nextTick(function () {
      this.closeLoginPreloader()
    })
  }
}

</script>

<style scoped>
a {
  text-decoration: none;
}
.base-div {
  position: absolute;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-image: url('/media/imgs/lk-back.jpg');
  background-repeat: repeat;
  opacity: 0.2;
}
ui5-shellbar {
  position: absolute;
  border-bottom: 1px solid #dadada;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 12;
  --sapShellColor: #ffffff;
  --sapShell_TextColor: #00455d;
  --sapShell_Hover_Background: #f9f8f5;
//--sapAccentColor1: #00455d;
  --sapContent_IconColor: #00455d;

}
ui5-side-navigation[collapsed] {
  z-index: 11;
  width: 3.25em;
}
ui5-side-navigation {
  position: absolute;
  top: 45px;
  left: 0;
  height: 100%;
  z-index: 11;
  width: 425px;
  text-align: center;
}

ui5-shellbar::part(root) {
  padding-inline-start: 0.5rem;
  padding-inline-end: 0.5rem;
}
.content-div {
  position: absolute;
  top: 80px;
  left: 100px;
  color: black;
  width: calc(97vw - 60px);
  height: calc(97vh - 80px);
  border: none;
  z-index: 10;
  overflow: hidden;
}

</style>