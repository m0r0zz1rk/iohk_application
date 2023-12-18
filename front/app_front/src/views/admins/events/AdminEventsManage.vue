<template>
  <LkBase ref="baseComponent">
    <slot>
      <ui5-card class="full-card">
        <ui5-card-header slot="header"
                         title-text="Управление мероприятием">
        </ui5-card-header>
        <div style="width: 100%; text-align: center; justify-content: center">
          <div style="display: inline-block">
            <table>
              <tr>
                <td>Мероприятие:</td>
                <td>
                  <div v-if="selectedEvent === null">
                    <ui5-badge color-scheme="3">Не выбрано</ui5-badge>
                  </div>
                  <div v-if="selectedEvent !== null">
                    <b>{{selectedEvent.name}} ({{selectedEvent.date_range}})</b>
                  </div>
                </td>
              </tr>
              <tr>
                <td colspan="2">
                  <ui5-button icon="search"
                              @click="e => $refs.findEventDialog.show(e.target)">
                    Поиск мероприятия
                  </ui5-button>
                </td>
              </tr>
            </table>
          </div>
        </div>
        <ui5-tabcontainer fixed collapsed @tab-select="e => changeTab(e.detail.tabIndex)">
          <ui5-tab text="Информация о мероприятии" :selected="selectedTab === 'information'" />
          <ui5-tab text="Расписание" :selected="selectedTab === 'schedule'" />
          <ui5-tab text="Форма заявки пользователя" :selected="selectedTab === 'user_form'" />
          <ui5-tab text="Форма заявки участников от пользователя" :selected="selectedTab === 'part_forms'" />
        </ui5-tabcontainer>
        <div v-if="selectedEvent === null" style="width: 100%; text-align: center; justify-content: center">
          <div style="display: inline-block">
            <ui5-badge color-scheme="3">Выберите мероприятие</ui5-badge>
          </div>
        </div>
        <div v-if="selectedEvent !== null" style="width: 100%; text-align: center; justify-content: center">
          <div v-if="((selectedTab === 'information') && (Information !== '(информация)'))">
            <ui5-button icon="save"
                        :disabled="changeInfo"
                        @click="e => saveInformation()">
              Сохранить изменения
            </ui5-button><br/><br/>
            <TinyMCE ref='infoTinyMCE'
                     v-bind:Information="Information"
                     v-bind:additional-data="{name: selectedEvent.name}"
                     v-bind:editorHeight="580" />
          </div>
        </div>
      </ui5-card>
    </slot>
  </LkBase>
  <ui5-dialog ref="findEventDialog">
    <AdminEventsTable v-bind:tableColumns="tableColumns"
                      v-bind:headerText="'Поиск мероприятия'"
                      v-bind:tableMode="'SingleSelect'"
                      v-bind:addButton="false"
                      v-bind:activeRow="'Active'"
                      v-bind:activeRowEvent="setSelectedEvent"
                      v-bind:showActions="true"/>
    <div slot="footer" style="display: flex; justify-content: flex-end; width: 100%; align-items: center">
      <div style="flex: 1;"></div>
      <ui5-button design="Emphasized"
                  @click="e => $refs.findEventDialog.close()">
        Закрыть
      </ui5-button>
    </div>
  </ui5-dialog>
</template>

<script>
import LkBase from "../../../components/LkBase.vue";
import PaginationTable from "../../../components/PaginationTable.vue";
import AdminEventsTable from "./AdminEventsTable.vue";
import TinyMCE from "../../../components/TinyMCE.vue";

export default {
  name: 'AdminEventsManage',
  components: {TinyMCE, AdminEventsTable, LkBase, PaginationTable},
  data() {
    return {
      Information: '(информация)',
      changeInfo: false,
      selectedTab: 'information',
      selectedEvent: null,
      tableColumns: [
        {name: 'ID объекта', alias: 'object_id', whiteSpace: 'nowrap'},
        {name: 'Наименование', alias: 'name', whiteSpace: 'nowrap'},
        {name: 'Краткое пояснение', alias: 'description', whiteSpace: 'normal'},
        {name: 'Тип', alias: 'event_type', whiteSpace: 'normal'},
        {name: 'Сроки подачи заявок', alias: 'app_date_range', whiteSpace: 'nowrap'},
        {name: 'Сроки проведения мероприятия', alias: 'date_range', whiteSpace: 'nowrap'},
        {name: 'Категории участников', alias: 'categories', whiteSpace: 'nowrap'}
      ]
    }
  },
  methods: {
    setSelectedEvent(event) {
      this.selectedEvent = event
      this.selectedTab = ''
      this.getEventInformation()
      this.$refs.findEventDialog.close()
    },
    async saveInformation() {
      this.changeInfo = true
      let url = this.$store.state.backendUrl+'/api/v1/admins/information_save/'+this.selectedEvent.object_id+'/'
      await fetch (url,{
        method: 'PATCH',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'Content-Type': 'web_app/json;charset=UTF-8',
          'Authorization': 'Token '+getCookie('iohk_token')
        },
        body: JSON.stringify({
          'info': this.$refs.infoTinyMCE.editorText
        })
      })
          .then(resp => {
            if (resp.status === 200) {
              return resp.json()
            } else {
              this.changeInfo = false
              if (resp.status === 401) {
                showMessage('error', 'Пожалуйста, войдите в систему', false)
                this.$router.push('/?nextUrl='+window.location.href.split('/')[3])
                return false
              }
              showMessage('error', 'Произошла ошибка, повторите попытку позже')
            }
          })
          .then(data => {
            if (data['error']) {
              showMessage('error', data['error'])
            } else {
              showMessage('success', data['success'])
              this.getEventInformation()
            }
            this.changeInfo = false
          })
    },
    changeTab(index) {
      switch(index) {
        case 0:
          this.selectedTab = 'information'
          break

        case 1:
          this.selectedTab = 'schedule'
          break

        case 2:
          this.selectedTab = 'user_form'
          break

        default:
          this.selectedTab = 'part_forms'
      }
    },
    async getEventInformation() {
      await fetch(this.$store.state.backendUrl+'/api/v1/admins/information/?event='+this.selectedEvent.name, {
        method: 'GET',
        headers: {
          'X-CSRFToken': getCookie("csrftoken"),
          'Content-Type': 'web_app/json;charset=UTF-8',
          'Authorization': 'Token '+getCookie('iohk_token')
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
            this.Information = data[0]['info']
            this.selectedTab = 'information'
          })
    }
  }
}
</script>

<style scoped>

</style>