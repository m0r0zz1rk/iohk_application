<template>
  <ui5-side-navigation id="side_nav" ref="sideNavigation" :collapsed="sideNavCollapsed">
    <ui5-side-navigation-item text="Главная" icon="home"
                              :selected="selectedMenu === 'main'"
                              @click="navigate('/main')" />
    <template v-for="item in items">
      <ui5-side-navigation-item v-if="item.only_admin === isAdmin"
                                :text="item.text"
                                :icon="item.icon"
                                :selected="selectedMenu === item.mainMenu"
                                @click="e => {
                                if (item.next) {
                                  navigate(item.next)
                                }
                              }">
        <ui5-side-navigation-sub-item v-for="subItem in item.subItems"
                                      :text="subItem.text"
                                      :icon="subItem.icon"
                                      @click="e => navigate(subItem.next)" />

      </ui5-side-navigation-item>
    </template>
  </ui5-side-navigation>
</template>

<script>

import store from "../modules/store/index.js";

export default {
  name: 'SideNavigation',
  data() {
    return {
      selectedMenu: '',
      isAdmin: false,
      items: [
        {
          text: 'Справочники',
          only_admin: true,
          icon: 'sap-box',
          mainMenu: 'guides',
          next: '/guides'
        },
        {
          text: 'Пользователи',
          only_admin: true,
          icon: 'company-view',
          mainMenu: 'users',
          next: '/users'
        },
        {
          text: 'Мероприятия',
          only_admin: true,
          icon: 'education',
          mainMenu: 'admin_events',
          subItems: [
            {
              text: 'Просмотр',
              icon: 'list',
              next: '/admin_events/view'
            },
            {
              text: 'Управление',
              icon: 'settings',
              next: '/admin_events/manage'
            },
          ]
        },
        {
          text: 'Заявки',
          only_admin: true,
          icon: 'request',
          mainMenu: 'apps',
          next: '/apps'
        },
        {
          text: 'Журнал',
          only_admin: true,
          icon: 'time-account',
          mainMenu: 'journal',
          next: '/journal'
        }
      ]
    }
  },
  props: {
    sideNavCollapsed: {type: Boolean},
  },
  methods: {
    navigate(name_component) {
      this.$router.push(name_component)
    },
    async checkAdmin() {
      fetch(store.state.backendUrl+'/api/v1/auth/check_admin/', {
        method: 'GET',
        headers: {
          'Authorization': 'Token '+store.state.iohk_token
        },
      })
          .then(resp => {
            this.isAdmin = resp.status === 200;
          })
    }
  },
  mounted() {
    this.selectedMenu = window.location.href.split('/')[3]
    this.checkAdmin()
  }
}

</script>

<style scoped>

</style>